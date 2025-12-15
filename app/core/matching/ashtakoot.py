"""
Ashtakoot (8-Kuta) Matching System
"""
from typing import Dict, Tuple


class AshtakootMatching:
    """Ashtakoot (8-fold) compatibility matching system"""
    
    # Maximum points for each Kuta
    MAX_POINTS = {
        'Varna': 1,
        'Vashya': 2,
        'Tara': 3,
        'Yoni': 4,
        'Graha Maitri': 5,
        'Gana': 6,
        'Bhakoot': 7,
        'Nadi': 8
    }
    
    TOTAL_MAX_POINTS = 36
    
    # Varna (Caste) classification
    VARNA_MAP = {
        'Aries': 'Kshatriya', 'Taurus': 'Vaishya', 'Gemini': 'Shudra',
        'Cancer': 'Brahmin', 'Leo': 'Kshatriya', 'Virgo': 'Vaishya',
        'Libra': 'Shudra', 'Scorpio': 'Brahmin', 'Sagittarius': 'Kshatriya',
        'Capricorn': 'Vaishya', 'Aquarius': 'Shudra', 'Pisces': 'Brahmin'
    }
    
    VARNA_ORDER = ['Brahmin', 'Kshatriya', 'Vaishya', 'Shudra']
    
    # Vashya (Attraction) classification
    VASHYA_MAP = {
        'Aries': ['Leo', 'Sagittarius', 'Aries'],
        'Taurus': ['Cancer', 'Libra'],
        'Gemini': ['Virgo', 'Aquarius'],
        'Cancer': ['Scorpio', 'Sagittarius'],
        'Leo': ['Aries', 'Sagittarius', 'Leo'],
        'Virgo': ['Gemini', 'Pisces'],
        'Libra': ['Capricorn', 'Virgo'],
        'Scorpio': ['Cancer', 'Pisces'],
        'Sagittarius': ['Aries', 'Leo', 'Pisces'],
        'Capricorn': ['Aquarius', 'Aries'],
        'Aquarius': ['Gemini', 'Aquarius'],
        'Pisces': ['Capricorn', 'Scorpio']
    }
    
    # Gana (Nature) classification
    GANA_MAP = {
        'Ashwini': 'Deva', 'Bharani': 'Manushya', 'Krittika': 'Rakshasa',
        'Rohini': 'Manushya', 'Mrigashira': 'Deva', 'Ardra': 'Manushya',
        'Punarvasu': 'Deva', 'Pushya': 'Deva', 'Ashlesha': 'Rakshasa',
        'Magha': 'Rakshasa', 'Purva Phalguni': 'Manushya', 'Uttara Phalguni': 'Manushya',
        'Hasta': 'Deva', 'Chitra': 'Rakshasa', 'Swati': 'Deva',
        'Vishakha': 'Rakshasa', 'Anuradha': 'Deva', 'Jyeshtha': 'Rakshasa',
        'Mula': 'Rakshasa', 'Purva Ashadha': 'Manushya', 'Uttara Ashadha': 'Manushya',
        'Shravana': 'Deva', 'Dhanishta': 'Rakshasa', 'Shatabhisha': 'Rakshasa',
        'Purva Bhadrapada': 'Manushya', 'Uttara Bhadrapada': 'Manushya', 'Revati': 'Deva'
    }
    
    # Yoni (Sexual compatibility)
    YONI_MAP = {
        'Ashwini': 'Horse', 'Bharani': 'Elephant', 'Krittika': 'Sheep',
        'Rohini': 'Serpent', 'Mrigashira': 'Serpent', 'Ardra': 'Dog',
        'Punarvasu': 'Cat', 'Pushya': 'Sheep', 'Ashlesha': 'Cat',
        'Magha': 'Rat', 'Purva Phalguni': 'Rat', 'Uttara Phalguni': 'Cow',
        'Hasta': 'Buffalo', 'Chitra': 'Tiger', 'Swati': 'Buffalo',
        'Vishakha': 'Tiger', 'Anuradha': 'Deer', 'Jyeshtha': 'Deer',
        'Mula': 'Dog', 'Purva Ashadha': 'Monkey', 'Uttara Ashadha': 'Mongoose',
        'Shravana': 'Monkey', 'Dhanishta': 'Lion', 'Shatabhisha': 'Horse',
        'Purva Bhadrapada': 'Lion', 'Uttara Bhadrapada': 'Cow', 'Revati': 'Elephant'
    }
    
    # Yoni compatibility matrix
    YONI_COMPATIBILITY = {
        'Horse': {'Horse': 4, 'Elephant': 2, 'Sheep': 2, 'Serpent': 3, 'Dog': 2, 
                 'Cat': 2, 'Rat': 2, 'Cow': 1, 'Buffalo': 3, 'Tiger': 1, 
                 'Deer': 2, 'Monkey': 3, 'Mongoose': 2, 'Lion': 1},
        'Elephant': {'Elephant': 4, 'Horse': 2, 'Sheep': 3, 'Serpent': 3, 'Dog': 2,
                    'Cat': 3, 'Rat': 2, 'Cow': 2, 'Buffalo': 3, 'Tiger': 2,
                    'Deer': 2, 'Monkey': 3, 'Mongoose': 2, 'Lion': 0},
        'Sheep': {'Sheep': 4, 'Monkey': 0, 'Tiger': 2, 'Horse': 2, 'Elephant': 3,
                 'Serpent': 2, 'Dog': 2, 'Cat': 2, 'Rat': 3, 'Cow': 2,
                 'Buffalo': 2, 'Deer': 2, 'Mongoose': 2, 'Lion': 2},
        'Serpent': {'Serpent': 4, 'Mongoose': 0, 'Horse': 3, 'Elephant': 3, 'Sheep': 2,
                   'Dog': 2, 'Cat': 2, 'Rat': 2, 'Cow': 2, 'Buffalo': 2,
                   'Tiger': 2, 'Deer': 2, 'Monkey': 2, 'Lion': 2},
        'Dog': {'Dog': 4, 'Deer': 0, 'Horse': 2, 'Elephant': 2, 'Sheep': 2,
               'Serpent': 2, 'Cat': 2, 'Rat': 2, 'Cow': 2, 'Buffalo': 2,
               'Tiger': 2, 'Monkey': 2, 'Mongoose': 2, 'Lion': 2},
        'Cat': {'Cat': 4, 'Rat': 0, 'Horse': 2, 'Elephant': 3, 'Sheep': 2,
               'Serpent': 2, 'Dog': 2, 'Cow': 2, 'Buffalo': 2, 'Tiger': 2,
               'Deer': 2, 'Monkey': 2, 'Mongoose': 2, 'Lion': 2},
        'Rat': {'Rat': 4, 'Cat': 0, 'Horse': 2, 'Elephant': 2, 'Sheep': 3,
               'Serpent': 2, 'Dog': 2, 'Cow': 2, 'Buffalo': 2, 'Tiger': 2,
               'Deer': 2, 'Monkey': 3, 'Mongoose': 2, 'Lion': 2},
        'Cow': {'Cow': 4, 'Tiger': 0, 'Horse': 1, 'Elephant': 2, 'Sheep': 2,
               'Serpent': 2, 'Dog': 2, 'Cat': 2, 'Rat': 2, 'Buffalo': 3,
               'Deer': 2, 'Monkey': 2, 'Mongoose': 2, 'Lion': 2},
        'Buffalo': {'Buffalo': 4, 'Lion': 0, 'Horse': 3, 'Elephant': 3, 'Sheep': 2,
                   'Serpent': 2, 'Dog': 2, 'Cat': 2, 'Rat': 2, 'Cow': 3,
                   'Tiger': 2, 'Deer': 2, 'Monkey': 2, 'Mongoose': 2},
        'Tiger': {'Tiger': 4, 'Cow': 0, 'Horse': 1, 'Elephant': 2, 'Sheep': 2,
                 'Serpent': 2, 'Dog': 2, 'Cat': 2, 'Rat': 2, 'Buffalo': 2,
                 'Deer': 3, 'Monkey': 2, 'Mongoose': 2, 'Lion': 2},
        'Deer': {'Deer': 4, 'Dog': 0, 'Horse': 2, 'Elephant': 2, 'Sheep': 2,
                'Serpent': 2, 'Cat': 2, 'Rat': 2, 'Cow': 2, 'Buffalo': 2,
                'Tiger': 3, 'Monkey': 2, 'Mongoose': 2, 'Lion': 2},
        'Monkey': {'Monkey': 4, 'Sheep': 0, 'Horse': 3, 'Elephant': 3, 'Serpent': 2,
                  'Dog': 2, 'Cat': 2, 'Rat': 3, 'Cow': 2, 'Buffalo': 2,
                  'Tiger': 2, 'Deer': 2, 'Mongoose': 2, 'Lion': 2},
        'Mongoose': {'Mongoose': 4, 'Serpent': 0, 'Horse': 2, 'Elephant': 2, 'Sheep': 2,
                    'Dog': 2, 'Cat': 2, 'Rat': 2, 'Cow': 2, 'Buffalo': 2,
                    'Tiger': 2, 'Deer': 2, 'Monkey': 2, 'Lion': 2},
        'Lion': {'Lion': 4, 'Buffalo': 0, 'Horse': 1, 'Elephant': 0, 'Sheep': 2,
                'Serpent': 2, 'Dog': 2, 'Cat': 2, 'Rat': 2, 'Cow': 2,
                'Tiger': 2, 'Deer': 2, 'Monkey': 2, 'Mongoose': 2}
    }
    
    def calculate_varna_kuta(self, male_moon_sign: str, female_moon_sign: str) -> Dict:
        """Calculate Varna Kuta (1 point)"""
        male_varna = self.VARNA_MAP[male_moon_sign]
        female_varna = self.VARNA_MAP[female_moon_sign]
        
        male_order = self.VARNA_ORDER.index(male_varna)
        female_order = self.VARNA_ORDER.index(female_varna)
        
        # Male's varna should be equal or higher
        points = 1 if male_order <= female_order else 0
        
        return {
            'name': 'Varna Kuta',
            'male': male_varna,
            'female': female_varna,
            'points': points,
            'max_points': 1,
            'description': 'Spiritual compatibility and ego'
        }
    
    def calculate_vashya_kuta(self, male_moon_sign: str, female_moon_sign: str) -> Dict:
        """Calculate Vashya Kuta (2 points)"""
        male_vashya = self.VASHYA_MAP[male_moon_sign]
        female_vashya = self.VASHYA_MAP[female_moon_sign]
        
        # Check mutual attraction
        male_attracts_female = female_moon_sign in male_vashya
        female_attracts_male = male_moon_sign in female_vashya
        
        if male_attracts_female and female_attracts_male:
            points = 2
        elif male_attracts_female or female_attracts_male:
            points = 1
        else:
            points = 0
        
        if points == 2:
            relation_detail = "Strong mutual attraction between both signs"
        elif points == 1:
            if male_attracts_female and not female_attracts_male:
                relation_detail = f"{male_moon_sign} attracts {female_moon_sign}, but attraction is one-sided"
            elif female_attracts_male and not male_attracts_female:
                relation_detail = f"{female_moon_sign} attracts {male_moon_sign}, but attraction is one-sided"
            else:
                relation_detail = "Partial attraction between the signs"
        else:
            relation_detail = "Low or no natural attraction between the signs"

        return {
            'name': 'Vashya Kuta',
            # For UI: show each partner's Moon sign
            'male': male_moon_sign,
            'female': female_moon_sign,
            'male_attracts_female': male_attracts_female,
            'female_attracts_male': female_attracts_male,
            'points': points,
            'max_points': 2,
            'description': 'Mutual attraction and control',
            'detail': relation_detail,
        }
    
    def calculate_tara_kuta(self, male_nakshatra_num: int, female_nakshatra_num: int) -> Dict:
        """Calculate Tara Kuta (3 points)"""
        # Count from male to female nakshatra
        count = (female_nakshatra_num - male_nakshatra_num + 27) % 27 + 1
        remainder = count % 9
        
        # Janma (1), Sampat (2), Vipat (3), Kshema (4), Pratyari (5),
        # Sadhaka (6), Naidhana (7), Mitra (8), Parama Mitra (9)
        
        if remainder in [1, 3, 5, 7]:  # Inauspicious taras
            points = 0
        elif remainder in [2, 4, 6, 8]:  # Somewhat auspicious
            points = 1.5
        else:  # remainder == 0 (9)
            points = 3

        # Map indices back to nakshatra names so UI can show
        # each partner's birth star in the Tara Kuta row.
        nakshatra_names = [
            'Ashwini',
            'Bharani',
            'Krittika',
            'Rohini',
            'Mrigashira',
            'Ardra',
            'Punarvasu',
            'Pushya',
            'Ashlesha',
            'Magha',
            'Purva Phalguni',
            'Uttara Phalguni',
            'Hasta',
            'Chitra',
            'Swati',
            'Vishakha',
            'Anuradha',
            'Jyeshtha',
            'Mula',
            'Purva Ashadha',
            'Uttara Ashadha',
            'Shravana',
            'Dhanishta',
            'Shatabhisha',
            'Purva Bhadrapada',
            'Uttara Bhadrapada',
            'Revati',
        ]

        male_nakshatra = nakshatra_names[male_nakshatra_num] if 0 <= male_nakshatra_num < len(nakshatra_names) else 'Unknown'
        female_nakshatra = nakshatra_names[female_nakshatra_num] if 0 <= female_nakshatra_num < len(nakshatra_names) else 'Unknown'
        
        return {
            'name': 'Tara Kuta',
            'male': male_nakshatra,
            'female': female_nakshatra,
            'count': count,
            'tara_number': remainder if remainder != 0 else 9,
            'points': points,
            'max_points': 3,
            'description': 'Birth star compatibility and health'
        }
    
    def calculate_yoni_kuta(self, male_nakshatra: str, female_nakshatra: str) -> Dict:
        """Calculate Yoni Kuta (4 points)"""
        male_yoni = self.YONI_MAP[male_nakshatra]
        female_yoni = self.YONI_MAP[female_nakshatra]
        
        points = self.YONI_COMPATIBILITY.get(male_yoni, {}).get(female_yoni, 2)
        
        return {
            'name': 'Yoni Kuta',
            'male': male_yoni,
            'female': female_yoni,
            'points': points,
            'max_points': 4,
            'description': 'Physical and sexual compatibility'
        }
    
    def calculate_graha_maitri_kuta(
        self, 
        male_moon_sign_num: int, 
        female_moon_sign_num: int
    ) -> Dict:
        """Calculate Graha Maitri Kuta (5 points)"""
        # Sign lords
        lords = [
            'Mars', 'Venus', 'Mercury', 'Moon', 'Sun', 'Mercury',
            'Venus', 'Mars', 'Jupiter', 'Saturn', 'Saturn', 'Jupiter'
        ]
        
        male_lord = lords[male_moon_sign_num]
        female_lord = lords[female_moon_sign_num]
        
        # Planetary relationships (simplified)
        friends = {
            'Sun': ['Moon', 'Mars', 'Jupiter'],
            'Moon': ['Sun', 'Mercury'],
            'Mars': ['Sun', 'Moon', 'Jupiter'],
            'Mercury': ['Sun', 'Venus'],
            'Jupiter': ['Sun', 'Moon', 'Mars'],
            'Venus': ['Mercury', 'Saturn'],
            'Saturn': ['Mercury', 'Venus']
        }
        
        enemies = {
            'Sun': ['Venus', 'Saturn'],
            'Moon': ['None'],
            'Mars': ['Mercury'],
            'Mercury': ['Moon'],
            'Jupiter': ['Mercury', 'Venus'],
            'Venus': ['Sun', 'Moon'],
            'Saturn': ['Sun', 'Moon', 'Mars']
        }
        
        if male_lord == female_lord:
            points = 5  # Same lord
        elif female_lord in friends.get(male_lord, []) and male_lord in friends.get(female_lord, []):
            points = 4  # Mutual friends
        elif female_lord in friends.get(male_lord, []) or male_lord in friends.get(female_lord, []):
            points = 3  # One-way friend
        elif female_lord not in enemies.get(male_lord, []) and male_lord not in enemies.get(female_lord, []):
            points = 1  # Neutral
        else:
            points = 0  # Enemies
        
        return {
            'name': 'Graha Maitri Kuta',
            'male_lord': male_lord,
            'female_lord': female_lord,
            'points': points,
            'max_points': 5,
            'description': 'Mental compatibility and friendship'
        }
    
    def calculate_gana_kuta(self, male_nakshatra: str, female_nakshatra: str) -> Dict:
        """Calculate Gana Kuta (6 points)"""
        male_gana = self.GANA_MAP[male_nakshatra]
        female_gana = self.GANA_MAP[female_nakshatra]
        
        if male_gana == female_gana:
            points = 6
        elif (male_gana == 'Deva' and female_gana == 'Manushya') or \
             (male_gana == 'Manushya' and female_gana == 'Deva'):
            points = 5
        elif (male_gana == 'Manushya' and female_gana == 'Rakshasa') or \
             (male_gana == 'Rakshasa' and female_gana == 'Manushya'):
            points = 0
        else:  # Deva and Rakshasa
            points = 0
        
        return {
            'name': 'Gana Kuta',
            'male': male_gana,
            'female': female_gana,
            'points': points,
            'max_points': 6,
            'description': 'Temperament and behavior compatibility'
        }
    
    def calculate_bhakoot_kuta(self, male_moon_sign_num: int, female_moon_sign_num: int) -> Dict:
        """Calculate Bhakoot Kuta (7 points)"""
        diff = abs(male_moon_sign_num - female_moon_sign_num)
        
        # 2/12, 5/9, 6/8 positions are inauspicious
        if diff in [1, 5, 6, 7, 11]:
            points = 0
        else:
            points = 7

        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
            'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]

        # Classify Bhakoot relationship type for richer UI text
        if diff in [1, 11]:
            relation_detail = "2/12 Bhakoot relationship – can give financial and stability challenges"
        elif diff in [5, 7]:
            relation_detail = "5/9 Bhakoot relationship – may cause dharma and life-path mismatch"
        elif diff == 6:
            relation_detail = "6/8 Bhakoot relationship – associated with health and obstacle issues"
        else:
            relation_detail = "Favourable Bhakoot relationship between the Moon signs"

        return {
            'name': 'Bhakoot Kuta',
            # For UI: show each partner's Moon sign
            'male': signs[male_moon_sign_num],
            'female': signs[female_moon_sign_num],
            'sign_difference': diff,
            'points': points,
            'max_points': 7,
            'description': 'Love and prosperity in relationship',
            'detail': relation_detail,
        }
    
    def calculate_nadi_kuta(self, male_nakshatra_num: int, female_nakshatra_num: int) -> Dict:
        """Calculate Nadi Kuta (8 points) - Most important"""
        # Nadi classification (Aadi, Madhya, Antya)
        nadi_map = [
            'Aadi', 'Madhya', 'Antya', 'Aadi', 'Madhya', 'Antya',
            'Aadi', 'Madhya', 'Antya', 'Aadi', 'Madhya', 'Antya',
            'Aadi', 'Madhya', 'Antya', 'Aadi', 'Madhya', 'Antya',
            'Aadi', 'Madhya', 'Antya', 'Aadi', 'Madhya', 'Antya',
            'Aadi', 'Madhya', 'Antya'
        ]
        
        male_nadi = nadi_map[male_nakshatra_num]
        female_nadi = nadi_map[female_nakshatra_num]
        
        # Same Nadi is inauspicious (health issues for children)
        points = 0 if male_nadi == female_nadi else 8
        
        return {
            'name': 'Nadi Kuta',
            'male': male_nadi,
            'female': female_nadi,
            'points': points,
            'max_points': 8,
            'description': 'Health and progeny',
            'critical': True if points == 0 else False
        }
    
    def calculate_ashtakoot_matching(
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
        Complete Ashtakoot matching calculation
        
        Returns:
            Complete matching report with all 8 Kutas
        """
        # Calculate all 8 Kutas
        varna = self.calculate_varna_kuta(male_moon_sign, female_moon_sign)
        vashya = self.calculate_vashya_kuta(male_moon_sign, female_moon_sign)
        tara = self.calculate_tara_kuta(male_nakshatra_num, female_nakshatra_num)
        yoni = self.calculate_yoni_kuta(male_nakshatra, female_nakshatra)
        graha_maitri = self.calculate_graha_maitri_kuta(male_moon_sign_num, female_moon_sign_num)
        gana = self.calculate_gana_kuta(male_nakshatra, female_nakshatra)
        bhakoot = self.calculate_bhakoot_kuta(male_moon_sign_num, female_moon_sign_num)
        nadi = self.calculate_nadi_kuta(male_nakshatra_num, female_nakshatra_num)
        
        # Calculate total
        total_points = sum([
            varna['points'], vashya['points'], tara['points'], yoni['points'],
            graha_maitri['points'], gana['points'], bhakoot['points'], nadi['points']
        ])
        
        # Determine compatibility level
        if total_points >= 28:
            compatibility = 'Excellent'
            recommendation = 'Highly compatible match'
        elif total_points >= 24:
            compatibility = 'Very Good'
            recommendation = 'Very compatible match'
        elif total_points >= 18:
            compatibility = 'Good'
            recommendation = 'Compatible match with minor adjustments'
        elif total_points >= 12:
            compatibility = 'Average'
            recommendation = 'Moderate compatibility, needs understanding'
        else:
            compatibility = 'Poor'
            recommendation = 'Not recommended without remedies'
        
        # Check critical issues
        critical_issues = []
        if nadi['points'] == 0:
            critical_issues.append('Nadi Dosha present - health and progeny concerns')
        if bhakoot['points'] == 0:
            critical_issues.append('Bhakoot Dosha present - financial concerns')
        if gana['points'] == 0:
            critical_issues.append('Gana Dosha present - temperament conflicts')
        
        return {
            'kutas': {
                'varna': varna,
                'vashya': vashya,
                'tara': tara,
                'yoni': yoni,
                'graha_maitri': graha_maitri,
                'gana': gana,
                'bhakoot': bhakoot,
                'nadi': nadi
            },
            'total_points': round(total_points, 1),
            'max_points': self.TOTAL_MAX_POINTS,
            'percentage': round((total_points / self.TOTAL_MAX_POINTS) * 100, 2),
            'compatibility': compatibility,
            'recommendation': recommendation,
            'critical_issues': critical_issues
        }


# Global instance
ashtakoot_matching = AshtakootMatching()
