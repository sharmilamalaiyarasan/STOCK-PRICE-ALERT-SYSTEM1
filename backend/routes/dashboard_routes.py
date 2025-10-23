# backend/routes/dashboard_routes.py
from fastapi import APIRouter, Depends
from backend.services.dashboard_service import DashboardService
from backend.utils.token import verify_access_token

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.post("/log")
async def log_trade(data: dict, current_user=Depends(verify_access_token)):
    return await DashboardService.log_trade(
        current_user["_id"],
        data["symbol"],
        data["action"],
        data["qty"],
        data["price"]
    )

@router.get("/history")
async def get_trade_history(current_user=Depends(verify_access_token)):
    return await DashboardService.get_trade_history(current_user["_id"])
