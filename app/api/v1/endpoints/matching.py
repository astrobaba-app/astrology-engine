"""
Matching endpoints
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from app.api.v1.models import MatchingRequest
from app.core.chart_engine import chart_engine
from app.core.matching.ashtakoot import ashtakoot_matching
from app.core.matching.dashakoot import dashakoot_matching
from app.core.vedic.yogas_doshas import yoga_dosha_calculator
from app.core.vedic.divisional_charts import divisional_charts

router = APIRouter()


def _get_sign_lord(sign: str) -> str:
    """Get ruling planet of a zodiac sign (duplicated from kundli.py)."""
    lords = {
        "Aries": "Mars",
        "Taurus": "Venus",
        "Gemini": "Mercury",
        "Cancer": "Moon",
        "Leo": "Sun",
        "Virgo": "Mercury",
        "Libra": "Venus",
        "Scorpio": "Mars",
        "Sagittarius": "Jupiter",
        "Capricorn": "Saturn",
        "Aquarius": "Saturn",
        "Pisces": "Jupiter",
    }
    return lords.get(sign, "Unknown")


def _get_nakshatra_lord_by_name(nakshatra: str) -> str:
    """Get nakshatra lord from nakshatra name using the standard 27-sequence."""
    if not nakshatra:
        return "Unknown"

    nakshatra_names = [
        "Ashwini",
        "Bharani",
        "Krittika",
        "Rohini",
        "Mrigashira",
        "Ardra",
        "Punarvasu",
        "Pushya",
        "Ashlesha",
        "Magha",
        "Purva Phalguni",
        "Uttara Phalguni",
        "Hasta",
        "Chitra",
        "Swati",
        "Vishakha",
        "Anuradha",
        "Jyeshtha",
        "Mula",
        "Purva Ashadha",
        "Uttara Ashadha",
        "Shravana",
        "Dhanishta",
        "Shatabhisha",
        "Purva Bhadrapada",
        "Uttara Bhadrapada",
        "Revati",
    ]

    try:
        index = nakshatra_names.index(nakshatra)
    except ValueError:
        return "Unknown"

    lords_cycle = ["Ketu", "Venus", "Sun", "Moon", "Mars", "Rahu", "Jupiter", "Saturn", "Mercury"]
    return lords_cycle[index % 9]


def _get_avastha(planet: str, sign: str) -> str:
    """Basic avastha label based on exaltation/own sign/debilitation."""
    exaltations = {
        "Sun": "Aries",
        "Moon": "Taurus",
        "Mars": "Capricorn",
        "Mercury": "Virgo",
        "Jupiter": "Cancer",
        "Venus": "Pisces",
        "Saturn": "Libra",
    }
    debilitations = {
        "Sun": "Libra",
        "Moon": "Scorpio",
        "Mars": "Cancer",
        "Mercury": "Pisces",
        "Jupiter": "Capricorn",
        "Venus": "Virgo",
        "Saturn": "Aries",
    }
    own_signs = {
        "Sun": ["Leo"],
        "Moon": ["Cancer"],
        "Mars": ["Aries", "Scorpio"],
        "Mercury": ["Gemini", "Virgo"],
        "Jupiter": ["Sagittarius", "Pisces"],
        "Venus": ["Taurus", "Libra"],
        "Saturn": ["Capricorn", "Aquarius"],
    }

    if exaltations.get(planet) == sign:
        return "Exalted"
    if debilitations.get(planet) == sign:
        return "Debilitated"
    if sign in own_signs.get(planet, []):
        return "Own Sign"
    return "Neutral"


def _extract_planet_details(chart):
    """Extract compact planet details for UI (sign, degree, nakshatra, house, lords, avastha)."""
    try:
        planets = chart.get("planets", {})
        planet_houses = chart.get("planet_houses", {})
        details = []

        for planet_name, planet_data in planets.items():
            longitude = float(planet_data.get("longitude", 0.0))
            sign = planet_data.get("sign")
            nakshatra = planet_data.get("nakshatra")

            details.append(
                {
                    "name": planet_name,
                    "sign": sign,
                    "signLord": _get_sign_lord(sign) if sign else None,
                    "degree": round(longitude % 30, 2),
                    "nakshatra": nakshatra,
                    "nakshatraLord": _get_nakshatra_lord_by_name(nakshatra) if nakshatra else None,
                    "house": planet_houses.get(planet_name),
                    "avastha": _get_avastha(planet_name, sign) if sign else None,
                }
            )

        # Add Ascendant as a pseudo-planet row for UI if available
        try:
            asc_long = chart.get("ascendant", {}).get("longitude")
            if asc_long is not None:
                asc_sign_num = int(asc_long / 30)
                asc_degree = round(asc_long % 30, 2)
                sign_names = [
                    "Aries",
                    "Taurus",
                    "Gemini",
                    "Cancer",
                    "Leo",
                    "Virgo",
                    "Libra",
                    "Scorpio",
                    "Sagittarius",
                    "Capricorn",
                    "Aquarius",
                    "Pisces",
                ]
                asc_sign = sign_names[asc_sign_num]

                # Compute Ascendant nakshatra name and lord
                nakshatra_span = 360 / 27
                nakshatra_num = int(asc_long / nakshatra_span)
                nakshatra_names = [
                    "Ashwini",
                    "Bharani",
                    "Krittika",
                    "Rohini",
                    "Mrigashira",
                    "Ardra",
                    "Punarvasu",
                    "Pushya",
                    "Ashlesha",
                    "Magha",
                    "Purva Phalguni",
                    "Uttara Phalguni",
                    "Hasta",
                    "Chitra",
                    "Swati",
                    "Vishakha",
                    "Anuradha",
                    "Jyeshtha",
                    "Mula",
                    "Purva Ashadha",
                    "Uttara Ashadha",
                    "Shravana",
                    "Dhanishta",
                    "Shatabhisha",
                    "Purva Bhadrapada",
                    "Uttara Bhadrapada",
                    "Revati",
                ]

                asc_nakshatra = nakshatra_names[nakshatra_num]

                details.append(
                    {
                        "name": "Ascendant",
                        "sign": asc_sign,
                        "signLord": _get_sign_lord(asc_sign),
                        "degree": asc_degree,
                        "nakshatra": asc_nakshatra,
                        "nakshatraLord": _get_nakshatra_lord_by_name(asc_nakshatra),
                        "house": 1,
                        "avastha": "Neutral",
                    }
                )
        except Exception:
            # Fail gracefully if ascendant data is missing or malformed
            pass

        return details
    except Exception:
        # In case of any unexpected shape, fail gracefully
        return []


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

        # Attach key Moon details so frontend can show Janam Rashi etc.
        # These live inside the ashtakoot JSON that the backend stores.
        matching["male_moon_sign"] = male_moon["sign"]
        matching["female_moon_sign"] = female_moon["sign"]
        matching["male_moon_nakshatra"] = male_moon["nakshatra"]
        matching["female_moon_nakshatra"] = female_moon["nakshatra"]
        
        # Also calculate Dashakoot (10-Kuta)
        dashakoot = dashakoot_matching.calculate_dashakoot_matching(
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

        # Prepare Lagna (D1) charts for both using divisional charts
        try:
            male_lagna_chart = divisional_charts.calculate_chart(male_chart['planets'], 'D1')
            female_lagna_chart = divisional_charts.calculate_chart(female_chart['planets'], 'D1')
        except Exception:
            male_lagna_chart = None
            female_lagna_chart = None

        # Ascendant details for both (for accurate Lagna chart rendering)
        def _get_ascendant_info(chart):
            try:
                asc_long = chart['ascendant']['longitude']
                sign_num = int(asc_long / 30)
                degree = round(asc_long % 30, 2)
                signs = [
                    'Aries', 'Taurus', 'Gemini', 'Cancer',
                    'Leo', 'Virgo', 'Libra', 'Scorpio',
                    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
                ]
                sign = signs[sign_num]
                return {
                    "sign": sign,
                    "sign_num": sign_num,
                    "degree": degree,
                }
            except Exception:
                return None

        male_ascendant = _get_ascendant_info(male_chart)
        female_ascendant = _get_ascendant_info(female_chart)
        
        return {
            "success": True,
            "male_name": male_data.name,
            "female_name": female_data.name,
            "ashtakoot_matching": matching,
            "dashakoot_matching": dashakoot,
            "male_mangal_dosha": male_mangal,
            "female_mangal_dosha": female_mangal,
            # Compact planet tables for UI (Planet Details tab)
            "male_planet_details": _extract_planet_details(male_chart),
            "female_planet_details": _extract_planet_details(female_chart),
            # Lagna (D1) charts and ascendant info for UI (Lagna Chart tab)
            "male_lagna_chart": male_lagna_chart,
            "female_lagna_chart": female_lagna_chart,
            "male_ascendant": male_ascendant,
            "female_ascendant": female_ascendant,
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
