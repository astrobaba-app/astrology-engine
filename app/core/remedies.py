"""
Remedies Engine
"""
from typing import Dict, List


class RemediesEngine:
    """Generate remedies based on planetary positions and afflictions"""
    
    # Gemstone recommendations
    GEMSTONES = {
        'Sun': {
            'primary': 'Ruby',
            'substitute': ['Red Garnet', 'Red Spinel'],
            'weight': '3-6 carats',
            'finger': 'Ring finger',
            'day': 'Sunday',
            'time': 'Sunrise'
        },
        'Moon': {
            'primary': 'Pearl',
            'substitute': ['Moonstone'],
            'weight': '5-7 carats',
            'finger': 'Little finger',
            'day': 'Monday',
            'time': 'Evening'
        },
        'Mars': {
            'primary': 'Red Coral',
            'substitute': ['Carnelian'],
            'weight': '5-8 carats',
            'finger': 'Ring finger',
            'day': 'Tuesday',
            'time': 'Morning'
        },
        'Mercury': {
            'primary': 'Emerald',
            'substitute': ['Green Tourmaline', 'Peridot'],
            'weight': '3-6 carats',
            'finger': 'Little finger',
            'day': 'Wednesday',
            'time': 'Morning'
        },
        'Jupiter': {
            'primary': 'Yellow Sapphire',
            'substitute': ['Yellow Topaz', 'Citrine'],
            'weight': '3-6 carats',
            'finger': 'Index finger',
            'day': 'Thursday',
            'time': 'Morning'
        },
        'Venus': {
            'primary': 'Diamond',
            'substitute': ['White Sapphire', 'Zircon'],
            'weight': '1-2 carats',
            'finger': 'Little finger',
            'day': 'Friday',
            'time': 'Morning'
        },
        'Saturn': {
            'primary': 'Blue Sapphire',
            'substitute': ['Amethyst', 'Blue Tourmaline'],
            'weight': '4-7 carats',
            'finger': 'Middle finger',
            'day': 'Saturday',
            'time': 'Evening'
        },
        'Rahu': {
            'primary': 'Hessonite (Gomed)',
            'substitute': [],
            'weight': '5-8 carats',
            'finger': 'Middle finger',
            'day': 'Saturday',
            'time': 'Evening'
        },
        'Ketu': {
            'primary': "Cat's Eye (Lehsunia)",
            'substitute': [],
            'weight': '5-7 carats',
            'finger': 'Middle finger',
            'day': 'Tuesday',
            'time': 'Evening'
        }
    }
    
    # Mantras
    MANTRAS = {
        'Sun': {
            'mantra': 'Om Hraam Hreem Hraum Sah Suryaya Namah',
            'count': 7000,
            'deity': 'Lord Surya'
        },
        'Moon': {
            'mantra': 'Om Shraam Shreem Shraum Sah Chandraya Namah',
            'count': 11000,
            'deity': 'Lord Chandra'
        },
        'Mars': {
            'mantra': 'Om Kraam Kreem Kraum Sah Bhaumaya Namah',
            'count': 10000,
            'deity': 'Lord Mangal'
        },
        'Mercury': {
            'mantra': 'Om Braam Breem Braum Sah Budhaya Namah',
            'count': 9000,
            'deity': 'Lord Budha'
        },
        'Jupiter': {
            'mantra': 'Om Graam Greem Graum Sah Gurave Namah',
            'count': 19000,
            'deity': 'Lord Brihaspati'
        },
        'Venus': {
            'mantra': 'Om Draam Dreem Draum Sah Shukraya Namah',
            'count': 16000,
            'deity': 'Lord Shukra'
        },
        'Saturn': {
            'mantra': 'Om Praam Preem Praum Sah Shanaye Namah',
            'count': 23000,
            'deity': 'Lord Shani'
        },
        'Rahu': {
            'mantra': 'Om Bhraam Bhreem Bhraum Sah Rahave Namah',
            'count': 18000,
            'deity': 'Lord Rahu'
        },
        'Ketu': {
            'mantra': 'Om Sraam Sreem Sraum Sah Ketave Namah',
            'count': 17000,
            'deity': 'Lord Ketu'
        }
    }
    
    # Charity/Donation
    CHARITY = {
        'Sun': {
            'items': ['Wheat', 'Jaggery', 'Ruby', 'Copper'],
            'day': 'Sunday',
            'color': 'Red/Orange'
        },
        'Moon': {
            'items': ['Rice', 'Sugar', 'White clothes', 'Pearl'],
            'day': 'Monday',
            'color': 'White'
        },
        'Mars': {
            'items': ['Red lentils', 'Jaggery', 'Red clothes', 'Copper'],
            'day': 'Tuesday',
            'color': 'Red'
        },
        'Mercury': {
            'items': ['Green vegetables', 'Green clothes', 'Emerald'],
            'day': 'Wednesday',
            'color': 'Green'
        },
        'Jupiter': {
            'items': ['Yellow clothes', 'Turmeric', 'Gold', 'Gram dal'],
            'day': 'Thursday',
            'color': 'Yellow'
        },
        'Venus': {
            'items': ['White rice', 'Sugar', 'White clothes', 'Silver'],
            'day': 'Friday',
            'color': 'White/Pink'
        },
        'Saturn': {
            'items': ['Black sesame', 'Iron', 'Black clothes', 'Mustard oil'],
            'day': 'Saturday',
            'color': 'Black/Blue'
        },
        'Rahu': {
            'items': ['Black gram', 'Blue clothes', 'Iron'],
            'day': 'Saturday',
            'color': 'Dark colors'
        },
        'Ketu': {
            'items': ['Sesame', 'Blankets', 'Black gram'],
            'day': 'Tuesday',
            'color': 'Brown/Grey'
        }
    }
    
    # Fasting days
    FASTING = {
        'Sun': 'Sunday',
        'Moon': 'Monday',
        'Mars': 'Tuesday',
        'Mercury': 'Wednesday',
        'Jupiter': 'Thursday',
        'Venus': 'Friday',
        'Saturn': 'Saturday',
        'Rahu': 'Saturday',
        'Ketu': 'Tuesday'
    }
    
    def recommend_gemstones(
        self,
        strengths: Dict,
        planet_houses: Dict
    ) -> List[Dict]:
        """
        Recommend gemstones based on planetary strengths
        
        Args:
            strengths: Shadbala strengths of planets
            planet_houses: House positions of planets
            
        Returns:
            List of gemstone recommendations
        """
        recommendations = []
        
        # Identify weak planets
        for planet, strength_data in strengths.items():
            if strength_data['percentage'] < 50:  # Weak planet
                gem_info = self.GEMSTONES.get(planet)
                if gem_info:
                    recommendations.append({
                        'planet': planet,
                        'reason': f'{planet} is weak ({strength_data["percentage"]}%)',
                        'gemstone': gem_info['primary'],
                        'alternatives': gem_info['substitute'],
                        'weight': gem_info['weight'],
                        'finger': gem_info['finger'],
                        'wearing_day': gem_info['day'],
                        'wearing_time': gem_info['time'],
                        'metal': 'Gold' if planet in ['Sun', 'Jupiter', 'Mars'] else 'Silver'
                    })
        
        # Recommend ascendant lord gemstone
        # This is simplified - actual implementation would determine ascendant lord
        
        return recommendations
    
    def recommend_mantras(
        self,
        planets_to_strengthen: List[str]
    ) -> List[Dict]:
        """
        Recommend mantras for specific planets
        
        Args:
            planets_to_strengthen: List of planet names
            
        Returns:
            List of mantra recommendations
        """
        recommendations = []
        
        for planet in planets_to_strengthen:
            mantra_info = self.MANTRAS.get(planet)
            if mantra_info:
                recommendations.append({
                    'planet': planet,
                    'mantra': mantra_info['mantra'],
                    'count': mantra_info['count'],
                    'deity': mantra_info['deity'],
                    'benefits': f'Strengthens {planet} and reduces negative effects'
                })
        
        return recommendations
    
    def recommend_charity(
        self,
        planets_to_pacify: List[str]
    ) -> List[Dict]:
        """
        Recommend charity/donations for planets
        
        Args:
            planets_to_pacify: List of planet names
            
        Returns:
            List of charity recommendations
        """
        recommendations = []
        
        for planet in planets_to_pacify:
            charity_info = self.CHARITY.get(planet)
            if charity_info:
                recommendations.append({
                    'planet': planet,
                    'items': charity_info['items'],
                    'day': charity_info['day'],
                    'color': charity_info['color'],
                    'instructions': f'Donate on {charity_info["day"]} to needy people'
                })
        
        return recommendations
    
    def recommend_fasting(
        self,
        planets_to_appease: List[str]
    ) -> List[Dict]:
        """
        Recommend fasting days
        
        Args:
            planets_to_appease: List of planet names
            
        Returns:
            List of fasting recommendations
        """
        recommendations = []
        
        for planet in planets_to_appease:
            fasting_day = self.FASTING.get(planet)
            if fasting_day:
                recommendations.append({
                    'planet': planet,
                    'day': fasting_day,
                    'instructions': f'Fast on {fasting_day} or eat once a day',
                    'benefits': f'Appeases {planet} and reduces malefic effects'
                })
        
        return recommendations
    
    def generate_comprehensive_remedies(
        self,
        strengths: Dict,
        planet_houses: Dict,
        doshas: Dict
    ) -> Dict:
        """
        Generate comprehensive remedies report
        
        Args:
            strengths: Planetary strengths
            planet_houses: Planet house positions
            doshas: Detected doshas
            
        Returns:
            Complete remedies report
        """
        # Identify weak planets
        weak_planets = [
            planet for planet, data in strengths.items()
            if data['percentage'] < 50
        ]
        
        # Identify planets causing doshas
        dosha_planets = []
        if doshas.get('mangal_dosha', {}).get('present'):
            dosha_planets.append('Mars')
        if doshas.get('kaal_sarp_dosha', {}).get('present'):
            dosha_planets.extend(['Rahu', 'Ketu'])
        if doshas.get('pitra_dosha', {}).get('present'):
            dosha_planets.append('Sun')
        
        # Remove duplicates
        planets_needing_remedies = list(set(weak_planets + dosha_planets))
        
        return {
            'gemstones': self.recommend_gemstones(strengths, planet_houses),
            'mantras': self.recommend_mantras(planets_needing_remedies),
            'charity': self.recommend_charity(planets_needing_remedies),
            'fasting': self.recommend_fasting(planets_needing_remedies),
            'general_remedies': [
                'Perform daily meditation and yoga',
                'Recite Gayatri Mantra daily',
                'Visit temples regularly',
                'Help the needy and poor',
                'Respect elders and teachers'
            ]
        }


# Global instance
remedies_engine = RemediesEngine()
