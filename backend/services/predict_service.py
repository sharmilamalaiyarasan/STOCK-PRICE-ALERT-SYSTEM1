from datetime import datetime
import pandas as pd
import yfinance as yf
from prophet import Prophet

def predict_threshold_time(symbol: str, target_price: float):
    try:
        print(f"🔮 Running prediction for {symbol} ...")

        # --- Download 6 months of hourly data ---
        df = yf.download(symbol, period="6mo", interval="1h", progress=False)
        if df.empty:
            return f"⚠️ Unable to fetch data for {symbol}"

        # --- Flatten any multi-index columns ---
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = ['_'.join(col).strip() if isinstance(col, tuple) else col for col in df.columns]

        # --- Reset index so Datetime becomes a column ---
        df = df.reset_index()

        # --- Normalize column names ---
        df.columns = [c.lower() for c in df.columns]
        print(f"✅ Columns after normalization: {df.columns.tolist()}")

        # --- Detect datetime column ---
        time_col = next((c for c in ["datetime", "date", "index", "time"] if c in df.columns), None)
        if not time_col:
            return f"⚠️ Could not find datetime column for {symbol}."

        # --- Detect close column ---
        close_col = next((c for c in df.columns if "close" in c), None)
        if not close_col:
            return f"⚠️ Data for {symbol} missing 'Close' prices."

        # --- Rename for Prophet ---
        df = df.rename(columns={time_col: "ds", close_col: "y"})

        # --- Clean timezone info ---
        df["ds"] = pd.to_datetime(df["ds"]).dt.tz_localize(None)  # ✅ FIX HERE
        df["y"] = pd.to_numeric(df["y"], errors="coerce")
        df = df.dropna(subset=["y"])

        # --- Train Prophet model ---
        model = Prophet(
            daily_seasonality=True,
            weekly_seasonality=True,
            changepoint_prior_scale=0.3,
        )
        model.fit(df[["ds", "y"]])

        # --- Forecast next 90 days hourly ---
        future = model.make_future_dataframe(periods=90 * 24, freq="H")
        forecast = model.predict(future)

        # --- Determine trend & crossing ---
        current_price = float(df["y"].iloc[-1])
        if current_price < target_price:
            crossing = forecast[forecast["yhat"] >= target_price]
            trend = "📈 Uptrend"
        else:
            crossing = forecast[forecast["yhat"] <= target_price]
            trend = "📉 Downtrend"

        if crossing.empty:
            max_pred = forecast["yhat"].max()
            min_pred = forecast["yhat"].min()
            extreme = max_pred if trend == "📈 Uptrend" else min_pred
            eta = forecast.iloc[-1]["ds"]
            return (
                f"⚠️ {symbol}: Target ${target_price:.2f} not reached within next 90 days.\n"
                f"Current: ${current_price:.2f}\n"
                f"Trend: {trend}\n"
                f"Max expected: ${extreme:.2f} by {eta.strftime('%Y-%m-%d %H:%M UTC')}"
            )

        eta = crossing.iloc[0]["ds"]
        hours_remaining = (eta - datetime.utcnow()).total_seconds() / 3600
        lower_time = (eta - pd.Timedelta(hours=6)).strftime("%Y-%m-%d %H:%M UTC")
        upper_time = (eta + pd.Timedelta(hours=6)).strftime("%Y-%m-%d %H:%M UTC")

        return (
            f"🎯 {symbol} {trend}\n"
            f"Current price: ${current_price:.2f}\n"
            f"Target price: ${target_price:.2f}\n"
            f"Predicted to reach around {eta.strftime('%Y-%m-%d %H:%M UTC')}\n"
            f"≈ In {hours_remaining:.1f} hours ({hours_remaining/24:.1f} days)\n"
            f"Confidence window: {lower_time} → {upper_time}"
        )

    except Exception as e:
        return f"❌ Prediction error: {e}"
