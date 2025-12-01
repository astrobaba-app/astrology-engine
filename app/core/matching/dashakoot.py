"""
Dashakoot (10-Kuta) Matching System
Extension of Ashtakoot with 2 additional Kutas
"""
from typing import Dict
from app.core.matching.ashtakoot import ashtakoot_matching


class DashakootMatching:
    """Dashakoot (10-fold) compatibility matching system"""
    
    # Maximum points for each Kuta
    MAX_POINTS = {
        'Varna': 1,
        'Vashya': 2,
        'Tara': 3,
        'Yoni': 4,
        'Graha Maitri': 5,
        'Gana': 6,
        'Bhakoot': 7,
        'Nadi': 8,
        'Mahendra': 1,       # Additional in Dashakoot
        'Stree Deergha': 1   # Additional in Dashakoot
    }
    
    TOTAL_MAX_POINTS = 38  # 36 + 2 additional
    
    def calculate_mahendra_kuta(self, male_nakshatra_num: int, female_nakshatra_num: int) -> Dict:
        """
        Calculate Mahendra Kuta (1 point)
        Ensures male's prosperity and dominance
        """
        # Count from male to female nakshatra
        count = (female_nakshatra_num - male_nakshatra_num + 27) % 27 + 1
        
        # Mahendra positions: 4, 7, 10, 13, 16, 19, 22, 25
        mahendra_positions = [4, 7, 10, 13, 16, 19, 22, 25]
        
        points = 1 if count in mahendra_positions else 0
        
        return {
            'name': 'Mahendra Kuta',
            'count': count,
            'points': points,
            'max_points': 1,
            'description': 'Male prosperity and dominance',
            'favorable': points == 1
        }
    
    def calculate_stree_deergha_kuta(self, male_nakshatra_num: int, female_nakshatra_num: int) -> Dict:
        """
        Calculate Stree Deergha Kuta (1 point)
        Ensures female's welfare and longevity
        """
        # Count from female to male nakshatra
        count = (male_nakshatra_num - female_nakshatra_num + 27) % 27 + 1
        
        # Stree Deergha is favorable if count > 13 (more than half the zodiac)
        points = 1 if count > 13 else 0
        
        return {
            'name': 'Stree Deergha Kuta',
            'count': count,
            'points': points,
            'max_points': 1,
            'description': 'Female welfare and longevity',
            'favorable': points == 1
        }
    
    def calculate_dashakoot_matching(
        self,
        male_moon_sign: str,
        male_moon_sign_num: int,
        male_nakshatra: str,
        male_nakshatra_num: int,
        female_moon_sign: str,
        female_moon_sign_num: int,
        female_nakshatra: str,
        female_nakshatra_num: int
    ) -> Dict:
        """
        Complete Dashakoot matching calculation
        Includes all 8 Ashtakoot Kutas + 2 additional Kutas
        
        Returns:
            Complete matching report with all 10 Kutas
        """
        # First, get all 8 Ashtakoot Kutas
        ashtakoot_result = ashtakoot_matching.calculate_ashtakoot_matching(
            male_moon_sign=male_moon_sign,
            male_moon_sign_num=male_moon_sign_num,
            male_nakshatra=male_nakshatra,
            male_nakshatra_num=male_nakshatra_num,
            female_moon_sign=female_moon_sign,
            female_moon_sign_num=female_moon_sign_num,
            female_nakshatra=female_nakshatra,
            female_nakshatra_num=female_nakshatra_num
        )
        
        # Calculate 2 additional Kutas
        mahendra = self.calculate_mahendra_kuta(male_nakshatra_num, female_nakshatra_num)
        stree_deergha = self.calculate_stree_deergha_kuta(male_nakshatra_num, female_nakshatra_num)
        
        # Add additional Kutas to the result
        all_kutas = ashtakoot_result['kutas'].copy()
        all_kutas['mahendra'] = mahendra
        all_kutas['stree_deergha'] = stree_deergha
        
        # Calculate new total
        total_points = ashtakoot_result['total_points'] + mahendra['points'] + stree_deergha['points']
        
        # Determine compatibility level for Dashakoot
        if total_points >= 30:
            compatibility = 'Excellent'
            recommendation = 'Highly compatible match'
        elif total_points >= 25:
            compatibility = 'Very Good'
            recommendation = 'Very compatible match'
        elif total_points >= 20:
            compatibility = 'Good'
            recommendation = 'Compatible match with minor adjustments'
        elif total_points >= 15:
            compatibility = 'Average'
            recommendation = 'Moderate compatibility, needs understanding'
        else:
            compatibility = 'Poor'
            recommendation = 'Not recommended without remedies'
        
        # Keep critical issues from Ashtakoot
        critical_issues = ashtakoot_result['critical_issues'].copy()
        
        # Add warnings for additional kutas if needed
        if mahendra['points'] == 0:
            critical_issues.append('Mahendra not favorable - may affect male prosperity')
        if stree_deergha['points'] == 0:
            critical_issues.append('Stree Deergha not favorable - may affect female welfare')
        
        return {
            'kutas': all_kutas,
            'total_points': round(total_points, 1),
            'max_points': self.TOTAL_MAX_POINTS,
            'percentage': round((total_points / self.TOTAL_MAX_POINTS) * 100, 2),
            'compatibility': compatibility,
            'recommendation': recommendation,
            'critical_issues': critical_issues,
            'ashtakoot_score': ashtakoot_result['total_points'],
            'additional_kutas_score': mahendra['points'] + stree_deergha['points']
        }


# Global instance
dashakoot_matching = DashakootMatching()
