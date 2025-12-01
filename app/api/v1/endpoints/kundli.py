"""
Comprehensive Kundli (Birth Chart) endpoints - AstroTalk level detail
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, List, Optional
from pydantic import BaseModel
from app.api.v1.models import BirthData
from app.core.chart_engine import chart_engine
from app.core.vedic.ashtakavarga import ashtakavarga_calculator
from app.core.vedic.yogas_doshas import yoga_dosha_calculator
from app.core.vedic.dasha import dasha_calculator
from app.core.vedic.divisional_charts import divisional_charts
from app.core.vedic.panchang import panchang_calculator
from app.core.horoscope_engine import horoscope_engine
from app.core.remedies import remedies_engine

router = APIRouter()


class KundliRequest(BaseModel):
    """Complete Kundli request"""
    birth_data: BirthData
    include_predictions: bool = True
    include_remedies: bool = True


class KundliBasicRequest(BaseModel):
    """Basic Kundli information request"""
    birth_data: BirthData


@router.post("/basic")
async def get_basic_kundli(request: KundliBasicRequest):
    """
    Get basic Kundli information including:
    - Personal details
    - Birth chart
    - Ascendant details
    - Planetary positions
    - House cusps
    - Panchang details
    """
    try:
        birth_data = request.birth_data
        date_str = f"{birth_data.date} {birth_data.time}"
        birth_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        # Calculate birth chart
        chart = chart_engine.calculate_birth_chart(
            date=birth_datetime,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        
        # Calculate panchang
        panchang = panchang_calculator.calculate_panchang(
            date=birth_datetime,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        
        # Get ascendant details
        ascendant_sign = int(chart['ascendant']['longitude'] / 30)
        ascendant_degree = chart['ascendant']['longitude'] % 30
        sign_names = ['Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo', 
                     'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces']
        
        # Calculate Moon sign (Rashi)
        moon_sign = int(chart['planets']['Moon']['longitude'] / 30)
        
        # Calculate Sun sign
        sun_sign = int(chart['planets']['Sun']['longitude'] / 30)
        
        # Get nakshatra details for Moon
        moon_longitude = chart['planets']['Moon']['longitude']
        nakshatra_span = 360 / 27
        nakshatra_num = int(moon_longitude / nakshatra_span)
        nakshatra_names = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
            'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
            'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
            'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
            'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
        ]
        
        # Planetary strengths
        planet_strengths = {}
        for planet_name, planet_data in chart['planets'].items():
            house_num = chart['planet_houses'][planet_name]
            is_exalted = _check_exaltation(planet_name, planet_data['sign'])
            is_debilitated = _check_debilitation(planet_name, planet_data['sign'])
            is_own_sign = _check_own_sign(planet_name, planet_data['sign'])
            
            strength = "Average"
            if is_exalted:
                strength = "Exalted (Excellent)"
            elif is_debilitated:
                strength = "Debilitated (Weak)"
            elif is_own_sign:
                strength = "Own Sign (Strong)"
            
            planet_strengths[planet_name] = {
                'strength': strength,
                'is_exalted': is_exalted,
                'is_debilitated': is_debilitated,
                'is_own_sign': is_own_sign,
                'house': house_num,
                'sign': planet_data['sign']
            }
        
        return {
            "success": True,
            "personal_details": {
                "name": birth_data.name,
                "date_of_birth": birth_data.date,
                "time_of_birth": birth_data.time,
                "place_of_birth": f"Lat: {birth_data.latitude}, Long: {birth_data.longitude}",
                "timezone": birth_data.timezone
            },
            "vedic_details": {
                "ascendant": {
                    "sign": sign_names[ascendant_sign],
                    "sign_number": ascendant_sign + 1,
                    "degree": round(ascendant_degree, 2),
                    "lord": _get_sign_lord(sign_names[ascendant_sign])
                },
                "moon_sign": {
                    "sign": sign_names[moon_sign],
                    "sign_number": moon_sign + 1,
                    "nakshatra": nakshatra_names[nakshatra_num],
                    "nakshatra_lord": _get_nakshatra_lord(nakshatra_num)
                },
                "sun_sign": {
                    "sign": sign_names[sun_sign],
                    "sign_number": sun_sign + 1
                }
            },
            "panchang": panchang,
            "planets": chart['planets'],
            "planet_houses": chart['planet_houses'],
            "planet_strengths": planet_strengths,
            "houses": chart['houses'],
            "birth_chart_d1": _format_chart_for_display(chart)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/complete")
async def get_complete_kundli(request: KundliRequest):
    """
    Get complete comprehensive Kundli with all details:
    - Basic chart information
    - All divisional charts (D1-D60)
    - Ashtakavarga analysis
    - Vimshottari Dasha (120 years)
    - All Yogas and Doshas
    - Planetary strengths and friendships
    - Life predictions
    - Remedies
    """
    try:
        birth_data = request.birth_data
        date_str = f"{birth_data.date} {birth_data.time}"
        birth_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        # 1. Birth chart
        chart = chart_engine.calculate_birth_chart(
            date=birth_datetime,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        
        # 2. Panchang
        panchang = panchang_calculator.calculate_panchang(
            date=birth_datetime,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        
        # 3. Divisional charts
        div_charts = divisional_charts.calculate_all_charts(chart['planets'])
        
        # 4. Ashtakavarga
        ascendant_sign = int(chart['ascendant']['longitude'] / 30)
        ashtakavarga = ashtakavarga_calculator.calculate_comprehensive_ashtakavarga(
            planets=chart['planets'],
            ascendant_sign=ascendant_sign
        )
        
        # 5. Yogas and Doshas
        yogas_doshas = yoga_dosha_calculator.analyze_all_yogas_doshas(
            planets=chart['planets'],
            planet_houses=chart['planet_houses'],
            houses=chart['houses']
        )
        
        # 6. Vimshottari Dasha
        moon_longitude = chart['planets']['Moon']['longitude']
        dashas = dasha_calculator.calculate_vimshottari_dasha(
            moon_longitude=moon_longitude,
            birth_date=birth_datetime,
            years=120
        )
        
        # 7. Current Dasha period
        current_dasha = _get_current_dasha_period(dashas)
        
        # 8. Planetary analysis
        planetary_analysis = _analyze_planets_detailed(chart, yogas_doshas)
        
        # 9. Life predictions
        predictions = None
        if request.include_predictions:
            predictions = horoscope_engine.generate_birth_horoscope(
                chart_data=chart,
                yogas_doshas=yogas_doshas,
                dashas=dashas,
                divisional_charts=div_charts,
                ashtakavarga=ashtakavarga
            )
        
        # 10. Remedies
        remedies = None
        if request.include_remedies:
            remedies = remedies_engine.get_personalized_remedies(
                chart_data=chart,
                yogas_doshas=yogas_doshas,
                ashtakavarga=ashtakavarga
            )
        
        return {
            "success": True,
            "name": birth_data.name,
            "basic_details": {
                "date_of_birth": birth_data.date,
                "time_of_birth": birth_data.time,
                "place": f"Lat: {birth_data.latitude}, Long: {birth_data.longitude}",
                "timezone": birth_data.timezone
            },
            "birth_chart": _format_chart_for_display(chart),
            "panchang": panchang,
            "divisional_charts": div_charts,
            "ashtakavarga": ashtakavarga,
            "yogas_doshas": yogas_doshas,
            "dashas": dashas,
            "current_dasha": current_dasha,
            "planetary_analysis": planetary_analysis,
            "predictions": predictions,
            "remedies": remedies
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/charts")
async def get_all_charts(request: KundliBasicRequest):
    """
    Get all divisional charts (D1 to D60) formatted for display
    """
    try:
        birth_data = request.birth_data
        date_str = f"{birth_data.date} {birth_data.time}"
        birth_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        chart = chart_engine.calculate_birth_chart(
            date=birth_datetime,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        
        div_charts = divisional_charts.calculate_all_charts(chart['planets'])
        
        # Format each chart for display
        formatted_charts = {}
        for chart_name, chart_data in div_charts.items():
            formatted_charts[chart_name] = {
                "data": chart_data,
                "display": _format_divisional_chart_for_display(chart_data)
            }
        
        return {
            "success": True,
            "name": birth_data.name,
            "charts": formatted_charts
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/planetary-analysis")
async def get_planetary_analysis(request: KundliBasicRequest):
    """
    Detailed planetary analysis including:
    - Planetary positions
    - Strengths (Shadbala)
    - Friendships
    - Aspects
    - Yogas formed
    """
    try:
        birth_data = request.birth_data
        date_str = f"{birth_data.date} {birth_data.time}"
        birth_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        chart = chart_engine.calculate_birth_chart(
            date=birth_datetime,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        
        yogas_doshas = yoga_dosha_calculator.analyze_all_yogas_doshas(
            planets=chart['planets'],
            planet_houses=chart['planet_houses'],
            houses=chart['houses']
        )
        
        analysis = _analyze_planets_detailed(chart, yogas_doshas)
        
        return {
            "success": True,
            "name": birth_data.name,
            "planetary_analysis": analysis
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/dasha-predictions")
async def get_dasha_predictions(request: KundliBasicRequest):
    """
    Current and upcoming Dasha predictions
    """
    try:
        birth_data = request.birth_data
        date_str = f"{birth_data.date} {birth_data.time}"
        birth_datetime = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        
        chart = chart_engine.calculate_birth_chart(
            date=birth_datetime,
            latitude=birth_data.latitude,
            longitude=birth_data.longitude,
            timezone=birth_data.timezone
        )
        
        moon_longitude = chart['planets']['Moon']['longitude']
        dashas = dasha_calculator.calculate_vimshottari_dasha(
            moon_longitude=moon_longitude,
            birth_date=birth_datetime,
            years=120
        )
        
        current_dasha = _get_current_dasha_period(dashas)
        dasha_predictions = _generate_dasha_predictions(current_dasha, chart)
        
        return {
            "success": True,
            "name": birth_data.name,
            "current_dasha": current_dasha,
            "predictions": dasha_predictions,
            "upcoming_periods": _get_upcoming_dasha_periods(dashas, 5)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Helper functions

def _format_chart_for_display(chart: Dict) -> Dict:
    """Format chart data for visual display"""
    houses_with_planets = {}
    
    for i in range(1, 13):
        houses_with_planets[i] = {
            "sign": chart['houses'][i]['sign'],
            "planets": []
        }
    
    for planet_name, house_num in chart['planet_houses'].items():
        planet_data = chart['planets'][planet_name]
        houses_with_planets[house_num]['planets'].append({
            "name": planet_name,
            "degree": round(planet_data['longitude'] % 30, 2)
        })
    
    return houses_with_planets


def _format_divisional_chart_for_display(chart_data: Dict) -> Dict:
    """Format divisional chart for display"""
    houses_with_planets = {}
    
    for i in range(1, 13):
        houses_with_planets[i] = {"planets": []}
    
    for planet_name, planet_info in chart_data.items():
        house = planet_info['house']
        if house not in houses_with_planets:
            houses_with_planets[house] = {"planets": []}
        
        houses_with_planets[house]['planets'].append({
            "name": planet_name,
            "sign": planet_info['sign']
        })
    
    return houses_with_planets


def _check_exaltation(planet: str, sign: str) -> bool:
    """Check if planet is exalted"""
    exaltations = {
        'Sun': 'Aries', 'Moon': 'Taurus', 'Mars': 'Capricorn',
        'Mercury': 'Virgo', 'Jupiter': 'Cancer', 'Venus': 'Pisces',
        'Saturn': 'Libra'
    }
    return exaltations.get(planet) == sign


def _check_debilitation(planet: str, sign: str) -> bool:
    """Check if planet is debilitated"""
    debilitations = {
        'Sun': 'Libra', 'Moon': 'Scorpio', 'Mars': 'Cancer',
        'Mercury': 'Pisces', 'Jupiter': 'Capricorn', 'Venus': 'Virgo',
        'Saturn': 'Aries'
    }
    return debilitations.get(planet) == sign


def _check_own_sign(planet: str, sign: str) -> bool:
    """Check if planet is in own sign"""
    own_signs = {
        'Sun': ['Leo'],
        'Moon': ['Cancer'],
        'Mars': ['Aries', 'Scorpio'],
        'Mercury': ['Gemini', 'Virgo'],
        'Jupiter': ['Sagittarius', 'Pisces'],
        'Venus': ['Taurus', 'Libra'],
        'Saturn': ['Capricorn', 'Aquarius']
    }
    return sign in own_signs.get(planet, [])


def _get_sign_lord(sign: str) -> str:
    """Get ruling planet of sign"""
    lords = {
        'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury',
        'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury',
        'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter',
        'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
    }
    return lords.get(sign, 'Unknown')


def _get_nakshatra_lord(nakshatra_num: int) -> str:
    """Get nakshatra lord"""
    lords = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
    return lords[nakshatra_num % 9]


def _analyze_planets_detailed(chart: Dict, yogas_doshas: Dict) -> Dict:
    """Detailed planetary analysis"""
    analysis = {}
    
    for planet_name, planet_data in chart['planets'].items():
        house = chart['planet_houses'][planet_name]
        sign = planet_data['sign']
        
        analysis[planet_name] = {
            "position": {
                "sign": sign,
                "house": house,
                "degree": round(planet_data['longitude'] % 30, 2),
                "nakshatra": planet_data.get('nakshatra', 'Unknown')
            },
            "strength": {
                "exalted": _check_exaltation(planet_name, sign),
                "debilitated": _check_debilitation(planet_name, sign),
                "own_sign": _check_own_sign(planet_name, sign),
                "retrograde": planet_data.get('retrograde', False)
            },
            "significations": _get_planet_significations(planet_name),
            "house_effects": _get_house_effects(planet_name, house)
        }
    
    return analysis


def _get_planet_significations(planet: str) -> List[str]:
    """Get what planet signifies"""
    significations = {
        'Sun': ['Soul', 'Father', 'Authority', 'Government', 'Status', 'Confidence'],
        'Moon': ['Mind', 'Mother', 'Emotions', 'Public', 'Travel', 'Nurturing'],
        'Mars': ['Energy', 'Courage', 'Property', 'Siblings', 'Accidents', 'Sports'],
        'Mercury': ['Intelligence', 'Communication', 'Business', 'Education', 'Skills'],
        'Jupiter': ['Wisdom', 'Wealth', 'Children', 'Teachers', 'Fortune', 'Religion'],
        'Venus': ['Love', 'Marriage', 'Luxury', 'Arts', 'Beauty', 'Vehicles'],
        'Saturn': ['Discipline', 'Karma', 'Delays', 'Hard work', 'Longevity', 'Justice'],
        'Rahu': ['Obsession', 'Innovation', 'Foreign', 'Technology', 'Illusion'],
        'Ketu': ['Spirituality', 'Liberation', 'Past life', 'Research', 'Detachment']
    }
    return significations.get(planet, [])


def _get_house_effects(planet: str, house: int) -> str:
    """Get effects of planet in specific house"""
    effects = {
        1: f"{planet} in 1st house affects personality, appearance, and self",
        2: f"{planet} in 2nd house affects wealth, family, and speech",
        3: f"{planet} in 3rd house affects courage, siblings, and communication",
        4: f"{planet} in 4th house affects home, mother, and emotions",
        5: f"{planet} in 5th house affects children, creativity, and education",
        6: f"{planet} in 6th house affects health, enemies, and service",
        7: f"{planet} in 7th house affects marriage, partnerships, and business",
        8: f"{planet} in 8th house affects transformation, longevity, and occult",
        9: f"{planet} in 9th house affects fortune, father, and spirituality",
        10: f"{planet} in 10th house affects career, status, and profession",
        11: f"{planet} in 11th house affects gains, friends, and ambitions",
        12: f"{planet} in 12th house affects expenses, losses, and liberation"
    }
    return effects.get(house, "Unknown effect")


def _get_current_dasha_period(dashas: Dict) -> Dict:
    """Get currently running dasha period"""
    current_date = datetime.now()
    
    for mahadasha in dashas.get('mahadasha_periods', []):
        start = datetime.fromisoformat(mahadasha['start_date'].replace('Z', '+00:00'))
        end = datetime.fromisoformat(mahadasha['end_date'].replace('Z', '+00:00'))
        
        if start <= current_date <= end:
            # Find current antardasha
            for antardasha in mahadasha.get('antardasha_periods', []):
                ant_start = datetime.fromisoformat(antardasha['start_date'].replace('Z', '+00:00'))
                ant_end = datetime.fromisoformat(antardasha['end_date'].replace('Z', '+00:00'))
                
                if ant_start <= current_date <= ant_end:
                    return {
                        "mahadasha": mahadasha['planet'],
                        "mahadasha_start": mahadasha['start_date'],
                        "mahadasha_end": mahadasha['end_date'],
                        "antardasha": antardasha['planet'],
                        "antardasha_start": antardasha['start_date'],
                        "antardasha_end": antardasha['end_date']
                    }
    
    return {"mahadasha": "Unknown", "antardasha": "Unknown"}


def _generate_dasha_predictions(current_dasha: Dict, chart: Dict) -> Dict:
    """Generate predictions for current dasha period"""
    maha_planet = current_dasha.get('mahadasha', 'Unknown')
    antar_planet = current_dasha.get('antardasha', 'Unknown')
    
    return {
        "mahadasha_effects": f"{maha_planet} Mahadasha brings focus on {', '.join(_get_planet_significations(maha_planet)[:3])}",
        "antardasha_effects": f"{antar_planet} Antardasha influences {', '.join(_get_planet_significations(antar_planet)[:2])}",
        "combined_prediction": f"Period of {maha_planet}-{antar_planet} suggests balanced focus on both planetary themes",
        "areas_of_focus": _get_planet_significations(maha_planet) + _get_planet_significations(antar_planet),
        "recommendations": [
            f"Strengthen {maha_planet} through remedies",
            f"Be mindful of {antar_planet} significations",
            "Regular spiritual practices recommended"
        ]
    }


def _get_upcoming_dasha_periods(dashas: Dict, count: int) -> List[Dict]:
    """Get upcoming dasha periods"""
    current_date = datetime.now()
    upcoming = []
    
    for mahadasha in dashas.get('mahadasha_periods', []):
        start = datetime.fromisoformat(mahadasha['start_date'].replace('Z', '+00:00'))
        
        if start > current_date:
            upcoming.append({
                "planet": mahadasha['planet'],
                "start_date": mahadasha['start_date'],
                "end_date": mahadasha['end_date'],
                "duration_years": mahadasha.get('duration', 0)
            })
            
            if len(upcoming) >= count:
                break
    
    return upcoming
