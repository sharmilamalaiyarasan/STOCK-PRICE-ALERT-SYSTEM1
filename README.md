# 📈 Real-Time Stock Monitoring and Alert System
This project focuses on developing an **AI-powered stock tracking system** that enhances trading efficiency through **real-time price monitoring, predictive analytics, and instant alert notifications**.
The system integrates:
- **Temporal Convolutional Network (TCN)** for short-term price forecasting
- **FinBERT** for financial news sentiment analysis

Together, they provide users with **automated, data-driven insights** beyond manual tracking — ensuring faster, smarter trading decisions.

---

## ⚙️ Problem Statement
Manual stock tracking is inefficient and error-prone, often leading to delayed reactions and missed opportunities.  
Users need an intelligent, real-time system that:
- Monitors stock prices continuously
- Tracks market sentiment
- Sends **instant Buy/Sell alerts** when defined conditions are met

This ensures users can act immediately and make informed trading decisions.

---

## 🎯 Project Objectives
| Objective | Description |
|------------|-------------|
| **Data Collection** | Collect real-time stock prices and financial news data via APIs. |
| **Price Prediction** | Use a **TCN model** to forecast the next stock price from historical data. |
| **Threshold Alerting** | Trigger instant **SMS alerts** through Vonage when price thresholds are met. |
| **Sentiment Analysis** | Analyze daily news sentiment using **FinBERT** and summarize for users. |
| **Dashboard Visualization** | Build an interactive dashboard for live data, portfolio, and alerts. |
| **User Management** | Enable secure signup/login with **Google or phone (OTP)** authentication. |

---

## 📊 Expected Outcomes
✅ Automated, real-time SMS alerts for Buy/Sell decisions  
✅ Interactive dashboard with live charts, performance graphs, and trade history  
✅ Personalized, authenticated user access  
✅ Enhanced trading responsiveness and data-backed decision making  

---

## 🏗️ System Architecture

### 🔹 Overview
The system follows an **event-driven, microservices architecture** with modular layers for frontend, backend, database, and AI models.

### 🔹 Workflow
#### Step 1: User Authentication
- Secure login via **Google OAuth** or **Phone OTP**
- User profiles stored in **MongoDB**

#### Step 2: Data Ingestion
- **Price Data:** Collected from stock APIs
- **News Data:** Processed through **FinBERT** for sentiment scoring
- **Historical Data:** Stored in **TimescaleDB** for time-series optimization

#### Step 3: Price Prediction
- **PyTorch TCN** model predicts the next stock price using the last 30 data points

#### Step 4: Alert & Notification
- **Celery + Redis** scheduler continuously checks for threshold breaches
- On trigger, sends **Buy/Sell alerts** to users via **Vonage SMS API**

#### Step 5: Dashboard Visualization
- Built with **React.js** and **Chart.js / Recharts**
- Displays live prices, sentiment scores, trade history, and performance analytics

---

## 🧩 Tools and Technologies

| Layer | Tools / Technologies | Responsibilities |
|-------|-----------------------|------------------|
| **Frontend** | React.js, Chart.js, Recharts | Display live stock data, trade history, and graphs |
| **Backend / API** | FastAPI, Celery, Redis | Handle requests, schedule tasks, and ensure security |
| **Database** | MongoDB, TimescaleDB | Store user data, alerts, and historical stock records |
| **Model** | PyTorch (TCN), FinBERT (HuggingFace) | Forecast prices and analyze sentiment |
| **Notification** | Vonage SMS API | Send instant alerts and summaries |
| **Authentication** | JWT, Google OAuth | Secure login and session handling |
| **Hosting** | GitHub | Deployment and version control |

---

## 🔧 Tool Definition Block

| Tool | Definition |
|------|-------------|
| **Vonage** | Cloud communication API to send SMS alerts instantly when price thresholds are breached. |
| **TCN (Temporal Convolutional Network)** | Deep learning model specialized for time-series forecasting (stock price prediction). |
| **FinBERT** | BERT model fine-tuned for financial text sentiment analysis. |
| **MongoDB** | NoSQL database for user profiles, alerts, and general app data. |
| **TimescaleDB** | Time-series PostgreSQL extension optimized for stock price data ingestion and queries. |
| **FastAPI** | High-performance Python web framework for backend APIs. |
| **ReactJS** | JavaScript library for creating a responsive, interactive dashboard frontend. |

---

## 🖥️ Current Status
✅ Project setup completed  
✅ Frontend and backend communication established  
✅ Real-time price fetching APIs integrated  
✅ MongoDB & TimescaleDB connected  
🚧 Work in progress on:
- Model integration (TCN & FinBERT)
- Automated alert triggering via Celery/Vonage
- Dashboard enhancements and deployment

---

## 🚀 How to Run (Developer Setup)

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/<your-repo-name>.git
cd stock-monitoring-system
```

### 2️⃣ Setup Virtual Environment
```bash
python -m venv venv
venv\Scripts\activate     # on Windows
source venv/bin/activate  # on Linux/Mac
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Configure Environment Variables
Create a `.env` file in the backend directory with:
```
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db
MONGO_USER=your_user
MONGO_PASSWORD=your_password
FINANCIAL_API_KEY=your_api_key
TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
JWT_SECRET=your_secret
```

### 5️⃣ Run the Backend Server
```bash
uvicorn backend.main:app --reload
```

### 6️⃣ Run Celery Worker
```bash
celery -A backend.tasks worker --loglevel=info
```

### 7️⃣ Start the Frontend
```bash
cd frontend
npm install
npm start
```

Then open the app in your browser at **http://localhost:3000**

---

## 📈 Future Enhancements
- Integration of Reinforcement Learning for automated trade simulation
- Voice/WhatsApp alerts using Twilio
- Multi-user portfolio analytics
- Cloud deployment (AWS / Render / Railway)

---

## 📜 License
This project is licensed under the **MIT License** — free for educational and research purposes.

---

## 💡 Acknowledgements
Special thanks to the open-source communities of:
- [FastAPI](https://fastapi.tiangolo.com)
- [PyTorch](https://pytorch.org)
- [HuggingFace](https://huggingface.co)
- [Twilio](https://www.twilio.com)
- [React.js](https://react.dev)

---

## 👥 Collaborators

[Boomika S](https://github.com/boomiikas) |
[Sakthi  Gowshick S](https://github.com/sakthigowshick) |
[Sanjaykumar S](https://github.com/sanjaysk17) |
[Sharmila M](https://github.com/sharmilamalaiyarasan) |
[Subhiksha Kodibass](https://github.com/subhiksha-kodi) 
