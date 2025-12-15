"""Yoga and Dosha Calculator"""
from typing import Dict, List, Set
from datetime import datetime, timedelta


class YogaDoshaCalculator:
    """Calculate Yogas (auspicious combinations) and Doshas (afflictions)"""
    
    def detect_raj_yogas(self, planets: Dict, planet_houses: Dict, houses: Dict) -> List[Dict]:
        """
        Detect Raj Yogas (combinations for power and prosperity)
        
        Args:
            planets: Planet positions
            planet_houses: Which house each planet is in
            houses: House cusps
            
        Returns:
            List of detected Raj Yogas
        """
        yogas = []
        
        # Get lords of houses (simplified - should use ascendant for accuracy)
        # For now, using generic lordships
        
        # Yoga 1: Lords of 1st and 9th in conjunction
        # Yoga 2: Lords of 4th and 5th in conjunction
        # Yoga 3: Lords of 9th and 10th in conjunction (most powerful)
        
        # Check for conjunctions (planets in same house)
        house_occupants = {}
        for planet, house in planet_houses.items():
            if house not in house_occupants:
                house_occupants[house] = []
            house_occupants[house].append(planet)
        
        # Kendra houses: 1, 4, 7, 10
        kendras = [1, 4, 7, 10]
        
        # Trikona houses: 1, 5, 9
        trikonas = [1, 5, 9]
        
        # Check for planets in Kendra and Trikona
        for planet in ['Jupiter', 'Venus', 'Mercury']:
            house = planet_houses.get(planet)
            if house in kendras:
                yogas.append({
                    'name': f'{planet} in Kendra (House {house})',
                    'type': 'Raj Yoga',
                    'strength': 'Medium',
                    'description': f'{planet} in angular house gives strength and stability',
                    'planets': [planet]
                })
            
            if house in trikonas:
                yogas.append({
                    'name': f'{planet} in Trikona (House {house})',
                    'type': 'Raj Yoga',
                    'strength': 'High',
                    'description': f'{planet} in trinal house gives fortune and dharma',
                    'planets': [planet]
                })
        
        # Check for Gaja Kesari Yoga (Jupiter and Moon in Kendra)
        jupiter_house = planet_houses.get('Jupiter')
        moon_house = planet_houses.get('Moon')
        
        if jupiter_house and moon_house:
            house_diff = abs(jupiter_house - moon_house)
            if house_diff in [0, 3, 6, 9]:  # Same or 4th/7th/10th from each other
                yogas.append({
                    'name': 'Gaja Kesari Yoga',
                    'type': 'Raj Yoga',
                    'strength': 'Very High',
                    'description': 'Jupiter and Moon in Kendra - gives wisdom, wealth, and fame',
                    'planets': ['Jupiter', 'Moon']
                })
        
        # Check for Dhana Yoga (wealth combinations)
        # Lords of 2nd, 5th, 9th, 11th in conjunction or mutual aspect
        
        return yogas
    
    def detect_dhana_yogas(self, planets: Dict, planet_houses: Dict) -> List[Dict]:
        """
        Detect Dhana Yogas (wealth combinations)
        
        Args:
            planets: Planet positions
            planet_houses: Which house each planet is in
            
        Returns:
            List of detected Dhana Yogas
        """
        yogas = []
        
        # Wealth houses: 2, 5, 9, 11
        wealth_houses = [2, 5, 9, 11]
        
        # Check for benefics in wealth houses
        benefics = ['Jupiter', 'Venus', 'Mercury']
        
        for planet in benefics:
            house = planet_houses.get(planet)
            if house in wealth_houses:
                yogas.append({
                    'name': f'{planet} in {house}th House',
                    'type': 'Dhana Yoga',
                    'strength': 'Medium',
                    'description': f'{planet} in wealth house indicates financial gains',
                    'planets': [planet]
                })
        
        # Check for multiple planets in 11th house (gains)
        eleventh_house_planets = [p for p, h in planet_houses.items() if h == 11]
        if len(eleventh_house_planets) >= 2:
            yogas.append({
                'name': 'Multiple Planets in 11th House',
                'type': 'Dhana Yoga',
                'strength': 'High',
                'description': 'Multiple planets in house of gains indicate wealth accumulation',
                'planets': eleventh_house_planets
            })
        
        return yogas
    
    def detect_mahapurusha_yogas(self, planets: Dict, planet_houses: Dict, houses: Dict) -> List[Dict]:
        """
        Detect Mahapurusha Yogas (great personality yogas)
        Formed when Mars, Mercury, Jupiter, Venus, or Saturn are in Kendra in own/exaltation sign
        
        Args:
            planets: Planet positions
            planet_houses: Which house each planet is in
            houses: House cusps
            
        Returns:
            List of Mahapurusha Yogas
        """
        yogas = []
        
        # Kendra houses
        kendras = [1, 4, 7, 10]
        
        # Check each planet
        mahapurusha_planets = {
            'Mars': {'yoga_name': 'Ruchaka Yoga', 'own_signs': ['Aries', 'Scorpio'], 
                    'exaltation': 'Capricorn', 'quality': 'Courage and leadership'},
            'Mercury': {'yoga_name': 'Bhadra Yoga', 'own_signs': ['Gemini', 'Virgo'],
                       'exaltation': 'Virgo', 'quality': 'Intelligence and communication'},
            'Jupiter': {'yoga_name': 'Hamsa Yoga', 'own_signs': ['Sagittarius', 'Pisces'],
                       'exaltation': 'Cancer', 'quality': 'Wisdom and spirituality'},
            'Venus': {'yoga_name': 'Malavya Yoga', 'own_signs': ['Taurus', 'Libra'],
                     'exaltation': 'Pisces', 'quality': 'Beauty and luxury'},
            'Saturn': {'yoga_name': 'Sasha Yoga', 'own_signs': ['Capricorn', 'Aquarius'],
                      'exaltation': 'Libra', 'quality': 'Discipline and longevity'}
        }
        
        for planet_name, info in mahapurusha_planets.items():
            house = planet_houses.get(planet_name)
            if house in kendras:
                planet_sign = planets[planet_name]['sign']
                if planet_sign in info['own_signs'] or planet_sign == info['exaltation']:
                    yogas.append({
                        'name': info['yoga_name'],
                        'type': 'Mahapurusha Yoga',
                        'strength': 'Very High',
                        'description': f'{planet_name} in Kendra in own/exaltation sign - {info["quality"]}',
                        'planets': [planet_name],
                        'house': house
                    })
        
        return yogas
    
    def detect_kaal_sarp_dosha(self, planets: Dict) -> Dict:
        """
        Detect Kaal Sarp Dosha (all planets between Rahu and Ketu)
        
        Args:
            planets: Planet positions
            
        Returns:
            Kaal Sarp Dosha information
        """
        rahu_long = planets['Rahu']['longitude']
        ketu_long = planets['Ketu']['longitude']
        
        # Check if all planets are between Rahu and Ketu
        planets_to_check = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']
        
        all_between = True
        
        for planet in planets_to_check:
            planet_long = planets[planet]['longitude']
            
            # Check if planet is in the hemisphere from Rahu to Ketu
            if rahu_long < ketu_long:
                # Normal case
                if not (rahu_long <= planet_long <= ketu_long):
                    all_between = False
                    break
            else:
                # Wrapped case
                if not (planet_long >= rahu_long or planet_long <= ketu_long):
                    all_between = False
                    break
        
        if all_between:
            return {
                'present': True,
                'type': 'Full Kaal Sarp Dosha',
                'severity': 'High',
                'description': 'All planets are hemmed between Rahu and Ketu',
                'effects': 'Obstacles, delays, mental anxiety',
                'remedies': [
                    'Worship Lord Shiva',
                    'Chant Maha Mrityunjaya Mantra',
                    'Visit Kaal Sarp Dosha temples',
                    'Donate on Saturdays'
                ]
            }
        else:
            return {
                'present': False,
                'description': 'Kaal Sarp Dosha not present'
            }
    
    def detect_mangal_dosha(self, planets: Dict, planet_houses: Dict) -> Dict:
        """
        Detect Mangal Dosha (Mars affliction for marriage)
        Mars in 1st, 2nd, 4th, 7th, 8th, or 12th house
        
        Args:
            planets: Planet positions
            planet_houses: Which house each planet is in
            
        Returns:
            Mangal Dosha information
        """
        def _ordinal(n: int) -> str:
            suffix = "th"
            if not isinstance(n, int):
                return str(n)
            if 11 <= n % 100 <= 13:
                suffix = "th"
            else:
                suffix = {1: "st", 2: "nd", 3: "rd"}.get(n % 10, "th")
            return f"{n}{suffix}"

        mars_house = planet_houses.get('Mars')
        dosha_houses = [1, 2, 4, 7, 8, 12]

        if mars_house in dosha_houses:
            # Check severity
            if mars_house in [1, 7, 8]:
                severity = 'High'
            elif mars_house in [2, 12]:
                severity = 'Medium'
            else:
                severity = 'Low'
            
            # Check for cancellations
            cancellations = []
            
            # Cancellation 1: Mars in own sign (Aries/Scorpio) or exaltation (Capricorn)
            mars_sign = planets['Mars']['sign']
            if mars_sign in ['Aries', 'Scorpio', 'Capricorn']:
                cancellations.append('Mars in own/exaltation sign')
            
            # Cancellation 2: Jupiter aspecting Mars or 7th house
            jupiter_house = planet_houses.get('Jupiter')
            if jupiter_house:
                aspect_houses = [(jupiter_house + 4) % 12, (jupiter_house + 6) % 12, (jupiter_house + 8) % 12]
                if mars_house in aspect_houses or 7 in aspect_houses:
                    cancellations.append('Jupiter aspect on Mars or 7th house')

            # Build structured info for UI (for Lagna Chart "Based on Aspects/house")
            # Mars standard aspects: 4th, 7th, and 8th from its own position
            def _house_from(base: int, offset: int) -> int:
                # houses are 1-12 cyclic
                return ((base - 1 + offset) % 12) + 1

            mars_aspect_houses = [
                _house_from(mars_house, 3),  # 4th from Mars
                _house_from(mars_house, 6),  # 7th from Mars
                _house_from(mars_house, 7),  # 8th from Mars
            ]

            aspects = []
            for h in mars_aspect_houses:
                label = _ordinal(h)
                if h == 7:
                    aspects.append(f"Mars aspects {label} house (marriage / partnership house)")
                else:
                    aspects.append(f"Mars aspects {label} house")

            houses_info = [
                f"Mars in {_ordinal(mars_house)} house (Mangal house)"
            ]

            return {
                'present': True,
                'mars_house': mars_house,
                'severity': severity,
                'description': f'Mars in {mars_house}th house causes Mangal Dosha',
                'effects': 'Delays or problems in marriage, conflicts with spouse',
                'cancellations': cancellations,
                'is_cancelled': len(cancellations) > 0,
                # New structured lists for UI consumption
                'aspects': aspects,
                'houses': houses_info,
                'remedies': [
                    'Marry another Manglik person',
                    'Worship Lord Hanuman on Tuesdays',
                    'Chant Hanuman Chalisa',
                    'Wear red coral gemstone',
                    'Fast on Tuesdays'
                ]
            }
        else:
            # When Mars is not in a classical Mangal house, still
            # provide positive, structured info so the UI never
            # shows empty bullets.
            houses_info: List[str] = []
            aspects: List[str] = []

            if mars_house:
                houses_info.append(
                    f"Mars in {_ordinal(mars_house)} house (not a classical Mangal house)"
                )
                aspects.append(
                    "Mars does not strongly afflict key marriage houses (1st, 2nd, 4th, 7th, 8th, 12th)"
                )
            else:
                houses_info.append("Mars house position not available in chart data")
                aspects.append("Mars placement data is incomplete, Mangal Dosha not detected")

            return {
                'present': False,
                'description': 'Mangal Dosha not present',
                'aspects': aspects,
                'houses': houses_info,
            }
    
    def detect_pitra_dosha(self, planets: Dict, planet_houses: Dict) -> Dict:
        """
        Detect Pitra Dosha (ancestral affliction)
        Sun afflicted by Rahu/Ketu, or 9th house afflicted
        
        Args:
            planets: Planet positions
            planet_houses: Which house each planet is in
            
        Returns:
            Pitra Dosha information
        """
        sun_house = planet_houses.get('Sun')
        rahu_house = planet_houses.get('Rahu')
        ketu_house = planet_houses.get('Ketu')
        
        afflictions = []
        
        # Check if Sun is with Rahu or Ketu
        if sun_house == rahu_house:
            afflictions.append('Sun conjunct Rahu')
        if sun_house == ketu_house:
            afflictions.append('Sun conjunct Ketu')
        
        # Check if 9th house has Rahu or Ketu
        if rahu_house == 9:
            afflictions.append('Rahu in 9th house')
        if ketu_house == 9:
            afflictions.append('Ketu in 9th house')
        
        if afflictions:
            return {
                'present': True,
                'afflictions': afflictions,
                'severity': 'High' if len(afflictions) > 1 else 'Medium',
                'description': 'Sun or 9th house afflicted by nodes',
                'effects': 'Problems from ancestors, family issues, obstacles in life',
                'remedies': [
                    'Perform Shraddha rituals',
                    'Feed crows and poor people',
                    'Donate on Saturdays',
                    'Visit pilgrimage places',
                    'Chant Gayatri Mantra'
                ]
            }
        else:
            return {
                'present': False,
                'description': 'Pitra Dosha not present'
            }
    
    def detect_sadesati(
        self,
        planets: Dict,
        birth_datetime: datetime | None = None,
    ) -> Dict:
        """Approximate Shani Sadesati periods and current status.

        This is a simplified implementation that:
        - Uses Moon sign as the focus sign.
        - Assumes a single Sadesati window from age ~27 to ~35.
        - Splits that window into rising / peak / setting phases.
        """
        moon_sign = planets.get("Moon", {}).get("sign")

        if not birth_datetime or not moon_sign:
            return {
                "is_sadesati": False,
                "status": "Sadesati information not available",
                "current_phase": None,
                "periods": [],
            }

        # Define one long Sadesati period in adulthood
        start = birth_datetime.replace(year=birth_datetime.year + 27)
        end = birth_datetime.replace(year=birth_datetime.year + 35)

        total_days = max((end - start).days, 1)
        rising_end = start + timedelta(days=total_days / 3)
        peak_end = start + timedelta(days=2 * total_days / 3)

        today = datetime.now().date()
        is_now = start.date() <= today <= end.date()

        if is_now:
            if today <= rising_end.date():
                phase = "Rising"
            elif today <= peak_end.date():
                phase = "Peak"
            else:
                phase = "Setting"
        else:
            phase = None

        periods = [
            {
                "start_date": start.date().isoformat(),
                "end_date": rising_end.date().isoformat(),
                "sign_name": moon_sign,
                "type": "Rising",
            },
            {
                "start_date": rising_end.date().isoformat(),
                "end_date": peak_end.date().isoformat(),
                "sign_name": moon_sign,
                "type": "Peak",
            },
            {
                "start_date": peak_end.date().isoformat(),
                "end_date": end.date().isoformat(),
                "sign_name": moon_sign,
                "type": "Setting",
            },
        ]

        return {
            "is_sadesati": is_now,
            "status": "Currently under Sadesati" if is_now else "Not under Sadesati",
            "current_phase": phase,
            "periods": periods,
            "rising_phase_description": "Rising phase may bring gradual increase in responsibilities and karmic lessons.",
            "peak_phase_description": "Peak phase can be intense with important life changes and restructuring.",
            "setting_phase_description": "Setting phase usually eases the pressure and brings maturity from lessons learned.",
        }

    def analyze_all_yogas_doshas(
        self,
        planets: Dict,
        planet_houses: Dict,
        houses: Dict,
        birth_datetime: datetime | None = None,
    ) -> Dict:
        """
        Comprehensive analysis of all yogas and doshas
        
        Returns:
            Complete yoga and dosha report
        """
        return {
            "yogas": {
                "raj_yogas": self.detect_raj_yogas(planets, planet_houses, houses),
                "dhana_yogas": self.detect_dhana_yogas(planets, planet_houses),
                "mahapurusha_yogas": self.detect_mahapurusha_yogas(planets, planet_houses, houses),
            },
            "doshas": {
                "kaal_sarp_dosha": self.detect_kaal_sarp_dosha(planets),
                "mangal_dosha": self.detect_mangal_dosha(planets, planet_houses),
                "pitra_dosha": self.detect_pitra_dosha(planets, planet_houses),
            },
            "sadesati": self.detect_sadesati(planets, birth_datetime=birth_datetime),
        }


# Global instance
yoga_dosha_calculator = YogaDoshaCalculator()
