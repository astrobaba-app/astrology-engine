"""
Divisional Charts endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.v1.models import DivisionalChartRequest
from app.core.chart_engine import chart_engine
from app.core.vedic.divisional_charts import divisional_charts

router = APIRouter()


@router.post("/")
async def calculate_divisional_chart(request: DivisionalChartRequest):
    """
    Calculate specific divisional chart (D1, D9, D10, etc.)
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
        
        # Calculate divisional chart
        div_chart = divisional_charts.calculate_chart(
            planets=chart['planets'],
            division=request.division
        )
        
        return {
            "success": True,
            "name": birth_data.name,
            "divisional_chart": div_chart
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/all")
async def calculate_all_divisional_charts(birth_data_request: dict):
    """
    Calculate all major divisional charts
    """
    try:
        birth_data = birth_data_request.get('birth_data')
        
        # Parse datetime
        date_str = f"{birth_data['date']} {birth_data['time']}"
        birth_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        # Get birth chart
        chart = chart_engine.calculate_birth_chart(
            date=birth_datetime,
            latitude=birth_data['latitude'],
            longitude=birth_data['longitude'],
            timezone=birth_data.get('timezone', 'Asia/Kolkata')
        )
        
        # Calculate all charts
        all_charts = divisional_charts.calculate_all_charts(chart['planets'])
        
        return {
            "success": True,
            "name": birth_data['name'],
            "divisional_charts": all_charts
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
