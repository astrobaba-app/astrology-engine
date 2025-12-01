"""
Panchang (Vedic Calendar) Calculator
"""
from datetime import datetime, time, timedelta
from typing import Dict, List
import pytz
from app.core.ephemeris import ephemeris


class PanchangCalculator:
    """Calculate Panchang elements"""
    
    # Tithi names
    TITHIS = [
        'Pratipada', 'Dwitiya', 'Tritiya', 'Chaturthi', 'Panchami',
        'Shashthi', 'Saptami', 'Ashtami', 'Navami', 'Dashami',
        'Ekadashi', 'Dwadashi', 'Trayodashi', 'Chaturdashi', 'Purnima/Amavasya'
    ]
    
    # Yoga names
    YOGAS = [
        'Vishkambha', 'Priti', 'Ayushman', 'Saubhagya', 'Shobhana',
        'Atiganda', 'Sukarman', 'Dhriti', 'Shula', 'Ganda',
        'Vriddhi', 'Dhruva', 'Vyaghata', 'Harshana', 'Vajra',
        'Siddhi', 'Vyatipata', 'Variyan', 'Parigha', 'Shiva',
        'Siddha', 'Sadhya', 'Shubha', 'Shukla', 'Brahma',
        'Indra', 'Vaidhriti'
    ]
    
    # Karana names
    KARANAS = [
        'Bava', 'Balava', 'Kaulava', 'Taitila', 'Garaja',
        'Vanija', 'Vishti', 'Shakuni', 'Chatushpada', 'Naga', 'Kimstughna'
    ]
    
    # Nakshatra names
    NAKSHATRAS = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni',
        'Uttara Phalguni', 'Hasta', 'Chitra', 'Swati', 'Vishakha',
        'Anuradha', 'Jyeshtha', 'Mula', 'Purva Ashadha', 'Uttara Ashadha',
        'Shravana', 'Dhanishta', 'Shatabhisha', 'Purva Bhadrapada',
        'Uttara Bhadrapada', 'Revati'
    ]
    
    def calculate_tithi(self, sun_long: float, moon_long: float) -> Dict:
        """
        Calculate Tithi (lunar day)
        
        Args:
            sun_long: Sun's longitude
            moon_long: Moon's longitude
            
        Returns:
            Tithi information
        """
        # Calculate elongation (Moon - Sun)
        elongation = (moon_long - sun_long) % 360
        
        # Each tithi is 12 degrees
        tithi_num = int(elongation / 12)
        tithi_progress = (elongation % 12) / 12 * 100
        
        # Determine paksha (fortnight)
        if tithi_num < 15:
            paksha = 'Shukla' # Bright fortnight
            tithi_in_paksha = tithi_num
        else:
            paksha = 'Krishna'  # Dark fortnight
            tithi_in_paksha = tithi_num - 15
        
        # Get tithi name
        if tithi_in_paksha == 14:
            tithi_name = 'Purnima' if paksha == 'Shukla' else 'Amavasya'
        else:
            tithi_name = self.TITHIS[tithi_in_paksha]
        
        return {
            'number': tithi_num + 1,
            'name': tithi_name,
            'paksha': paksha,
            'progress_percent': round(tithi_progress, 2),
            'elongation': round(elongation, 6)
        }
    
    def calculate_nakshatra(self, moon_long: float) -> Dict:
        """
        Calculate Nakshatra (lunar mansion)
        
        Args:
            moon_long: Moon's longitude
            
        Returns:
            Nakshatra information
        """
        # Each nakshatra is 13°20' (13.333333°)
        nakshatra_num = int(moon_long / 13.333333333333334)
        nakshatra_progress = (moon_long % 13.333333333333334) / 13.333333333333334 * 100
        
        # Calculate pada (quarter)
        pada = int((moon_long % 13.333333333333334) / 3.333333333333333) + 1
        
        # Nakshatra lord
        lords = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
        lord = lords[nakshatra_num % 9]
        
        return {
            'number': nakshatra_num + 1,
            'name': self.NAKSHATRAS[nakshatra_num],
            'pada': pada,
            'lord': lord,
            'progress_percent': round(nakshatra_progress, 2)
        }
    
    def calculate_yoga(self, sun_long: float, moon_long: float) -> Dict:
        """
        Calculate Yoga (Sun + Moon longitude / 13°20')
        
        Args:
            sun_long: Sun's longitude
            moon_long: Moon's longitude
            
        Returns:
            Yoga information
        """
        # Sum of Sun and Moon longitudes
        yoga_sum = (sun_long + moon_long) % 360
        
        # Each yoga is 13°20' (13.333333°)
        yoga_num = int(yoga_sum / 13.333333333333334)
        yoga_progress = (yoga_sum % 13.333333333333334) / 13.333333333333334 * 100
        
        return {
            'number': yoga_num + 1,
            'name': self.YOGAS[yoga_num],
            'progress_percent': round(yoga_progress, 2)
        }
    
    def calculate_karana(self, sun_long: float, moon_long: float) -> Dict:
        """
        Calculate Karana (half of tithi)
        
        Args:
            sun_long: Sun's longitude
            moon_long: Moon's longitude
            
        Returns:
            Karana information
        """
        # Calculate elongation
        elongation = (moon_long - sun_long) % 360
        
        # Each karana is 6 degrees (half of tithi)
        karana_num = int(elongation / 6)
        karana_progress = (elongation % 6) / 6 * 100
        
        # First 7 karanas repeat 8 times, last 4 occur once
        if karana_num < 57:
            karana_index = karana_num % 7
        else:
            karana_index = 7 + (karana_num - 57)
        
        return {
            'number': karana_num + 1,
            'name': self.KARANAS[karana_index],
            'progress_percent': round(karana_progress, 2)
        }
    
    def calculate_rahu_kaal(
        self,
        date: datetime,
        latitude: float,
        longitude: float,
        timezone: str
    ) -> Dict:
        """
        Calculate Rahu Kaal (inauspicious period)
        
        Args:
            date: Date for calculation
            latitude: Location latitude
            longitude: Location longitude
            timezone: Timezone string
            
        Returns:
            Rahu Kaal timing
        """
        # Get sunrise and sunset
        sunrise_time = self._get_sunrise(date, latitude, longitude, timezone)
        sunset_time = self._get_sunset(date, latitude, longitude, timezone)
        
        # Calculate day duration
        day_duration = (sunset_time - sunrise_time).total_seconds() / 3600
        
        # Rahu Kaal is 1/8th of the day
        rahu_duration = day_duration / 8
        
        # Day of week (0 = Monday)
        day_of_week = date.weekday()
        
        # Rahu Kaal position by weekday (which 1/8th period)
        # Mon=8th, Tue=7th, Wed=5th, Thu=6th, Fri=4th, Sat=1st, Sun=2nd
        rahu_positions = {
            0: 7,  # Monday - 8th period (index 7)
            1: 6,  # Tuesday - 7th period
            2: 4,  # Wednesday - 5th period
            3: 5,  # Thursday - 6th period
            4: 3,  # Friday - 4th period
            5: 0,  # Saturday - 1st period
            6: 1   # Sunday - 2nd period
        }
        
        position = rahu_positions[day_of_week]
        
        # Calculate start time
        rahu_start = sunrise_time + timedelta(hours=position * rahu_duration)
        rahu_end = rahu_start + timedelta(hours=rahu_duration)
        
        return {
            'start': rahu_start.strftime('%H:%M:%S'),
            'end': rahu_end.strftime('%H:%M:%S'),
            'duration_minutes': round(rahu_duration * 60, 0)
        }
    
    def calculate_gulika_kaal(
        self,
        date: datetime,
        latitude: float,
        longitude: float,
        timezone: str
    ) -> Dict:
        """
        Calculate Gulika Kaal (son of Saturn period)
        
        Args:
            date: Date for calculation
            latitude: Location latitude
            longitude: Location longitude
            timezone: Timezone string
            
        Returns:
            Gulika Kaal timing
        """
        # Get sunrise and sunset
        sunrise_time = self._get_sunrise(date, latitude, longitude, timezone)
        sunset_time = self._get_sunset(date, latitude, longitude, timezone)
        
        # Calculate day duration
        day_duration = (sunset_time - sunrise_time).total_seconds() / 3600
        
        # Gulika Kaal is 1/8th of the day
        gulika_duration = day_duration / 8
        
        # Day of week
        day_of_week = date.weekday()
        
        # Gulika Kaal position by weekday
        # Mon=7th, Tue=6th, Wed=5th, Thu=4th, Fri=3rd, Sat=2nd, Sun=1st
        gulika_positions = {
            0: 6,  # Monday
            1: 5,  # Tuesday
            2: 4,  # Wednesday
            3: 3,  # Thursday
            4: 2,  # Friday
            5: 1,  # Saturday
            6: 0   # Sunday
        }
        
        position = gulika_positions[day_of_week]
        
        # Calculate start time
        gulika_start = sunrise_time + timedelta(hours=position * gulika_duration)
        gulika_end = gulika_start + timedelta(hours=gulika_duration)
        
        return {
            'start': gulika_start.strftime('%H:%M:%S'),
            'end': gulika_end.strftime('%H:%M:%S'),
            'duration_minutes': round(gulika_duration * 60, 0)
        }
    
    def _get_sunrise(
        self,
        date: datetime,
        latitude: float,
        longitude: float,
        timezone: str
    ) -> datetime:
        """Calculate sunrise time (simplified)"""
        # Combine date with approximate sunrise time (6 AM)
        sunrise_guess = datetime.combine(date.date(), time(6, 0))
        tz = pytz.timezone(timezone)
        sunrise_guess = tz.localize(sunrise_guess)
        
        # For production, use more accurate calculation
        # This is a placeholder - actual calculation would use Swiss Ephemeris
        return sunrise_guess
    
    def _get_sunset(
        self,
        date: datetime,
        latitude: float,
        longitude: float,
        timezone: str
    ) -> datetime:
        """Calculate sunset time (simplified)"""
        # Combine date with approximate sunset time (6 PM)
        sunset_guess = datetime.combine(date.date(), time(18, 0))
        tz = pytz.timezone(timezone)
        sunset_guess = tz.localize(sunset_guess)
        
        # For production, use more accurate calculation
        return sunset_guess
    
    def calculate_panchang(
        self,
        date: datetime,
        latitude: float,
        longitude: float,
        timezone: str
    ) -> Dict:
        """
        Calculate complete Panchang for a given date and location
        
        Args:
            date: Date for panchang
            latitude: Location latitude
            longitude: Location longitude
            timezone: Timezone string
            
        Returns:
            Complete Panchang data
        """
        # Get Julian Day
        jd = ephemeris.get_julian_day(date, timezone)
        
        # Get Sun and Moon positions
        sun = ephemeris.get_planet_position('Sun', jd)
        moon = ephemeris.get_planet_position('Moon', jd)
        
        # Calculate all panchang elements
        tithi = self.calculate_tithi(sun['longitude'], moon['longitude'])
        nakshatra = self.calculate_nakshatra(moon['longitude'])
        yoga = self.calculate_yoga(sun['longitude'], moon['longitude'])
        karana = self.calculate_karana(sun['longitude'], moon['longitude'])
        
        # Calculate inauspicious periods
        rahu_kaal = self.calculate_rahu_kaal(date, latitude, longitude, timezone)
        gulika_kaal = self.calculate_gulika_kaal(date, latitude, longitude, timezone)
        
        # Weekday
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        weekday = weekdays[date.weekday()]
        
        # Sunrise/Sunset (simplified)
        sunrise = self._get_sunrise(date, latitude, longitude, timezone)
        sunset = self._get_sunset(date, latitude, longitude, timezone)
        
        return {
            'date': date.strftime('%Y-%m-%d'),
            'weekday': weekday,
            'sunrise': sunrise.strftime('%H:%M:%S'),
            'sunset': sunset.strftime('%H:%M:%S'),
            'tithi': tithi,
            'nakshatra': nakshatra,
            'yoga': yoga,
            'karana': karana,
            'rahu_kaal': rahu_kaal,
            'gulika_kaal': gulika_kaal,
            'sun': {
                'longitude': sun['longitude'],
                'sign': sun['sign'],
                'nakshatra': sun['nakshatra']
            },
            'moon': {
                'longitude': moon['longitude'],
                'sign': moon['sign'],
                'nakshatra': moon['nakshatra']
            }
        }


# Global instance
panchang_calculator = PanchangCalculator()
