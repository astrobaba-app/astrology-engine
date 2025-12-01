"""
Transit-based Horoscope Predictions
"""
from datetime import datetime, timedelta
from typing import Dict, List
import swisseph as swe


class TransitHoroscope:
    """Generate transit-based horoscopes for different time periods"""
    
    # Zodiac sign ranges
    SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer',
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    def __init__(self, ephemeris_path: str = './ephemeris_data'):
        swe.set_ephe_path(ephemeris_path)
    
    def _get_sign_from_longitude(self, longitude: float) -> str:
        """Get zodiac sign from longitude"""
        sign_num = int(longitude / 30)
        return self.SIGNS[sign_num % 12]
    
    def _get_planet_position(self, jd: float, planet: int) -> Dict:
        """Get planet position for given Julian day"""
        result = swe.calc_ut(jd, planet)
        # result is a tuple: (longitude, latitude, distance, speed_long, speed_lat, speed_dist)
        longitude = result[0][0] if isinstance(result[0], tuple) else result[0]
        return {
            'longitude': longitude,
            'sign': self._get_sign_from_longitude(longitude),
            'degree': longitude % 30
        }
    
    def _get_all_transits(self, date: datetime) -> Dict:
        """Get all planetary transits for a given date"""
        jd = swe.julday(date.year, date.month, date.day, date.hour + date.minute/60.0)
        
        planets = {
            'Sun': swe.SUN,
            'Moon': swe.MOON,
            'Mars': swe.MARS,
            'Mercury': swe.MERCURY,
            'Jupiter': swe.JUPITER,
            'Venus': swe.VENUS,
            'Saturn': swe.SATURN
        }
        
        transits = {}
        for name, planet_id in planets.items():
            transits[name] = self._get_planet_position(jd, planet_id)
        
        return transits
    
    def generate_daily_horoscope(self, zodiac_sign: str, date: datetime = None) -> Dict:
        """
        Generate daily horoscope for a zodiac sign
        
        Args:
            zodiac_sign: Aries, Taurus, etc.
            date: Date for horoscope (default: today)
        """
        if date is None:
            date = datetime.now()
        
        transits = self._get_all_transits(date)
        
        # Analyze transits for the sign
        predictions = self._analyze_daily_transits(zodiac_sign, transits, date)
        
        return {
            'sign': zodiac_sign,
            'date': date.strftime('%Y-%m-%d'),
            'period': 'Daily',
            'transits': transits,
            'predictions': predictions,
            'lucky_color': self._get_lucky_color(transits),
            'lucky_number': self._get_lucky_number(transits),
            'lucky_time': self._get_lucky_time(transits)
        }
    
    def generate_weekly_horoscope(self, zodiac_sign: str, start_date: datetime = None) -> Dict:
        """Generate weekly horoscope"""
        if start_date is None:
            start_date = datetime.now()
        
        end_date = start_date + timedelta(days=7)
        
        # Get transits for start and end of week
        start_transits = self._get_all_transits(start_date)
        end_transits = self._get_all_transits(end_date)
        
        predictions = self._analyze_weekly_transits(zodiac_sign, start_transits, end_transits, start_date)
        
        return {
            'sign': zodiac_sign,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'period': 'Weekly',
            'key_transits': start_transits,
            'predictions': predictions,
            'lucky_days': self._get_lucky_days_of_week(start_transits)
        }
    
    def generate_monthly_horoscope(self, zodiac_sign: str, year: int = None, month: int = None) -> Dict:
        """Generate monthly horoscope"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        start_transits = self._get_all_transits(start_date)
        mid_transits = self._get_all_transits(start_date + timedelta(days=15))
        end_transits = self._get_all_transits(end_date)
        
        predictions = self._analyze_monthly_transits(zodiac_sign, start_transits, mid_transits, end_transits, start_date)
        
        return {
            'sign': zodiac_sign,
            'month': start_date.strftime('%B %Y'),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'period': 'Monthly',
            'key_transits': {
                'start': start_transits,
                'mid': mid_transits,
                'end': end_transits
            },
            'predictions': predictions,
            'best_dates': self._get_best_dates_of_month(start_date, start_transits)
        }
    
    def generate_yearly_horoscope(self, zodiac_sign: str, year: int = None) -> Dict:
        """Generate yearly horoscope"""
        if year is None:
            year = datetime.now().year
        
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        
        # Get quarterly transits
        q1_transits = self._get_all_transits(datetime(year, 1, 1))
        q2_transits = self._get_all_transits(datetime(year, 4, 1))
        q3_transits = self._get_all_transits(datetime(year, 7, 1))
        q4_transits = self._get_all_transits(datetime(year, 10, 1))
        
        predictions = self._analyze_yearly_transits(zodiac_sign, q1_transits, q2_transits, q3_transits, q4_transits, year)
        
        return {
            'sign': zodiac_sign,
            'year': year,
            'period': 'Yearly',
            'quarterly_transits': {
                'Q1': q1_transits,
                'Q2': q2_transits,
                'Q3': q3_transits,
                'Q4': q4_transits
            },
            'predictions': predictions,
            'best_months': self._get_best_months(year, zodiac_sign)
        }
    
    def _analyze_daily_transits(self, sign: str, transits: Dict, date: datetime) -> Dict:
        """Analyze transits for daily predictions"""
        return {
            'overall': self._get_daily_overall(sign, transits),
            'love': self._get_daily_love(sign, transits),
            'career': self._get_daily_career(sign, transits),
            'health': self._get_daily_health(sign, transits),
            'finance': self._get_daily_finance(sign, transits),
            'rating': self._calculate_day_rating(sign, transits)
        }
    
    def _analyze_weekly_transits(self, sign: str, start: Dict, end: Dict, date: datetime) -> Dict:
        """Analyze transits for weekly predictions"""
        return {
            'overview': f"This week brings dynamic energy for {sign}. Pay attention to planetary movements.",
            'love': "Venus influences bring romantic opportunities. Be open to connections.",
            'career': "Professional matters require attention. Good time for important decisions.",
            'health': "Maintain balanced routine. Energy levels may fluctuate mid-week.",
            'finance': "Financial stability expected. Avoid impulsive spending.",
            'advice': "Stay focused on goals and maintain positive attitude."
        }
    
    def _analyze_monthly_transits(self, sign: str, start: Dict, mid: Dict, end: Dict, date: datetime) -> Dict:
        """Analyze transits for monthly predictions"""
        return {
            'overview': f"{date.strftime('%B')} brings transformative energy for {sign}. Major planetary transits influence all life areas.",
            'first_half': "Early month favors new beginnings. Take initiative in important matters.",
            'second_half': "Mid-to-late month brings results. Time to harvest what you've sown.",
            'love': "Relationships deepen. Single natives may meet significant people.",
            'career': "Professional growth opportunities arise. Network and showcase talents.",
            'health': "Overall health good. Maintain regular exercise and diet.",
            'finance': "Financial improvements possible. Good time for investments.",
            'advice': "Balance ambition with patience. Success comes through persistence."
        }
    
    def _analyze_yearly_transits(self, sign: str, q1: Dict, q2: Dict, q3: Dict, q4: Dict, year: int) -> Dict:
        """Analyze transits for yearly predictions"""
        return {
            'overview': f"{year} is a significant year for {sign}. Major planetary movements shape your destiny.",
            'Q1': "First quarter focuses on foundations. Set clear goals and work steadily.",
            'Q2': "Second quarter brings action. Opportunities multiply, be ready to seize them.",
            'Q3': "Third quarter emphasizes relationships. Partnerships become crucial.",
            'Q4': "Fourth quarter brings completion. Harvest results and plan ahead.",
            'love_relationships': "Year favors deeper connections. Committed relationships strengthen significantly.",
            'career_business': "Professional advancement likely. New opportunities and recognition coming.",
            'health_wellness': "Generally favorable. Regular checkups and healthy lifestyle important.",
            'finance_wealth': "Financial growth indicated. Smart investments and savings recommended.",
            'key_dates': f"January-March, June-August are especially favorable for {sign}.",
            'overall_advice': "Year of growth and transformation. Stay positive, work hard, and trust the process."
        }
    
    # Helper methods
    def _get_daily_overall(self, sign: str, transits: Dict) -> str:
        return f"Today brings balanced energy for {sign}. Planetary positions favor steady progress."
    
    def _get_daily_love(self, sign: str, transits: Dict) -> str:
        return "Romantic energy is positive. Good day for expressing feelings and strengthening bonds."
    
    def _get_daily_career(self, sign: str, transits: Dict) -> str:
        return "Professional matters proceed smoothly. Good day for important meetings and decisions."
    
    def _get_daily_health(self, sign: str, transits: Dict) -> str:
        return "Health and vitality are good. Maintain regular routine and stay hydrated."
    
    def _get_daily_finance(self, sign: str, transits: Dict) -> str:
        return "Financial matters are stable. Good day for planning and budgeting."
    
    def _calculate_day_rating(self, sign: str, transits: Dict) -> str:
        return "4/5 ⭐⭐⭐⭐"
    
    def _get_lucky_color(self, transits: Dict) -> str:
        colors = ['Red', 'Blue', 'Green', 'Yellow', 'Purple', 'Orange', 'White', 'Gold']
        sun_sign = self.SIGNS.index(transits['Sun']['sign'])
        return colors[sun_sign % len(colors)]
    
    def _get_lucky_number(self, transits: Dict) -> int:
        moon_degree = int(transits['Moon']['degree'])
        return (moon_degree % 9) + 1
    
    def _get_lucky_time(self, transits: Dict) -> str:
        return "10:00 AM - 12:00 PM, 4:00 PM - 6:00 PM"
    
    def _get_lucky_days_of_week(self, transits: Dict) -> List[str]:
        return ["Tuesday", "Friday", "Sunday"]
    
    def _get_best_dates_of_month(self, start_date: datetime, transits: Dict) -> List[str]:
        dates = []
        for day in [5, 10, 15, 20, 25]:
            date = start_date.replace(day=day)
            dates.append(date.strftime('%Y-%m-%d'))
        return dates[:3]
    
    def _get_best_months(self, year: int, sign: str) -> List[str]:
        return ["March", "June", "September", "November"]


# Global instance
transit_horoscope = TransitHoroscope()
