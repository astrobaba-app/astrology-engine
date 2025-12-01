"""
Dasha endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.v1.models import DashaRequest
from app.core.chart_engine import chart_engine
from app.core.vedic.dasha import dasha_calculator

router = APIRouter()


@router.post("/vimshottari")
async def calculate_vimshottari_dasha(request: DashaRequest):
    """
    Calculate Vimshottari Dasha periods
    """
    try:
        birth_data = request.birth_data
        
        # Parse datetime
        date_str = f"{birth_data.date} {birth_data.time}"
        birth_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        # Get chart for Moon position
        chart = chart_engine.calculate_birth_chart(
            date=birth_datetime,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        
        # Get Moon longitude
        moon_longitude = chart['planets']['Moon']['longitude']
        
        # Calculate dashas
        dashas = dasha_calculator.calculate_vimshottari_dasha(
            moon_longitude=moon_longitude,
            birth_date=birth_datetime,
            years=request.years
        )
        
        return {
            "success": True,
            "name": birth_data.name,
            "dashas": dashas
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/antardasha")
async def calculate_antardasha(
    maha_dasha_lord: str,
    maha_dasha_start: str,
    maha_dasha_years: float
):
    """
    Calculate Antardasha (sub-periods) within a Mahadasha
    """
    try:
        start_date = datetime.strptime(maha_dasha_start, '%Y-%m-%d')
        
        antardashas = dasha_calculator.calculate_antardasha(
            maha_dasha_lord=maha_dasha_lord,
            maha_dasha_start=start_date,
            maha_dasha_years=maha_dasha_years
        )
        
        return {
            "success": True,
            "antardashas": antardashas
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
