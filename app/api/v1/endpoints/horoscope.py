"""
Ashtakavarga and Horoscope endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.v1.models import BirthData
from app.core.chart_engine import chart_engine
from app.core.vedic.ashtakavarga import ashtakavarga_calculator
from app.core.vedic.yogas_doshas import yoga_dosha_calculator
from app.core.vedic.dasha import dasha_calculator
from app.core.vedic.divisional_charts import divisional_charts
from app.core.horoscope_engine import horoscope_engine
from pydantic import BaseModel

router = APIRouter()


class AshtakavargaRequest(BaseModel):
    """Ashtakavarga request"""
    birth_data: BirthData


class HoroscopeRequest(BaseModel):
    """Complete horoscope request"""
    birth_data: BirthData


@router.post("/ashtakavarga")
async def calculate_ashtakavarga(request: AshtakavargaRequest):
    """
    Calculate Ashtakavarga (8-point benefic system)
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
        
        # Get ascendant sign number
        ascendant_sign = int(chart['ascendant']['longitude'] / 30)
        
        # Calculate comprehensive Ashtakavarga
        ashtakavarga = ashtakavarga_calculator.calculate_comprehensive_ashtakavarga(
            planets=chart['planets'],
            ascendant_sign=ascendant_sign
        )
        
        return {
            "success": True,
            "name": birth_data.name,
            "ashtakavarga": ashtakavarga
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/complete")
async def generate_complete_horoscope(request: HoroscopeRequest):
    """
    Generate comprehensive horoscope report
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
        
        # Get yogas and doshas
        yogas_doshas = yoga_dosha_calculator.analyze_all_yogas_doshas(
            planets=chart['planets'],
            planet_houses=chart['planet_houses'],
            houses=chart['houses']
        )
        
        # Get dashas
        moon_longitude = chart['planets']['Moon']['longitude']
        dashas = dasha_calculator.calculate_vimshottari_dasha(
            moon_longitude=moon_longitude,
            birth_date=birth_datetime,
            years=120
        )
        
        # Get divisional charts
        div_charts = divisional_charts.calculate_all_charts(chart['planets'])
        
        # Get ashtakavarga
        ascendant_sign = int(chart['ascendant']['longitude'] / 30)
        ashtakavarga = ashtakavarga_calculator.calculate_comprehensive_ashtakavarga(
            planets=chart['planets'],
            ascendant_sign=ascendant_sign
        )
        
        # Generate comprehensive horoscope
        horoscope = horoscope_engine.generate_birth_horoscope(
            chart_data=chart,
            yogas_doshas=yogas_doshas,
            dashas=dashas,
            divisional_charts=div_charts,
            ashtakavarga=ashtakavarga
        )
        
        return {
            "success": True,
            "name": birth_data.name,
            "horoscope": horoscope
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
