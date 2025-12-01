"""
Yogas and Doshas endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.v1.models import YogasRequest
from app.core.chart_engine import chart_engine
from app.core.vedic.yogas_doshas import yoga_dosha_calculator

router = APIRouter()


@router.post("")
@router.post("/")
@router.post("/analyze")
async def analyze_yogas_doshas(request: YogasRequest):
    """
    Analyze all yogas and doshas in the birth chart
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
        
        # Analyze yogas and doshas
        analysis = yoga_dosha_calculator.analyze_all_yogas_doshas(
            planets=chart['planets'],
            planet_houses=chart['planet_houses'],
            houses=chart['houses']
        )
        
        return {
            "success": True,
            "name": birth_data.name,
            "analysis": analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
