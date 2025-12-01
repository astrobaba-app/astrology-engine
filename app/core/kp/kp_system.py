"""
KP System Calculator
"""
from typing import Dict, List, Tuple
from app.core.ephemeris import ephemeris


class KPSystem:
    """Krishnamurti Paddhati (KP) System calculations"""
    
    # KP Ayanamsa constant (different from Lahiri)
    KP_AYANAMSA_OFFSET = 0.0  # KP uses its own ayanamsa
    
    # Nakshatra lords in KP system
    NAKSHATRA_LORDS = [
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars',
        'Rahu', 'Jupiter', 'Saturn', 'Mercury'
    ]
    
    # Sub-lord divisions (unequal divisions based on Vimshottari periods)
    SUB_LORD_PERIODS = {
        'Ketu': 7,
        'Venus': 20,
        'Sun': 6,
        'Moon': 10,
        'Mars': 7,
        'Rahu': 18,
        'Jupiter': 16,
        'Saturn': 19,
        'Mercury': 17
    }
    
    # Total of all periods
    TOTAL_PERIOD = 120
    
    def get_star_lord(self, longitude: float) -> str:
        """
        Get the star lord (Nakshatra lord) for a given longitude
        
        Args:
            longitude: Longitude in degrees (0-360)
            
        Returns:
            Star lord name
        """
        nakshatra_num = int(longitude / 13.333333333333334)
        star_lord = self.NAKSHATRA_LORDS[nakshatra_num % 9]
        return star_lord
    
    def get_sub_lord(self, longitude: float) -> str:
        """
        Get the sub-lord for a given longitude
        
        Args:
            longitude: Longitude in degrees (0-360)
            
        Returns:
            Sub-lord name
        """
        # Get position within nakshatra (0-13.333...)
        nakshatra_position = longitude % 13.333333333333334
        
        # Get nakshatra number to determine starting sub-lord
        nakshatra_num = int(longitude / 13.333333333333334)
        start_lord_index = nakshatra_num % 9
        
        # Calculate proportional position in sub-divisions
        # Each nakshatra is divided proportionally based on Vimshottari periods
        proportion = nakshatra_position / 13.333333333333334
        
        # Calculate which sub-lord based on proportional periods
        cumulative = 0
        for i in range(9):
            lord_index = (start_lord_index + i) % 9
            lord = self.NAKSHATRA_LORDS[lord_index]
            lord_period = self.SUB_LORD_PERIODS[lord]
            lord_proportion = lord_period / self.TOTAL_PERIOD
            
            if proportion < cumulative + lord_proportion:
                return lord
            
            cumulative += lord_proportion
        
        # Fallback (should not reach here)
        return self.NAKSHATRA_LORDS[start_lord_index]
    
    def get_sub_sub_lord(self, longitude: float) -> str:
        """
        Get the sub-sub-lord for a given longitude
        
        Args:
            longitude: Longitude in degrees (0-360)
            
        Returns:
            Sub-sub-lord name
        """
        # Get position within nakshatra
        nakshatra_position = longitude % 13.333333333333334
        nakshatra_num = int(longitude / 13.333333333333334)
        start_lord_index = nakshatra_num % 9
        
        # First find which sub-lord we're in
        proportion = nakshatra_position / 13.333333333333334
        
        cumulative = 0
        sub_lord = None
        sub_lord_start = 0
        sub_lord_proportion = 0
        
        for i in range(9):
            lord_index = (start_lord_index + i) % 9
            lord = self.NAKSHATRA_LORDS[lord_index]
            lord_period = self.SUB_LORD_PERIODS[lord]
            lord_proportion = lord_period / self.TOTAL_PERIOD
            
            if proportion < cumulative + lord_proportion:
                sub_lord = lord
                sub_lord_start = cumulative
                sub_lord_proportion = lord_proportion
                break
            
            cumulative += lord_proportion
        
        # Now divide the sub-lord further
        if sub_lord:
            position_in_sub = (proportion - sub_lord_start) / sub_lord_proportion
            
            # Find sub-sub-lord
            sub_lord_index = self.NAKSHATRA_LORDS.index(sub_lord)
            cumulative_sub = 0
            
            for i in range(9):
                lord_index = (sub_lord_index + i) % 9
                lord = self.NAKSHATRA_LORDS[lord_index]
                lord_period = self.SUB_LORD_PERIODS[lord]
                lord_proportion = lord_period / self.TOTAL_PERIOD
                
                if position_in_sub < cumulative_sub + lord_proportion:
                    return lord
                
                cumulative_sub += lord_proportion
        
        return self.NAKSHATRA_LORDS[start_lord_index]
    
    def calculate_cuspal_positions(
        self,
        houses: Dict
    ) -> List[Dict]:
        """
        Calculate KP cuspal positions with star lord and sub-lord
        
        Args:
            houses: House cusps from chart calculation
            
        Returns:
            List of cusp details with KP significators
        """
        cusps = []
        
        for i, cusp_longitude in enumerate(houses['cusps']):
            house_num = i + 1
            
            # Calculate sign
            sign_num = int(cusp_longitude / 30)
            signs = [
                'Aries', 'Taurus', 'Gemini', 'Cancer',
                'Leo', 'Virgo', 'Libra', 'Scorpio',
                'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
            ]
            
            # Get KP significators
            star_lord = self.get_star_lord(cusp_longitude)
            sub_lord = self.get_sub_lord(cusp_longitude)
            sub_sub_lord = self.get_sub_sub_lord(cusp_longitude)
            
            cusps.append({
                'house': house_num,
                'longitude': round(cusp_longitude, 6),
                'sign': signs[sign_num],
                'degree': round(cusp_longitude % 30, 6),
                'star_lord': star_lord,
                'sub_lord': sub_lord,
                'sub_sub_lord': sub_sub_lord
            })
        
        return cusps
    
    def calculate_planet_significators(
        self,
        planets: Dict
    ) -> Dict[str, Dict]:
        """
        Calculate KP significators for all planets
        
        Args:
            planets: Planet positions
            
        Returns:
            Dictionary of planet significators
        """
        planet_significators = {}
        
        for planet_name, planet_data in planets.items():
            longitude = planet_data['longitude']
            
            # Get significators
            star_lord = self.get_star_lord(longitude)
            sub_lord = self.get_sub_lord(longitude)
            sub_sub_lord = self.get_sub_sub_lord(longitude)
            
            planet_significators[planet_name] = {
                'longitude': longitude,
                'sign': planet_data['sign'],
                'degree': planet_data['sign_degree'],
                'nakshatra': planet_data['nakshatra'],
                'star_lord': star_lord,
                'sub_lord': sub_lord,
                'sub_sub_lord': sub_sub_lord,
                'is_retrograde': planet_data.get('is_retrograde', False)
            }
        
        return planet_significators
    
    def get_ruling_planets(
        self,
        query_time_jd: float,
        latitude: float,
        longitude: float
    ) -> Dict:
        """
        Calculate ruling planets at the time of query (KP Horary)
        
        Args:
            query_time_jd: Julian day of query
            latitude: Query location latitude
            longitude: Query location longitude
            
        Returns:
            Ruling planets
        """
        # Get ascendant at query time
        houses = ephemeris.get_houses(query_time_jd, latitude, longitude, 'PLACIDUS')
        asc_longitude = houses['ascendant']
        
        # Get Moon position
        moon = ephemeris.get_planet_position('Moon', query_time_jd)
        moon_longitude = moon['longitude']
        
        # Calculate day lord (weekday ruler)
        # This would need the actual datetime, simplified here
        day_lords = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        day_lord = day_lords[0]  # Placeholder
        
        # Ascendant significators
        asc_star_lord = self.get_star_lord(asc_longitude)
        asc_sub_lord = self.get_sub_lord(asc_longitude)
        
        # Moon significators
        moon_star_lord = self.get_star_lord(moon_longitude)
        moon_sub_lord = self.get_sub_lord(moon_longitude)
        
        return {
            'ascendant': {
                'longitude': asc_longitude,
                'star_lord': asc_star_lord,
                'sub_lord': asc_sub_lord
            },
            'moon': {
                'longitude': moon_longitude,
                'star_lord': moon_star_lord,
                'sub_lord': moon_sub_lord
            },
            'day_lord': day_lord,
            'ruling_planets': [
                day_lord,
                asc_star_lord,
                asc_sub_lord,
                moon_star_lord,
                moon_sub_lord
            ]
        }
    
    def analyze_house_significators(
        self,
        house_num: int,
        cusps: List[Dict],
        planets: Dict,
        planet_houses: Dict
    ) -> Dict:
        """
        Analyze significators for a specific house in KP system
        
        Args:
            house_num: House number (1-12)
            cusps: Cuspal positions
            planets: Planet positions
            planet_houses: Which house each planet is in
            
        Returns:
            House significator analysis
        """
        # Get cusp sub-lord
        cusp = cusps[house_num - 1]
        cusp_sub_lord = cusp['sub_lord']
        
        # Get planets in the house
        planets_in_house = [p for p, h in planet_houses.items() if h == house_num]
        
        # Get star lords of planets in house
        star_lords_in_house = []
        for planet in planets_in_house:
            star_lord = self.get_star_lord(planets[planet]['longitude'])
            star_lords_in_house.append(star_lord)
        
        # Planets in star of cusp sub-lord
        planets_in_star = []
        for planet_name, planet_data in planets.items():
            if self.get_star_lord(planet_data['longitude']) == cusp_sub_lord:
                planets_in_star.append(planet_name)
        
        return {
            'house': house_num,
            'cusp_sub_lord': cusp_sub_lord,
            'planets_in_house': planets_in_house,
            'star_lords_in_house': list(set(star_lords_in_house)),
            'planets_in_star_of_sub_lord': planets_in_star,
            'primary_significator': cusp_sub_lord,
            'matters': self._get_house_matters(house_num)
        }
    
    def _get_house_matters(self, house_num: int) -> str:
        """Get the matters signified by a house"""
        house_matters = {
            1: 'Self, personality, health, appearance',
            2: 'Wealth, family, speech, food',
            3: 'Siblings, courage, short travels, communication',
            4: 'Mother, home, property, vehicles, happiness',
            5: 'Children, education, speculation, romance',
            6: 'Enemies, diseases, debts, service',
            7: 'Marriage, partnership, spouse, business',
            8: 'Longevity, inheritance, sudden events, occult',
            9: 'Father, fortune, higher education, spirituality',
            10: 'Career, profession, status, authority',
            11: 'Gains, income, friends, desires',
            12: 'Losses, expenses, foreign lands, moksha'
        }
        return house_matters.get(house_num, '')
    
    def calculate_kp_chart(
        self,
        planets: Dict,
        houses: Dict,
        planet_houses: Dict
    ) -> Dict:
        """
        Calculate complete KP chart analysis
        
        Args:
            planets: Planet positions
            houses: House cusps
            planet_houses: Planet house positions
            
        Returns:
            Complete KP chart data
        """
        # Calculate cuspal positions
        cusps = self.calculate_cuspal_positions(houses)
        
        # Calculate planet significators
        planet_significators = self.calculate_planet_significators(planets)
        
        # Analyze all houses
        house_analyses = []
        for i in range(1, 13):
            analysis = self.analyze_house_significators(
                i, cusps, planets, planet_houses
            )
            house_analyses.append(analysis)
        
        return {
            'system': 'Krishnamurti Paddhati (KP)',
            'cusps': cusps,
            'planet_significators': planet_significators,
            'house_analyses': house_analyses
        }


# Global instance
kp_system = KPSystem()
