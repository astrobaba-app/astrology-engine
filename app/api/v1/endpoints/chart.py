"""
Chart endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.v1.models import ChartRequest
from app.core.chart_engine import chart_engine

router = APIRouter()


@router.post("/birth")
async def calculate_birth_chart(request: ChartRequest):
    """
    Calculate complete birth chart with planetary positions and houses
    """
    try:
        birth_data = request.birth_data
        
        # Parse datetime
        date_str = f"{birth_data.date} {birth_data.time}"
        birth_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        # Calculate chart
        chart = chart_engine.calculate_birth_chart(
            date=birth_datetime,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone,
            house_system=request.house_system
        )
        
        return {
            "success": True,
            "name": birth_data.name,
            "chart": chart
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
