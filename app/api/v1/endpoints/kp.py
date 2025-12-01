"""
KP System endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.v1.models import KPRequest
from app.core.chart_engine import chart_engine
from app.core.kp.kp_system import kp_system

router = APIRouter()


@router.post("/cuspal")
async def calculate_kp_cuspal(request: KPRequest):
    """
    Calculate KP cuspal positions with sub-lords
    """
    try:
        birth_data = request.birth_data
        
        # Parse datetime
        date_str = f"{birth_data.date} {birth_data.time}"
        birth_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        # Get birth chart
        chart = chart_engine.calculate_birth_chart(
            date=birth_datetime,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        
        # Calculate KP chart
        kp_chart = kp_system.calculate_kp_chart(
            planets=chart['planets'],
            houses=chart['houses'],
            planet_houses=chart['planet_houses']
        )
        
        return {
            "success": True,
            "name": birth_data.name,
            "kp_chart": kp_chart
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
