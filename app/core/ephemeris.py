"""
Swiss Ephemeris wrapper for astronomical calculations
"""
import swisseph as swe
from datetime import datetime
from typing import Dict, List, Tuple, Optional
import pytz
from app.config import settings


class SwissEphemeris:
    """Wrapper for Swiss Ephemeris library"""
    
    # Planet constants
    PLANETS = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mars': swe.MARS,
        'Mercury': swe.MERCURY,
        'Jupiter': swe.JUPITER,
        'Venus': swe.VENUS,
        'Saturn': swe.SATURN,
        'Rahu': swe.MEAN_NODE,  # North Node
        'Ketu': swe.MEAN_NODE,  # Will calculate as 180° opposite
        'Uranus': swe.URANUS,
        'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO,
    }
    
    # Ayanamsa types
    AYANAMSA_TYPES = {
        'LAHIRI': swe.SIDM_LAHIRI,
        'RAMAN': swe.SIDM_RAMAN,
        'KP': swe.SIDM_KRISHNAMURTI,
        'FAGAN_BRADLEY': swe.SIDM_FAGAN_BRADLEY,
    }
    
    # House systems
    HOUSE_SYSTEMS = {
        'PLACIDUS': 'P',
        'KOCH': 'K',
        'EQUAL': 'E',
        'WHOLE_SIGN': 'W',
        'CAMPANUS': 'C',
        'REGIOMONTANUS': 'R',
    }
    
    def __init__(self):
        """Initialize Swiss Ephemeris"""
        # Set ephemeris path
        swe.set_ephe_path(settings.EPHEMERIS_PATH)
        
        # Set ayanamsa
        ayanamsa_type = self.AYANAMSA_TYPES.get(
            settings.AYANAMSA, 
            swe.SIDM_LAHIRI
        )
        swe.set_sid_mode(ayanamsa_type)
    
    def get_julian_day(
        self, 
        dt: datetime, 
        timezone: str = None
    ) -> float:
        """Convert datetime to Julian Day (UT)"""
        if timezone:
            tz = pytz.timezone(timezone)
            dt = tz.localize(dt) if dt.tzinfo is None else dt
            dt = dt.astimezone(pytz.UTC)
        
        jd = swe.julday(
            dt.year, 
            dt.month, 
            dt.day,
            dt.hour + dt.minute/60.0 + dt.second/3600.0
        )
        return jd
    
    def get_planet_position(
        self, 
        planet: str, 
        jd: float,
        flags: int = swe.FLG_SWIEPH | swe.FLG_SIDEREAL
    ) -> Dict:
        """Get planet position in sidereal zodiac"""
        planet_id = self.PLANETS.get(planet)
        
        if planet_id is None:
            raise ValueError(f"Unknown planet: {planet}")
        
        # Calculate position
        result = swe.calc_ut(jd, planet_id, flags)
        longitude = result[0][0]
        
        # For Ketu, add 180 degrees to Rahu
        if planet == 'Ketu':
            longitude = (longitude + 180) % 360
        
        # Calculate degrees, minutes, seconds
        degrees = int(longitude)
        minutes = int((longitude - degrees) * 60)
        seconds = ((longitude - degrees) * 60 - minutes) * 60
        
        # Get sign and sign position
        sign_num = int(longitude / 30)
        sign_degree = longitude % 30
        
        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer',
            'Leo', 'Virgo', 'Libra', 'Scorpio',
            'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        # Get nakshatra
        nakshatra_num = int(longitude / 13.333333333333334)
        nakshatra_pada = int((longitude % 13.333333333333334) / 3.333333333333333) + 1
        
        nakshatras = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
            'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 
            'Uttara Phalguni', 'Hasta', 'Chitra', 'Swati', 'Vishakha',
            'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha', 'Uttara Ashadha',
            'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
            'Uttara Bhadrapada', 'Revati'
        ]
        
        return {
            'planet': planet,
            'longitude': round(longitude, 6),
            'sign': signs[sign_num],
            'sign_num': sign_num,
            'sign_degree': round(sign_degree, 6),
            'degrees': degrees,
            'minutes': minutes,
            'seconds': round(seconds, 2),
            'nakshatra': nakshatras[nakshatra_num],
            'nakshatra_num': nakshatra_num,
            'nakshatra_pada': nakshatra_pada,
            'is_retrograde': result[0][3] < 0 if len(result[0]) > 3 else False
        }
    
    def get_all_planets(self, jd: float) -> Dict[str, Dict]:
        """Get positions of all major planets"""
        planets_to_calc = [
            'Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter',
            'Venus', 'Saturn', 'Rahu', 'Ketu'
        ]
        
        positions = {}
        for planet in planets_to_calc:
            positions[planet] = self.get_planet_position(planet, jd)
        
        return positions
    
    def get_houses(
        self, 
        jd: float, 
        latitude: float, 
        longitude: float,
        house_system: str = 'PLACIDUS'
    ) -> Dict:
        """Calculate house cusps and angles"""
        hsys = self.HOUSE_SYSTEMS.get(house_system, 'P')
        
        # Calculate houses
        houses, ascmc = swe.houses(jd, latitude, longitude, hsys.encode())
        
        # Convert to list (houses is a tuple)
        house_cusps = list(houses)
        
        return {
            'cusps': [round(cusp, 6) for cusp in house_cusps],
            'ascendant': round(ascmc[0], 6),
            'mc': round(ascmc[1], 6),  # Midheaven
            'armc': round(ascmc[2], 6),  # Right Ascension of MC
            'vertex': round(ascmc[3], 6),
            'equatorial_ascendant': round(ascmc[4], 6),
            'co_ascendant_koch': round(ascmc[5], 6),
            'polar_ascendant': round(ascmc[6], 6),
            'house_system': house_system
        }
    
    def get_ayanamsa(self, jd: float) -> float:
        """Get ayanamsa value for given Julian Day"""
        return swe.get_ayanamsa_ut(jd)
    
    def close(self):
        """Close Swiss Ephemeris"""
        swe.close()


# Global ephemeris instance
ephemeris = SwissEphemeris()
