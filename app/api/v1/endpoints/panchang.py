"""
Panchang endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.v1.models import PanchangRequest
from app.core.vedic.panchang import panchang_calculator

router = APIRouter()


@router.post("/")
async def calculate_panchang(request: PanchangRequest):
    """
    Calculate Panchang (Vedic calendar) for a given date and location
    """
    try:
        # Parse date
        panchang_date = datetime.strptime(request.date, '%Y-%m-%d')
        
        # Calculate panchang
        panchang = panchang_calculator.calculate_panchang(
            date=panchang_date,
            latitude=request.latitude,
            longitude=request.longitude,
            timezone=request.timezone
        )
        
        return {
            "success": True,
            "panchang": panchang
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
