"""
Dasha (Planetary Period) Calculator
"""
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
from dateutil.relativedelta import relativedelta


class DashaCalculator:
    """Calculate Vimshottari and other Dasha systems"""
    
    # Vimshottari Dasha periods (in years)
    VIMSHOTTARI_PERIODS = {
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
    
    # Vimshottari Dasha sequence
    VIMSHOTTARI_SEQUENCE = [
        'Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 
        'Rahu', 'Jupiter', 'Saturn', 'Mercury'
    ]
    
    # Nakshatra lords (0-26)
    NAKSHATRA_LORDS = [
        'Ketu',    # 0: Ashwini
        'Venus',   # 1: Bharani
        'Sun',     # 2: Krittika
        'Moon',    # 3: Rohini
        'Mars',    # 4: Mrigashira
        'Rahu',    # 5: Ardra
        'Jupiter', # 6: Punarvasu
        'Saturn',  # 7: Pushya
        'Mercury', # 8: Ashlesha
        'Ketu',    # 9: Magha
        'Venus',   # 10: Purva Phalguni
        'Sun',     # 11: Uttara Phalguni
        'Moon',    # 12: Hasta
        'Mars',    # 13: Chitra
        'Rahu',    # 14: Swati
        'Jupiter', # 15: Vishakha
        'Saturn',  # 16: Anuradha
        'Mercury', # 17: Jyeshtha
        'Ketu',    # 18: Mula
        'Venus',   # 19: Purva Ashadha
        'Sun',     # 20: Uttara Ashadha
        'Moon',    # 21: Shravana
        'Mars',    # 22: Dhanishta
        'Rahu',    # 23: Shatabhisha
        'Jupiter', # 24: Purva Bhadrapada
        'Saturn',  # 25: Uttara Bhadrapada
        'Mercury'  # 26: Revati
    ]
    
    def get_moon_nakshatra(self, moon_longitude: float) -> Tuple[int, str, float]:
        """
        Get Moon's nakshatra details
        
        Returns:
            (nakshatra_num, nakshatra_name, balance_percent)
        """
        nakshatra_num = int(moon_longitude / 13.333333333333334)
        nakshatra_degree = moon_longitude % 13.333333333333334
        balance_percent = 1 - (nakshatra_degree / 13.333333333333334)
        
        nakshatras = [
            'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
            'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 
            'Uttara Phalguni', 'Hasta', 'Chitra', 'Swati', 'Vishakha',
            'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha', 'Uttara Ashadha',
            'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
            'Uttara Bhadrapada', 'Revati'
        ]
        
        return nakshatra_num, nakshatras[nakshatra_num], balance_percent
    
    def calculate_vimshottari_dasha(
        self,
        moon_longitude: float,
        birth_date: datetime,
        years: int = 120
    ) -> Dict:
        """
        Calculate Vimshottari Dasha periods
        
        Args:
            moon_longitude: Moon's longitude at birth
            birth_date: Date and time of birth
            years: Number of years to calculate (default 120 - full cycle)
            
        Returns:
            Complete dasha timeline
        """
        # Get birth nakshatra and balance
        nak_num, nak_name, balance = self.get_moon_nakshatra(moon_longitude)
        
        # Get birth dasha lord
        birth_dasha_lord = self.NAKSHATRA_LORDS[nak_num]
        
        # Calculate balance of birth dasha
        birth_dasha_years = self.VIMSHOTTARI_PERIODS[birth_dasha_lord]
        balance_years = birth_dasha_years * balance
        balance_days = balance_years * 365.25
        
        # Start calculating dashas
        dashas = []
        current_date = birth_date
        
        # Find starting position in sequence
        start_index = self.VIMSHOTTARI_SEQUENCE.index(birth_dasha_lord)
        
        # First dasha (balance period)
        end_date = current_date + timedelta(days=balance_days)
        dashas.append({
            'planet': birth_dasha_lord,
            'start_date': current_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'years': round(balance_years, 2),
            'is_balance': True
        })
        current_date = end_date
        
        # Calculate remaining dashas
        total_years_calculated = balance_years
        sequence_index = (start_index + 1) % 9
        
        while total_years_calculated < years:
            planet = self.VIMSHOTTARI_SEQUENCE[sequence_index]
            period_years = self.VIMSHOTTARI_PERIODS[planet]
            
            if total_years_calculated + period_years > years:
                period_years = years - total_years_calculated
            
            period_days = period_years * 365.25
            end_date = current_date + timedelta(days=period_days)
            
            dashas.append({
                'planet': planet,
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'years': round(period_years, 2),
                'is_balance': False
            })
            
            current_date = end_date
            total_years_calculated += period_years
            sequence_index = (sequence_index + 1) % 9
        
        return {
            'system': 'Vimshottari',
            'birth_nakshatra': nak_name,
            'birth_nakshatra_lord': birth_dasha_lord,
            'balance_at_birth': f"{round(balance * 100, 2)}%",
            'dashas': dashas
        }
    
    def calculate_antardasha(
        self,
        maha_dasha_lord: str,
        maha_dasha_start: datetime,
        maha_dasha_years: float
    ) -> List[Dict]:
        """
        Calculate Antardasha (sub-periods) within a Mahadasha
        
        Args:
            maha_dasha_lord: Planet ruling the Mahadasha
            maha_dasha_start: Start date of Mahadasha
            maha_dasha_years: Duration of Mahadasha in years
            
        Returns:
            List of Antardasha periods
        """
        antardashas = []
        
        # Find starting position in sequence
        start_index = self.VIMSHOTTARI_SEQUENCE.index(maha_dasha_lord)
        
        # Total proportional units for Mahadasha
        maha_period = self.VIMSHOTTARI_PERIODS[maha_dasha_lord]
        
        current_date = maha_dasha_start
        
        for i in range(9):
            planet_index = (start_index + i) % 9
            antar_lord = self.VIMSHOTTARI_SEQUENCE[planet_index]
            
            # Calculate proportional period
            antar_period = self.VIMSHOTTARI_PERIODS[antar_lord]
            antar_years = (maha_dasha_years * antar_period) / maha_period
            antar_days = antar_years * 365.25
            
            end_date = current_date + timedelta(days=antar_days)
            
            antardashas.append({
                'maha_dasha_lord': maha_dasha_lord,
                'antar_dasha_lord': antar_lord,
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'years': round(antar_years, 4),
                'months': round(antar_years * 12, 2),
                'days': round(antar_days, 0)
            })
            
            current_date = end_date
        
        return antardashas
    
    def calculate_pratyantar_dasha(
        self,
        maha_dasha_lord: str,
        antar_dasha_lord: str,
        antar_dasha_start: datetime,
        antar_dasha_years: float
    ) -> List[Dict]:
        """
        Calculate Pratyantardasha (sub-sub-periods) within an Antardasha
        
        Args:
            maha_dasha_lord: Planet ruling the Mahadasha
            antar_dasha_lord: Planet ruling the Antardasha
            antar_dasha_start: Start date of Antardasha
            antar_dasha_years: Duration of Antardasha in years
            
        Returns:
            List of Pratyantardasha periods
        """
        pratyantardashas = []
        
        # Find starting position in sequence
        start_index = self.VIMSHOTTARI_SEQUENCE.index(antar_dasha_lord)
        
        # Total proportional units for Antardasha
        antar_period = self.VIMSHOTTARI_PERIODS[antar_dasha_lord]
        
        current_date = antar_dasha_start
        
        for i in range(9):
            planet_index = (start_index + i) % 9
            pratyantar_lord = self.VIMSHOTTARI_SEQUENCE[planet_index]
            
            # Calculate proportional period
            pratyantar_period = self.VIMSHOTTARI_PERIODS[pratyantar_lord]
            pratyantar_years = (antar_dasha_years * pratyantar_period) / antar_period
            pratyantar_days = pratyantar_years * 365.25
            
            end_date = current_date + timedelta(days=pratyantar_days)
            
            pratyantardashas.append({
                'maha_dasha_lord': maha_dasha_lord,
                'antar_dasha_lord': antar_dasha_lord,
                'pratyantar_dasha_lord': pratyantar_lord,
                'start_date': current_date.strftime('%Y-%m-%d'),
                'end_date': end_date.strftime('%Y-%m-%d'),
                'years': round(pratyantar_years, 6),
                'months': round(pratyantar_years * 12, 4),
                'days': round(pratyantar_days, 1)
            })
            
            current_date = end_date
        
        return pratyantardashas
    
    def get_current_dasha(
        self,
        dashas: List[Dict],
        current_date: datetime = None
    ) -> Dict:
        """
        Get current running dasha for a given date
        
        Args:
            dashas: List of dasha periods
            current_date: Date to check (default: today)
            
        Returns:
            Current dasha information
        """
        if current_date is None:
            current_date = datetime.now()
        
        current_date_str = current_date.strftime('%Y-%m-%d')
        
        for dasha in dashas:
            if dasha['start_date'] <= current_date_str <= dasha['end_date']:
                # Calculate remaining time
                end_date = datetime.strptime(dasha['end_date'], '%Y-%m-%d')
                remaining_days = (end_date - current_date).days
                
                return {
                    **dasha,
                    'is_current': True,
                    'remaining_days': remaining_days,
                    'remaining_years': round(remaining_days / 365.25, 2)
                }
        
        return None


# Global instance
dasha_calculator = DashaCalculator()
