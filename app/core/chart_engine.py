"""
Birth Chart calculation engine
"""
from datetime import datetime
from typing import Dict, Optional
from app.core.ephemeris import ephemeris


class ChartEngine:
    """Main chart calculation engine"""
    
    def __init__(self):
        self.ephemeris = ephemeris
    
    def calculate_birth_chart(
        self,
        date: datetime,
        latitude: float,
        longitude: float,
        timezone: str,
        house_system: str = 'PLACIDUS'
    ) -> Dict:
        """
        Calculate complete birth chart
        
        Args:
            date: Birth date and time
            latitude: Birth place latitude
            longitude: Birth place longitude
            timezone: Timezone string (e.g., 'Asia/Kolkata')
            house_system: House system to use
            
        Returns:
            Complete birth chart data
        """
        # Get Julian Day
        jd = self.ephemeris.get_julian_day(date, timezone)
        
        # Calculate planetary positions
        planets = self.ephemeris.get_all_planets(jd)
        
        # Calculate houses
        houses = self.ephemeris.get_houses(jd, latitude, longitude, house_system)
        
        # Get ayanamsa
        ayanamsa = self.ephemeris.get_ayanamsa(jd)
        
        # Calculate ascendant sign
        asc_longitude = houses['ascendant']
        asc_sign_num = int(asc_longitude / 30)
        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer',
            'Leo', 'Virgo', 'Libra', 'Scorpio',
            'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        asc_sign = signs[asc_sign_num]
        
        # Determine planet house positions
        planet_houses = self._determine_planet_houses(planets, houses['cusps'])
        
        # Calculate planetary strengths (Shadbala)
        strengths = self._calculate_shadbala(planets, houses, jd)
        
        # Determine planetary relationships
        relationships = self._calculate_relationships(planets, houses['cusps'])
        
        return {
            'birth_details': {
                'date': date.isoformat(),
                'latitude': latitude,
                'longitude': longitude,
                'timezone': timezone,
                'julian_day': round(jd, 6),
                'ayanamsa': round(ayanamsa, 6)
            },
            'ascendant': {
                'longitude': houses['ascendant'],
                'sign': asc_sign,
                'degree': round(asc_longitude % 30, 6)
            },
            'planets': planets,
            'planet_houses': planet_houses,
            'houses': houses,
            'strengths': strengths,
            'relationships': relationships
        }
    
    def _determine_planet_houses(
        self, 
        planets: Dict, 
        cusps: list
    ) -> Dict[str, int]:
        """Determine which house each planet is in"""
        planet_houses = {}
        
        for planet_name, planet_data in planets.items():
            planet_long = planet_data['longitude']
            
            # Find the house
            house_num = 1
            for i in range(12):
                next_i = (i + 1) % 12
                cusp = cusps[i]
                next_cusp = cusps[next_i]
                
                # Handle zodiac wrap-around
                if cusp > next_cusp:
                    if planet_long >= cusp or planet_long < next_cusp:
                        house_num = i + 1
                        break
                else:
                    if cusp <= planet_long < next_cusp:
                        house_num = i + 1
                        break
            
            planet_houses[planet_name] = house_num
        
        return planet_houses
    
    def _calculate_shadbala(
        self, 
        planets: Dict, 
        houses: Dict, 
        jd: float
    ) -> Dict:
        """
        Calculate Shadbala (six-fold strength) for planets
        Simplified version - full implementation would be more complex
        """
        strengths = {}
        
        for planet_name in planets.keys():
            if planet_name in ['Rahu', 'Ketu']:
                continue  # Nodes don't have Shadbala
            
            planet_data = planets[planet_name]
            
            # Positional strength (based on sign)
            positional = self._get_positional_strength(planet_name, planet_data)
            
            # Directional strength (based on house position)
            directional = self._get_directional_strength(planet_name, planet_data, houses)
            
            # Temporal strength (day/night)
            temporal = 60  # Simplified
            
            # Motional strength (speed)
            motional = 0 if planet_data.get('is_retrograde') else 60
            
            # Natural strength (inherent)
            natural = self._get_natural_strength(planet_name)
            
            # Aspectual strength (aspects from other planets)
            aspectual = 60  # Simplified
            
            total = positional + directional + temporal + motional + natural + aspectual
            
            strengths[planet_name] = {
                'positional': round(positional, 2),
                'directional': round(directional, 2),
                'temporal': round(temporal, 2),
                'motional': round(motional, 2),
                'natural': round(natural, 2),
                'aspectual': round(aspectual, 2),
                'total': round(total, 2),
                'percentage': round((total / 390) * 100, 2)  # Max possible is 390
            }
        
        return strengths
    
    def _get_positional_strength(self, planet: str, data: Dict) -> float:
        """Get positional strength based on exaltation, own sign, etc."""
        sign_num = data['sign_num']
        degree = data['sign_degree']
        
        # Exaltation signs and degrees
        exaltation = {
            'Sun': (0, 10),      # Aries 10°
            'Moon': (1, 3),      # Taurus 3°
            'Mars': (9, 28),     # Capricorn 28°
            'Mercury': (5, 15),  # Virgo 15°
            'Jupiter': (3, 5),   # Cancer 5°
            'Venus': (11, 27),   # Pisces 27°
            'Saturn': (6, 20)    # Libra 20°
        }
        
        if planet in exaltation:
            exalt_sign, exalt_degree = exaltation[planet]
            if sign_num == exalt_sign:
                # Maximum at exact exaltation degree
                diff = abs(degree - exalt_degree)
                return 60 - (diff * 2)  # Decreases as we move away
        
        # Own sign strength
        own_signs = {
            'Sun': [4],           # Leo
            'Moon': [3],          # Cancer
            'Mars': [0, 7],       # Aries, Scorpio
            'Mercury': [2, 5],    # Gemini, Virgo
            'Jupiter': [8, 11],   # Sagittarius, Pisces
            'Venus': [1, 6],      # Taurus, Libra
            'Saturn': [9, 10]     # Capricorn, Aquarius
        }
        
        if planet in own_signs and sign_num in own_signs[planet]:
            return 45
        
        return 30  # Neutral
    
    def _get_directional_strength(
        self, 
        planet: str, 
        data: Dict, 
        houses: Dict
    ) -> float:
        """Get directional strength (Dig Bala)"""
        planet_long = data['longitude']
        
        # Best directions for planets
        best_positions = {
            'Sun': houses['mc'],           # 10th house (south)
            'Moon': houses['cusps'][3],    # 4th house (north)
            'Mars': houses['mc'],          # 10th house (south)
            'Mercury': houses['ascendant'], # 1st house (east)
            'Jupiter': houses['ascendant'], # 1st house (east)
            'Venus': houses['cusps'][3],   # 4th house (north)
            'Saturn': houses['cusps'][6]   # 7th house (west)
        }
        
        if planet in best_positions:
            best_pos = best_positions[planet]
            diff = abs(planet_long - best_pos)
            if diff > 180:
                diff = 360 - diff
            
            # Maximum strength at exact position
            return max(0, 60 - (diff / 3))
        
        return 30
    
    def _get_natural_strength(self, planet: str) -> float:
        """Get natural strength (Naisargika Bala)"""
        natural_strengths = {
            'Sun': 60,
            'Moon': 51.43,
            'Venus': 42.86,
            'Jupiter': 34.29,
            'Mercury': 25.71,
            'Mars': 17.14,
            'Saturn': 8.57
        }
        
        return natural_strengths.get(planet, 30)
    
    def _calculate_relationships(
        self, 
        planets: Dict, 
        cusps: list
    ) -> Dict:
        """Calculate planetary relationships (aspects, conjunctions, etc.)"""
        relationships = {
            'conjunctions': [],
            'oppositions': [],
            'trines': [],
            'squares': [],
            'sextiles': []
        }
        
        planet_list = [p for p in planets.keys() if p not in ['Rahu', 'Ketu']]
        
        for i, planet1 in enumerate(planet_list):
            for planet2 in planet_list[i+1:]:
                long1 = planets[planet1]['longitude']
                long2 = planets[planet2]['longitude']
                
                diff = abs(long1 - long2)
                if diff > 180:
                    diff = 360 - diff
                
                orb = 8  # Orb of influence
                
                if diff <= orb:  # Conjunction
                    relationships['conjunctions'].append({
                        'planet1': planet1,
                        'planet2': planet2,
                        'angle': round(diff, 2)
                    })
                elif abs(diff - 180) <= orb:  # Opposition
                    relationships['oppositions'].append({
                        'planet1': planet1,
                        'planet2': planet2,
                        'angle': round(diff, 2)
                    })
                elif abs(diff - 120) <= orb:  # Trine
                    relationships['trines'].append({
                        'planet1': planet1,
                        'planet2': planet2,
                        'angle': round(diff, 2)
                    })
                elif abs(diff - 90) <= orb:  # Square
                    relationships['squares'].append({
                        'planet1': planet1,
                        'planet2': planet2,
                        'angle': round(diff, 2)
                    })
                elif abs(diff - 60) <= orb:  # Sextile
                    relationships['sextiles'].append({
                        'planet1': planet1,
                        'planet2': planet2,
                        'angle': round(diff, 2)
                    })
        
        return relationships


# Global chart engine instance
chart_engine = ChartEngine()
