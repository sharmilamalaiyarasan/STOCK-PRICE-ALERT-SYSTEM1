# backend/routes/profile_routes.py
from fastapi import APIRouter, Depends, HTTPException
from backend.services.profile_service import ProfileService
from backend.utils.token import verify_access_token

router = APIRouter(prefix="/profile", tags=["Profile"])

@router.get("/me")
async def get_profile(current_user=Depends(verify_access_token)):
    profile = await ProfileService.get_profile(current_user["_id"])
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.put("/update")
async def update_profile(data: dict, current_user=Depends(verify_access_token)):
    success = await ProfileService.update_profile(current_user["_id"], data)
    return {"updated": success}

@router.put("/holdings")
async def update_holdings(data: dict, current_user=Depends(verify_access_token)):
    holdings = data.get("holdings", [])
    await ProfileService.update_holdings(current_user["_id"], holdings)
    return {"message": "Holdings updated"}

@router.put("/alerts")
async def toggle_alerts(enabled: bool, current_user=Depends(verify_access_token)):
    await ProfileService.toggle_alerts(current_user["_id"], enabled)
    return {"message": f"Email alerts {'enabled' if enabled else 'disabled'}"}
