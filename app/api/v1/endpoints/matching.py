"""
Matching endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.v1.models import MatchingRequest
from app.core.chart_engine import chart_engine
from app.core.matching.ashtakoot import ashtakoot_matching
from app.core.vedic.yogas_doshas import yoga_dosha_calculator

router = APIRouter()


@router.post("/ashtakoot")
async def calculate_ashtakoot_matching(request: MatchingRequest):
    """
    Calculate Ashtakoot (8-Kuta) compatibility matching
    """
    try:
        male_data = request.male_data
        female_data = request.female_data
        
        # Parse male birth datetime
        male_date_str = f"{male_data.date} {male_data.time}"
        male_datetime = datetime.strptime(male_date_str, '%Y-%m-%d %H:%M:%S')
        
        # Parse female birth datetime
        female_date_str = f"{female_data.date} {female_data.time}"
        female_datetime = datetime.strptime(female_date_str, '%Y-%m-%d %H:%M:%S')
        
        # Get male chart
        male_chart = chart_engine.calculate_birth_chart(
            date=male_datetime,
            latitude=male_data.latitude,
            longitude=male_data.longitude,
            timezone=male_data.timezone
        )
        
        # Get female chart
        female_chart = chart_engine.calculate_birth_chart(
            date=female_datetime,
            latitude=female_data.latitude,
            longitude=female_data.longitude,
            timezone=female_data.timezone
        )
        
        # Extract Moon data
        male_moon = male_chart['planets']['Moon']
        female_moon = female_chart['planets']['Moon']
        
        # Calculate matching
        matching = ashtakoot_matching.calculate_ashtakoot_matching(
            male_moon_sign=male_moon['sign'],
            male_moon_sign_num=male_moon['sign_num'],
            male_nakshatra=male_moon['nakshatra'],
            male_nakshatra_num=male_moon['nakshatra_num'],
            female_moon_sign=female_moon['sign'],
            female_moon_sign_num=female_moon['sign_num'],
            female_nakshatra=female_moon['nakshatra'],
            female_nakshatra_num=female_moon['nakshatra_num']
        )
        
        # Check Mangal Dosha for both
        male_mangal = yoga_dosha_calculator.detect_mangal_dosha(
            male_chart['planets'],
            male_chart['planet_houses']
        )
        
        female_mangal = yoga_dosha_calculator.detect_mangal_dosha(
            female_chart['planets'],
            female_chart['planet_houses']
        )
        
        return {
            "success": True,
            "male_name": male_data.name,
            "female_name": female_data.name,
            "ashtakoot_matching": matching,
            "male_mangal_dosha": male_mangal,
            "female_mangal_dosha": female_mangal
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
