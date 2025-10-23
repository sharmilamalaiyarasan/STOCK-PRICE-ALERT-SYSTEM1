# backend/routes/watchlist_routes.py
from fastapi import APIRouter, Depends
from backend.services.watchlist_service import WatchlistService
from backend.utils.token import verify_access_token

router = APIRouter(prefix="/watchlist", tags=["Watchlist"])

@router.get("/")
async def get_watchlist(current_user=Depends(verify_access_token)):
    return await WatchlistService.get_watchlist(current_user["_id"])

@router.post("/add/{symbol}")
async def add_to_watchlist(symbol: str, current_user=Depends(verify_access_token)):
    return await WatchlistService.add_to_watchlist(current_user["_id"], symbol)

@router.delete("/remove/{symbol}")
async def remove_from_watchlist(symbol: str, current_user=Depends(verify_access_token)):
    return await WatchlistService.remove_from_watchlist(current_user["_id"], symbol)
