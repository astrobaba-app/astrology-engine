"""
Daily, Weekly, Monthly, Yearly Horoscope Endpoints
"""
from fastapi import APIRouter, HTTPException, Query
from datetime import datetime
from pydantic import BaseModel
from app.core.transit_horoscope import transit_horoscope

router = APIRouter()


class HoroscopeResponse(BaseModel):
    """Horoscope response model"""
    success: bool
    data: dict


@router.get("/daily/{zodiac_sign}")
async def get_daily_horoscope(
    zodiac_sign: str,
    date: str = Query(None, description="Date in YYYY-MM-DD format (default: today)")
):
    """
    Get daily horoscope for a zodiac sign
    
    **Zodiac Signs**: Aries, Taurus, Gemini, Cancer, Leo, Virgo, 
    Libra, Scorpio, Sagittarius, Capricorn, Aquarius, Pisces
    
    **Example**: GET /api/v1/horoscope/daily/Aries?date=2025-12-01
    """
    try:
        # Validate zodiac sign
        valid_signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        zodiac_sign = zodiac_sign.capitalize()
        if zodiac_sign not in valid_signs:
            raise HTTPException(status_code=400, detail=f"Invalid zodiac sign. Must be one of: {', '.join(valid_signs)}")
        
        # Parse date if provided
        target_date = None
        if date:
            try:
                target_date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        # Generate horoscope
        horoscope = transit_horoscope.generate_daily_horoscope(zodiac_sign, target_date)
        
        return {
            "success": True,
            "data": horoscope
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/weekly/{zodiac_sign}")
async def get_weekly_horoscope(
    zodiac_sign: str,
    start_date: str = Query(None, description="Week start date in YYYY-MM-DD format (default: today)")
):
    """
    Get weekly horoscope for a zodiac sign
    
    **Example**: GET /api/v1/horoscope/weekly/Leo?start_date=2025-12-01
    """
    try:
        valid_signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        zodiac_sign = zodiac_sign.capitalize()
        if zodiac_sign not in valid_signs:
            raise HTTPException(status_code=400, detail=f"Invalid zodiac sign. Must be one of: {', '.join(valid_signs)}")
        
        target_date = None
        if start_date:
            try:
                target_date = datetime.strptime(start_date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        horoscope = transit_horoscope.generate_weekly_horoscope(zodiac_sign, target_date)
        
        return {
            "success": True,
            "data": horoscope
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/monthly/{zodiac_sign}")
async def get_monthly_horoscope(
    zodiac_sign: str,
    year: int = Query(None, description="Year (default: current year)"),
    month: int = Query(None, description="Month 1-12 (default: current month)")
):
    """
    Get monthly horoscope for a zodiac sign
    
    **Example**: GET /api/v1/horoscope/monthly/Virgo?year=2025&month=12
    """
    try:
        valid_signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        zodiac_sign = zodiac_sign.capitalize()
        if zodiac_sign not in valid_signs:
            raise HTTPException(status_code=400, detail=f"Invalid zodiac sign. Must be one of: {', '.join(valid_signs)}")
        
        if month and (month < 1 or month > 12):
            raise HTTPException(status_code=400, detail="Month must be between 1 and 12")
        
        horoscope = transit_horoscope.generate_monthly_horoscope(zodiac_sign, year, month)
        
        return {
            "success": True,
            "data": horoscope
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/yearly/{zodiac_sign}")
async def get_yearly_horoscope(
    zodiac_sign: str,
    year: int = Query(None, description="Year (default: current year)")
):
    """
    Get yearly horoscope for a zodiac sign
    
    **Example**: GET /api/v1/horoscope/yearly/Scorpio?year=2025
    """
    try:
        valid_signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        zodiac_sign = zodiac_sign.capitalize()
        if zodiac_sign not in valid_signs:
            raise HTTPException(status_code=400, detail=f"Invalid zodiac sign. Must be one of: {', '.join(valid_signs)}")
        
        horoscope = transit_horoscope.generate_yearly_horoscope(zodiac_sign, year)
        
        return {
            "success": True,
            "data": horoscope
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/all-signs/daily")
async def get_all_signs_daily(
    date: str = Query(None, description="Date in YYYY-MM-DD format (default: today)")
):
    """
    Get daily horoscope for ALL zodiac signs
    
    **Example**: GET /api/v1/horoscope/all-signs/daily?date=2025-12-01
    """
    try:
        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        target_date = None
        if date:
            try:
                target_date = datetime.strptime(date, '%Y-%m-%d')
            except ValueError:
                raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
        
        all_horoscopes = {}
        for sign in signs:
            all_horoscopes[sign] = transit_horoscope.generate_daily_horoscope(sign, target_date)
        
        return {
            "success": True,
            "data": {
                "date": date or datetime.now().strftime('%Y-%m-%d'),
                "horoscopes": all_horoscopes
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
