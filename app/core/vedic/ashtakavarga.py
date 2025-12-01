"""
Ashtakavarga Calculator
"""
from typing import Dict, List


class AshtakavargaCalculator:
    """Calculate Ashtakavarga (8-point strength system)"""
    
    # Benefic points assignment for each planet in different signs
    # Format: {planet: [sign positions where planet gives benefic points]}
    
    SUN_BENEFIC = {
        'Sun': [1, 2, 4, 7, 8, 9, 10, 11],
        'Moon': [3, 6, 10, 11],
        'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [5, 6, 9, 11],
        'Venus': [6, 7, 12],
        'Saturn': [1, 2, 4, 7, 8, 9, 10, 11],
        'Ascendant': [3, 4, 6, 10, 11, 12]
    }
    
    MOON_BENEFIC = {
        'Sun': [3, 6, 7, 8, 10, 11],
        'Moon': [1, 3, 6, 7, 10, 11],
        'Mars': [2, 3, 5, 6, 9, 10, 11],
        'Mercury': [1, 3, 4, 5, 7, 8, 10, 11],
        'Jupiter': [1, 4, 7, 8, 10, 11, 12],
        'Venus': [3, 4, 5, 7, 9, 10, 11],
        'Saturn': [3, 5, 6, 11],
        'Ascendant': [3, 6, 7, 8, 10, 11]
    }
    
    MARS_BENEFIC = {
        'Sun': [3, 5, 6, 10, 11],
        'Moon': [3, 6, 11],
        'Mars': [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [3, 5, 6, 11],
        'Jupiter': [6, 10, 11, 12],
        'Venus': [6, 8, 11, 12],
        'Saturn': [1, 4, 7, 8, 9, 10, 11],
        'Ascendant': [1, 3, 6, 10, 11]
    }
    
    MERCURY_BENEFIC = {
        'Sun': [5, 6, 9, 11, 12],
        'Moon': [2, 4, 6, 8, 10, 11],
        'Mars': [1, 2, 4, 7, 8, 9, 10, 11],
        'Mercury': [1, 3, 5, 6, 9, 10, 11, 12],
        'Jupiter': [6, 8, 11, 12],
        'Venus': [1, 2, 3, 4, 5, 8, 9, 11],
        'Saturn': [1, 2, 4, 7, 8, 9, 10, 11],
        'Ascendant': [1, 2, 4, 6, 8, 10, 11]
    }
    
    JUPITER_BENEFIC = {
        'Sun': [1, 2, 3, 4, 7, 8, 9, 10, 11],
        'Moon': [2, 5, 7, 9, 11],
        'Mars': [1, 2, 4, 7, 8, 10, 11],
        'Mercury': [1, 2, 4, 5, 6, 9, 10, 11],
        'Jupiter': [1, 2, 3, 4, 7, 8, 10, 11],
        'Venus': [2, 5, 6, 9, 10, 11],
        'Saturn': [3, 5, 6, 12],
        'Ascendant': [1, 2, 4, 5, 6, 7, 9, 10, 11]
    }
    
    VENUS_BENEFIC = {
        'Sun': [8, 11, 12],
        'Moon': [1, 2, 3, 4, 5, 8, 9, 11, 12],
        'Mars': [3, 4, 6, 9, 11, 12],
        'Mercury': [3, 5, 6, 9, 11],
        'Jupiter': [5, 8, 9, 10, 11],
        'Venus': [1, 2, 3, 4, 5, 8, 9, 10, 11],
        'Saturn': [3, 4, 5, 8, 9, 10, 11],
        'Ascendant': [1, 2, 3, 4, 5, 8, 9, 11, 12]
    }
    
    SATURN_BENEFIC = {
        'Sun': [1, 2, 4, 7, 8, 10, 11],
        'Moon': [3, 6, 11],
        'Mars': [3, 5, 6, 10, 11, 12],
        'Mercury': [6, 8, 9, 10, 11, 12],
        'Jupiter': [5, 6, 11, 12],
        'Venus': [6, 11, 12],
        'Saturn': [3, 5, 6, 11],
        'Ascendant': [1, 3, 4, 6, 10, 11, 12]
    }
    
    BENEFIC_POINTS = {
        'Sun': SUN_BENEFIC,
        'Moon': MOON_BENEFIC,
        'Mars': MARS_BENEFIC,
        'Mercury': MERCURY_BENEFIC,
        'Jupiter': JUPITER_BENEFIC,
        'Venus': VENUS_BENEFIC,
        'Saturn': SATURN_BENEFIC
    }
    
    def calculate_planet_ashtakavarga(
        self,
        planet_name: str,
        planets: Dict,
        ascendant_sign: int
    ) -> Dict:
        """
        Calculate Ashtakavarga for a specific planet
        
        Args:
            planet_name: Name of planet (Sun, Moon, Mars, etc.)
            planets: All planet positions
            ascendant_sign: Ascendant sign number (0-11)
            
        Returns:
            Ashtakavarga chart with benefic points for each sign
        """
        if planet_name not in self.BENEFIC_POINTS:
            return None
        
        benefic_config = self.BENEFIC_POINTS[planet_name]
        
        # Initialize points for all 12 signs
        sign_points = [0] * 12
        
        # Calculate points from each contributing planet
        for contributing_planet, positions in benefic_config.items():
            if contributing_planet == 'Ascendant':
                reference_sign = ascendant_sign
            else:
                reference_sign = planets[contributing_planet]['sign_num']
            
            # Add points to signs in benefic positions
            for position in positions:
                target_sign = (reference_sign + position - 1) % 12
                sign_points[target_sign] += 1
        
        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer',
            'Leo', 'Virgo', 'Libra', 'Scorpio',
            'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        # Create detailed result
        result = {
            'planet': planet_name,
            'total_points': sum(sign_points),
            'sign_points': []
        }
        
        for i, points in enumerate(sign_points):
            result['sign_points'].append({
                'sign': signs[i],
                'sign_num': i,
                'points': points
            })
        
        return result
    
    def calculate_sarvashtakavarga(
        self,
        planets: Dict,
        ascendant_sign: int
    ) -> Dict:
        """
        Calculate Sarvashtakavarga (combined Ashtakavarga of all planets)
        
        Args:
            planets: All planet positions
            ascendant_sign: Ascendant sign number
            
        Returns:
            Combined Ashtakavarga with total points for each sign
        """
        # Calculate individual Ashtakavarga for each planet
        individual_charts = {}
        
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn']:
            chart = self.calculate_planet_ashtakavarga(planet, planets, ascendant_sign)
            if chart:
                individual_charts[planet] = chart
        
        # Combine all charts
        combined_points = [0] * 12
        
        for planet_chart in individual_charts.values():
            for i, sign_data in enumerate(planet_chart['sign_points']):
                combined_points[i] += sign_data['points']
        
        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer',
            'Leo', 'Virgo', 'Libra', 'Scorpio',
            'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        result = {
            'total_points': sum(combined_points),
            'sign_points': [],
            'individual_charts': individual_charts
        }
        
        for i, points in enumerate(combined_points):
            result['sign_points'].append({
                'sign': signs[i],
                'sign_num': i,
                'points': points
            })
        
        return result
    
    def analyze_ashtakavarga_strength(
        self,
        sarvashtakavarga: Dict
    ) -> Dict:
        """
        Analyze strength of signs based on Ashtakavarga points
        
        Args:
            sarvashtakavarga: Combined Ashtakavarga
            
        Returns:
            Analysis of strong and weak signs
        """
        sign_points = sarvashtakavarga['sign_points']
        
        # Categorize signs
        very_strong = []  # 35+ points
        strong = []       # 30-34 points
        average = []      # 25-29 points
        weak = []         # 20-24 points
        very_weak = []    # Below 20 points
        
        for sign_data in sign_points:
            sign = sign_data['sign']
            points = sign_data['points']
            
            if points >= 35:
                very_strong.append({'sign': sign, 'points': points})
            elif points >= 30:
                strong.append({'sign': sign, 'points': points})
            elif points >= 25:
                average.append({'sign': sign, 'points': points})
            elif points >= 20:
                weak.append({'sign': sign, 'points': points})
            else:
                very_weak.append({'sign': sign, 'points': points})
        
        return {
            'very_strong_signs': very_strong,
            'strong_signs': strong,
            'average_signs': average,
            'weak_signs': weak,
            'very_weak_signs': very_weak,
            'interpretation': {
                'very_strong': 'Excellent results, prosperity, and success',
                'strong': 'Good results with effort',
                'average': 'Mixed results, requires perseverance',
                'weak': 'Challenges and obstacles',
                'very_weak': 'Significant difficulties, needs remedies'
            }
        }
    
    def calculate_comprehensive_ashtakavarga(
        self,
        planets: Dict,
        ascendant_sign: int
    ) -> Dict:
        """
        Calculate complete Ashtakavarga analysis
        
        Args:
            planets: All planet positions
            ascendant_sign: Ascendant sign number
            
        Returns:
            Complete Ashtakavarga report
        """
        # Calculate Sarvashtakavarga
        sarvashtakavarga = self.calculate_sarvashtakavarga(planets, ascendant_sign)
        
        # Analyze strength
        analysis = self.analyze_ashtakavarga_strength(sarvashtakavarga)
        
        # Calculate transit readiness (which signs are good for transits)
        transit_guide = self._calculate_transit_guide(sarvashtakavarga)
        
        return {
            'sarvashtakavarga': sarvashtakavarga,
            'analysis': analysis,
            'transit_guide': transit_guide
        }
    
    def _calculate_transit_guide(self, sarvashtakavarga: Dict) -> List[Dict]:
        """Calculate which signs are favorable for planetary transits"""
        guide = []
        
        for sign_data in sarvashtakavarga['sign_points']:
            sign = sign_data['sign']
            points = sign_data['points']
            
            if points >= 30:
                favorability = 'Highly Favorable'
            elif points >= 25:
                favorability = 'Favorable'
            elif points >= 20:
                favorability = 'Neutral'
            else:
                favorability = 'Unfavorable'
            
            guide.append({
                'sign': sign,
                'points': points,
                'favorability': favorability,
                'recommendation': self._get_transit_recommendation(favorability)
            })
        
        return guide
    
    def _get_transit_recommendation(self, favorability: str) -> str:
        """Get recommendation based on transit favorability"""
        recommendations = {
            'Highly Favorable': 'Excellent time for new beginnings, major decisions',
            'Favorable': 'Good time for important activities, planning',
            'Neutral': 'Proceed with caution, evaluate carefully',
            'Unfavorable': 'Avoid major decisions, focus on remedies'
        }
        return recommendations.get(favorability, '')


# Global instance
ashtakavarga_calculator = AshtakavargaCalculator()
