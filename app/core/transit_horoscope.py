"""
Transit-based Horoscope Predictions with Professional Accuracy
"""
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import swisseph as swe


class TransitHoroscope:
    """Generate professional-grade transit-based horoscopes"""
    
    # Zodiac sign ranges
    SIGNS = [
        'Aries', 'Taurus', 'Gemini', 'Cancer',
        'Leo', 'Virgo', 'Libra', 'Scorpio',
        'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
    ]
    
    # Sign characteristics for predictions
    SIGN_LORDS = {
        'Aries': 'Mars', 'Taurus': 'Venus', 'Gemini': 'Mercury',
        'Cancer': 'Moon', 'Leo': 'Sun', 'Virgo': 'Mercury',
        'Libra': 'Venus', 'Scorpio': 'Mars', 'Sagittarius': 'Jupiter',
        'Capricorn': 'Saturn', 'Aquarius': 'Saturn', 'Pisces': 'Jupiter'
    }
    
    # Planet speeds and effects
    PLANET_NATURE = {
        'Sun': 'Soul, Authority, Father, Government',
        'Moon': 'Mind, Emotions, Mother, Public',
        'Mars': 'Energy, Courage, Conflicts, Property',
        'Mercury': 'Intelligence, Communication, Business',
        'Jupiter': 'Wisdom, Fortune, Growth, Children',
        'Venus': 'Love, Luxury, Relationships, Arts',
        'Saturn': 'Discipline, Delays, Hard Work, Karma'
    }
    
    # Nakshatra data for precise predictions
    NAKSHATRAS = [
        'Ashwini', 'Bharani', 'Krittika', 'Rohini', 'Mrigashira', 'Ardra',
        'Punarvasu', 'Pushya', 'Ashlesha', 'Magha', 'Purva Phalguni', 'Uttara Phalguni',
        'Hasta', 'Chitra', 'Swati', 'Vishakha', 'Anuradha', 'Jyeshtha',
        'Mula', 'Purva Ashadha', 'Uttara Ashadha', 'Shravana', 'Dhanishta', 'Shatabhisha',
        'Purva Bhadrapada', 'Uttara Bhadrapada', 'Revati'
    ]
    
    def __init__(self, ephemeris_path: str = './ephemeris_data'):
        swe.set_ephe_path(ephemeris_path)
        swe.set_sid_mode(swe.SIDM_LAHIRI)  # Vedic/Sidereal mode
    
    def _get_sign_from_longitude(self, longitude: float) -> str:
        """Get zodiac sign from longitude"""
        sign_num = int(longitude / 30)
        return self.SIGNS[sign_num % 12]
    
    def _get_nakshatra_from_longitude(self, longitude: float) -> Dict:
        """Get nakshatra details from longitude"""
        nakshatra_span = 360 / 27
        nakshatra_num = int(longitude / nakshatra_span)
        pada = int((longitude % nakshatra_span) / (nakshatra_span / 4)) + 1
        
        return {
            'name': self.NAKSHATRAS[nakshatra_num % 27],
            'number': nakshatra_num + 1,
            'pada': pada,
            'lord': self._get_nakshatra_lord(nakshatra_num)
        }
    
    def _get_nakshatra_lord(self, nakshatra_num: int) -> str:
        """Get nakshatra lord based on Vimshottari Dasha system"""
        lords = ['Ketu', 'Venus', 'Sun', 'Moon', 'Mars', 'Rahu', 'Jupiter', 'Saturn', 'Mercury']
        return lords[nakshatra_num % 9]
    
    def _get_planet_position(self, jd: float, planet: int) -> Dict:
        """Get planet position for given Julian day"""
        result = swe.calc_ut(jd, planet, swe.FLG_SIDEREAL)
        longitude = result[0][0] if isinstance(result[0], tuple) else result[0]
        latitude = result[0][1] if isinstance(result[0], tuple) else result[1]
        speed = result[0][3] if isinstance(result[0], tuple) else result[3]
        
        return {
            'longitude': longitude,
            'latitude': latitude,
            'speed': speed,
            'sign': self._get_sign_from_longitude(longitude),
            'degree': longitude % 30,
            'nakshatra': self._get_nakshatra_from_longitude(longitude),
            'is_retrograde': speed < 0
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
            'Saturn': swe.SATURN,
            'Rahu': swe.MEAN_NODE,
            'Ketu': swe.MEAN_NODE  # Ketu is 180° opposite to Rahu
        }
        
        transits = {}
        for name, planet_id in planets.items():
            pos = self._get_planet_position(jd, planet_id)
            if name == 'Ketu':
                # Ketu is exactly opposite to Rahu
                pos['longitude'] = (pos['longitude'] + 180) % 360
                pos['sign'] = self._get_sign_from_longitude(pos['longitude'])
                pos['degree'] = pos['longitude'] % 30
                pos['nakshatra'] = self._get_nakshatra_from_longitude(pos['longitude'])
            transits[name] = pos
        
        return transits
    
    def _get_moon_phase(self, sun_long: float, moon_long: float) -> str:
        """Calculate moon phase"""
        diff = (moon_long - sun_long) % 360
        if diff < 45: return 'New Moon'
        elif diff < 90: return 'Waxing Crescent'
        elif diff < 135: return 'First Quarter'
        elif diff < 180: return 'Waxing Gibbous'
        elif diff < 225: return 'Full Moon'
        elif diff < 270: return 'Waning Gibbous'
        elif diff < 315: return 'Last Quarter'
        else: return 'Waning Crescent'
    
    def _calculate_transit_strength(self, sign: str, transits: Dict) -> Dict:
        """Calculate how strong transits are for a sign"""
        sign_lord = self.SIGN_LORDS[sign]
        sign_num = self.SIGNS.index(sign)
        
        strengths = {}
        for planet, pos in transits.items():
            if planet in ['Rahu', 'Ketu']:
                continue
            
            planet_sign_num = self.SIGNS.index(pos['sign'])
            
            # Calculate house position from natal sign
            house_from_sign = ((planet_sign_num - sign_num) % 12) + 1
            
            # Beneficial houses: 1, 2, 3, 5, 7, 9, 10, 11
            # Challenging houses: 4, 6, 8, 12
            if house_from_sign in [1, 5, 9, 10, 11]:
                strengths[planet] = 'Highly Beneficial'
            elif house_from_sign in [2, 3, 7]:
                strengths[planet] = 'Beneficial'
            elif house_from_sign in [6, 8, 12]:
                strengths[planet] = 'Challenging'
            else:
                strengths[planet] = 'Neutral'
        
        return strengths
    
    def _analyze_daily_transits_professional(
        self, zodiac_sign: str, transits: Dict, strengths: Dict, date: datetime
    ) -> Dict:
        """Generate professional-level daily predictions using Vedic principles"""
        
        sign_num = self.SIGNS.index(zodiac_sign)
        sign_lord = self.SIGN_LORDS[zodiac_sign]
        
        # Analyze each area with depth
        overall_rating = 0
        total_factors = 0
        
        # 1. Career & Professional Life
        career_score = 0
        career_factors = []
        
        # Sun (authority, father, government) in 10th house (career)
        sun_sign_num = self.SIGNS.index(transits['Sun']['sign'])
        sun_house = ((sun_sign_num - sign_num) % 12) + 1
        
        if sun_house == 10:
            career_factors.append("Sun in 10th house brings career recognition")
            career_score += 4
        elif sun_house in [1, 5, 9, 11]:
            career_factors.append("Favorable Sun transit supports professional growth")
            career_score += 3
        elif sun_house in [6, 8, 12]:
            career_factors.append("Sun transit may bring work challenges")
            career_score += 1
        else:
            career_score += 2
        
        # Saturn (work, responsibility) effects
        saturn_sign_num = self.SIGNS.index(transits['Saturn']['sign'])
        saturn_house = ((saturn_sign_num - sign_num) % 12) + 1
        
        if transits['Saturn']['is_retrograde']:
            career_factors.append("Retrograde Saturn: Review past work decisions")
            career_score += 1
        elif saturn_house in [3, 6, 10, 11]:
            career_factors.append("Saturn transit favors hard work and discipline")
            career_score += 3
        elif saturn_house in [1, 4, 7, 8, 12]:
            career_factors.append("Saturn may bring delays in professional matters")
            career_score += 1
        else:
            career_score += 2
        
        # Jupiter (growth, expansion) effects
        jupiter_sign_num = self.SIGNS.index(transits['Jupiter']['sign'])
        jupiter_house = ((jupiter_sign_num - sign_num) % 12) + 1
        
        if jupiter_house in [1, 2, 5, 9, 10, 11]:
            career_factors.append("Jupiter's blessings enhance opportunities")
            career_score += 3
        
        # 2. Love & Relationships
        love_score = 0
        love_factors = []
        
        # Venus (love, relationships)
        venus_sign_num = self.SIGNS.index(transits['Venus']['sign'])
        venus_house = ((venus_sign_num - sign_num) % 12) + 1
        
        if venus_house in [1, 5, 7, 11]:
            love_factors.append("Venus enhances romantic prospects")
            love_score += 4
        elif venus_house in [2, 4, 9]:
            love_factors.append("Favorable time for relationships")
            love_score += 3
        elif venus_house in [6, 8, 12]:
            love_factors.append("Exercise patience in relationships")
            love_score += 1
        else:
            love_score += 2
        
        if transits['Venus']['is_retrograde']:
            love_factors.append("Venus retrograde: Reflect on past relationships")
            love_score = max(2, love_score - 1)
        
        # Moon (emotions, mind)
        moon_nakshatra = transits['Moon']['nakshatra']['name']
        if transits['Moon']['nakshatra']['lord'] == sign_lord:
            love_factors.append(f"Moon in {moon_nakshatra} nakshatra supports emotional harmony")
            love_score += 2
        
        # 3. Health & Wellness
        health_score = 0
        health_factors = []
        
        # Moon (mind) and Mars (energy) for health
        mars_sign_num = self.SIGNS.index(transits['Mars']['sign'])
        mars_house = ((mars_sign_num - sign_num) % 12) + 1
        
        if mars_house in [1, 6, 8, 12]:
            health_factors.append("Mars position advises caution with health")
            health_score += 1
        elif mars_house in [3, 10, 11]:
            health_factors.append("Good energy levels and vitality")
            health_score += 4
        else:
            health_score += 3
        
        # Moon for mental health
        moon_sign_num = self.SIGNS.index(transits['Moon']['sign'])
        moon_house = ((moon_sign_num - sign_num) % 12) + 1
        
        if moon_house in [1, 4, 5, 9]:
            health_factors.append("Moon placement supports mental peace")
            health_score += 3
        elif moon_house in [6, 8, 12]:
            health_factors.append("Focus on stress management")
            health_score += 1
        else:
            health_score += 2
        
        # 4. Finance & Wealth
        finance_score = 0
        finance_factors = []
        
        # Jupiter (wealth) and Venus (luxury)
        if jupiter_house in [1, 2, 5, 9, 11]:
            finance_factors.append("Jupiter supports financial growth")
            finance_score += 4
        elif jupiter_house in [8, 12]:
            finance_factors.append("Avoid major financial decisions")
            finance_score += 1
        else:
            finance_score += 2
        
        if venus_house in [2, 11]:
            finance_factors.append("Venus favors monetary gains")
            finance_score += 3
        
        # Mercury (business, trade)
        mercury_sign_num = self.SIGNS.index(transits['Mercury']['sign'])
        mercury_house = ((mercury_sign_num - sign_num) % 12) + 1
        
        if mercury_house in [2, 3, 10, 11]:
            finance_factors.append("Good time for business and trade")
            finance_score += 3
        elif transits['Mercury']['is_retrograde']:
            finance_factors.append("Mercury retrograde: Review financial plans")
            finance_score = max(1, finance_score - 1)
        
        # 5. Overall Guidance
        overall_factors = []
        
        # Day lord (weekday ruler) analysis
        weekday_lord = ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn'][date.weekday()]
        if weekday_lord == sign_lord:
            overall_factors.append(f"Today is ruled by {weekday_lord}, your sign lord - highly auspicious")
            overall_rating += 2
        
        # Check if sign lord is well placed
        if sign_lord in transits:
            lord_house = ((self.SIGNS.index(transits[sign_lord]['sign']) - sign_num) % 12) + 1
            if lord_house in [1, 5, 9, 10, 11]:
                overall_factors.append(f"Your sign lord {sign_lord} is favorably placed")
                overall_rating += 2
            elif not transits[sign_lord]['is_retrograde']:
                overall_factors.append(f"{sign_lord} direct motion supports your endeavors")
                overall_rating += 1
        
        # Rahu-Ketu axis
        rahu_house = ((self.SIGNS.index(transits['Rahu']['sign']) - sign_num) % 12) + 1
        if rahu_house in [3, 6, 10, 11]:
            overall_factors.append("Rahu transit brings unconventional opportunities")
            overall_rating += 1
        elif rahu_house in [1, 7]:
            overall_factors.append("Rahu-Ketu axis on self-others: transformation period")
        
        # Calculate overall rating (1-5 stars)
        avg_score = (career_score + love_score + health_score + finance_score) / 16.0
        overall_rating += avg_score * 3
        final_rating = round(min(5, overall_rating))
        
        return {
            'overall': {
                'rating': final_rating,
                'summary': self._generate_overall_summary(zodiac_sign, final_rating, overall_factors),
                'key_factors': overall_factors
            },
            'career': {
                'rating': min(5, round(career_score / 1.6)),
                'prediction': ' '.join(career_factors[:2]) if career_factors else "Steady professional period",
                'advice': self._get_career_advice(career_score, transits),
                'factors': career_factors
            },
            'love': {
                'rating': min(5, round(love_score / 1.6)),
                'prediction': ' '.join(love_factors[:2]) if love_factors else "Normal relationship dynamics",
                'advice': self._get_love_advice(love_score, transits),
                'factors': love_factors
            },
            'health': {
                'rating': min(5, round(health_score / 1.4)),
                'prediction': ' '.join(health_factors[:2]) if health_factors else "Maintain health routines",
                'advice': self._get_health_advice(health_score, transits),
                'factors': health_factors
            },
            'finance': {
                'rating': min(5, round(finance_score / 1.6)),
                'prediction': ' '.join(finance_factors[:2]) if finance_factors else "Stable financial period",
                'advice': self._get_finance_advice(finance_score, transits),
                'factors': finance_factors
            }
        }
    
    def _generate_overall_summary(self, sign: str, rating: int, factors: List[str]) -> str:
        """Generate personalized overall summary"""
        summaries = {
            5: f"Excellent day for {sign}! Planetary alignments are highly favorable.",
            4: f"Very good day ahead for {sign}. Multiple positive influences.",
            3: f"Balanced day for {sign}. Mix of opportunities and challenges.",
            2: f"Challenging day for {sign}. Stay patient and focused.",
            1: f"Difficult period for {sign}. Practice caution and remedies."
        }
        base_summary = summaries.get(rating, summaries[3])
        
        if factors:
            base_summary += " " + factors[0]
        
        return base_summary
    
    def _get_career_advice(self, score: int, transits: Dict) -> str:
        """Career-specific advice"""
        if score >= 7:
            return "Excellent time for important meetings, presentations, and career initiatives"
        elif score >= 4:
            return "Focus on routine work and building professional relationships"
        else:
            return "Avoid major career decisions. Focus on learning and preparation"
    
    def _get_love_advice(self, score: int, transits: Dict) -> str:
        """Love-specific advice"""
        if score >= 7:
            return "Great time for romantic gestures, dates, and meaningful conversations"
        elif score >= 4:
            return "Good day for spending quality time with loved ones"
        else:
            return "Practice patience and understanding. Avoid confrontations"
    
    def _get_health_advice(self, score: int, transits: Dict) -> str:
        """Health-specific advice"""
        if score >= 6:
            return "Excellent vitality. Good time for starting new health routines"
        elif score >= 3:
            return "Maintain regular exercise and healthy eating habits"
        else:
            return "Prioritize rest, avoid stress, and consult healthcare if needed"
    
    def _get_finance_advice(self, score: int, transits: Dict) -> str:
        """Finance-specific advice"""
        if score >= 7:
            return "Favorable for investments, business deals, and financial planning"
        elif score >= 4:
            return "Good time for routine transactions and savings"
        else:
            return "Avoid risky investments. Focus on saving and financial review"
    
    def _calculate_lucky_elements(self, transits: Dict, zodiac_sign: str) -> Dict:
        """Calculate lucky elements based on transits"""
        
        # Lucky color from strongest planet
        colors = {
            'Sun': ['Gold', 'Orange', 'Red'],
            'Moon': ['White', 'Silver', 'Cream'],
            'Mars': ['Red', 'Maroon', 'Scarlet'],
            'Mercury': ['Green', 'Emerald', 'Parrot Green'],
            'Jupiter': ['Yellow', 'Golden Yellow', 'Saffron'],
            'Venus': ['White', 'Pink', 'Light Blue'],
            'Saturn': ['Black', 'Dark Blue', 'Navy']
        }
        
        sign_lord = self.SIGN_LORDS[zodiac_sign]
        lucky_colors = colors.get(sign_lord, ['White'])
        
        # Lucky number from Moon nakshatra
        moon_nakshatra_num = transits['Moon']['nakshatra']['number']
        lucky_number = (moon_nakshatra_num % 9) + 1
        
        # Lucky time from Moon position
        moon_longitude = transits['Moon']['longitude']
        hora_lord = self._get_hora_lord(moon_longitude)
        lucky_times = {
            'Sun': '12:00 PM - 1:00 PM',
            'Moon': '6:00 AM - 7:00 AM',
            'Mars': '12:00 AM - 1:00 AM',
            'Mercury': '6:00 PM - 7:00 PM',
            'Jupiter': '9:00 AM - 10:00 AM',
            'Venus': '3:00 PM - 4:00 PM',
            'Saturn': '6:00 PM - 7:00 PM'
        }
        
        # Lucky direction from Jupiter
        jupiter_sign_num = self.SIGNS.index(transits['Jupiter']['sign'])
        directions = ['East', 'South-East', 'South', 'South-West', 
                     'West', 'North-West', 'North', 'North-East',
                     'East', 'South-East', 'South', 'South-West']
        
        return {
            'color': lucky_colors[0],
            'colors': lucky_colors,
            'number': lucky_number,
            'time': lucky_times.get(hora_lord, '9:00 AM - 10:00 AM'),
            'direction': directions[jupiter_sign_num % 8],
            'gemstone': self._get_gemstone_for_sign(zodiac_sign),
            'day_quality': self._assess_day_quality(transits, zodiac_sign)
        }
    
    def _get_hora_lord(self, longitude: float) -> str:
        """Get hora lord from longitude"""
        hora_num = int((longitude / 15)) % 7
        lords = ['Sun', 'Venus', 'Mercury', 'Moon', 'Saturn', 'Jupiter', 'Mars']
        return lords[hora_num]
    
    def _get_gemstone_for_sign(self, zodiac_sign: str) -> str:
        """Get primary gemstone for sign"""
        gemstones = {
            'Aries': 'Red Coral',
            'Taurus': 'Diamond',
            'Gemini': 'Emerald',
            'Cancer': 'Pearl',
            'Leo': 'Ruby',
            'Virgo': 'Emerald',
            'Libra': 'Diamond',
            'Scorpio': 'Red Coral',
            'Sagittarius': 'Yellow Sapphire',
            'Capricorn': 'Blue Sapphire',
            'Aquarius': 'Blue Sapphire',
            'Pisces': 'Yellow Sapphire'
        }
        return gemstones.get(zodiac_sign, 'Pearl')
    
    def _assess_day_quality(self, transits: Dict, zodiac_sign: str) -> str:
        """Assess overall day quality"""
        sign_num = self.SIGNS.index(zodiac_sign)
        
        # Count beneficial transits
        beneficial = 0
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus']:
            planet_sign_num = self.SIGNS.index(transits[planet]['sign'])
            house = ((planet_sign_num - sign_num) % 12) + 1
            if house in [1, 5, 9, 10, 11]:
                beneficial += 2
            elif house in [2, 3, 4, 7]:
                beneficial += 1
        
        if beneficial >= 8:
            return "Highly Auspicious"
        elif beneficial >= 5:
            return "Auspicious"
        elif beneficial >= 3:
            return "Moderate"
        else:
            return "Challenging"
    
    def _get_daily_remedies(self, zodiac_sign: str, transits: Dict) -> List[Dict]:
        """Get personalized daily remedies"""
        remedies = []
        
        sign_lord = self.SIGN_LORDS[zodiac_sign]
        
        # Sign lord specific remedy
        sign_remedies = {
            'Sun': {
                'mantra': 'Om Suryaya Namaha',
                'action': 'Offer water to Sun at sunrise',
                'charity': 'Donate wheat or jaggery'
            },
            'Moon': {
                'mantra': 'Om Chandraya Namaha',
                'action': 'Offer milk to Lord Shiva',
                'charity': 'Donate rice or white clothes'
            },
            'Mars': {
                'mantra': 'Om Mangalaya Namaha',
                'action': 'Recite Hanuman Chalisa',
                'charity': 'Donate red lentils'
            },
            'Mercury': {
                'mantra': 'Om Budhaya Namaha',
                'action': 'Feed green vegetables to cows',
                'charity': 'Donate green clothes or books'
            },
            'Jupiter': {
                'mantra': 'Om Gurave Namaha',
                'action': 'Wear yellow on Thursdays',
                'charity': 'Donate yellow items or turmeric'
            },
            'Venus': {
                'mantra': 'Om Shukraya Namaha',
                'action': 'Offer white flowers to Goddess Lakshmi',
                'charity': 'Donate white clothes or rice'
            },
            'Saturn': {
                'mantra': 'Om Shanaischaraya Namaha',
                'action': 'Light mustard oil lamp on Saturdays',
                'charity': 'Donate black sesame or iron'
            }
        }
        
        lord_remedy = sign_remedies.get(sign_lord, sign_remedies['Sun'])
        remedies.append({
            'type': 'Sign Lord Remedy',
            'planet': sign_lord,
            'mantra': lord_remedy['mantra'],
            'mantra_count': '108 times',
            'action': lord_remedy['action'],
            'charity': lord_remedy['charity']
        })
        
        # Check for retrograde planets
        for planet, data in transits.items():
            if planet in ['Rahu', 'Ketu']:
                continue
            if data.get('is_retrograde'):
                remedies.append({
                    'type': 'Retrograde Planet Remedy',
                    'planet': planet,
                    'action': f'Chant {planet} mantra and practice patience',
                    'recommendation': f'{planet} retrograde requires review and reflection'
                })
        
        # Moon nakshatra remedy
        moon_nakshatra = transits['Moon']['nakshatra']['name']
        remedies.append({
            'type': 'Nakshatra Remedy',
            'nakshatra': moon_nakshatra,
            'action': f'Meditate during Moon in {moon_nakshatra}',
            'benefit': 'Enhances mental peace and intuition'
        })
        
        return remedies
    
    def generate_daily_horoscope(self, zodiac_sign: str, date: datetime = None) -> Dict:
        """
        Generate professional daily horoscope for a zodiac sign
        
        Args:
            zodiac_sign: Aries, Taurus, etc.
            date: Date for horoscope (default: today)
        """
        if date is None:
            date = datetime.now()
        
        transits = self._get_all_transits(date)
        strengths = self._calculate_transit_strength(zodiac_sign, transits)
        
        # Get sign lord transit
        sign_lord = self.SIGN_LORDS[zodiac_sign]
        lord_transit = transits.get(sign_lord, {})
        
        # Moon phase
        moon_phase = self._get_moon_phase(
            transits['Sun']['longitude'],
            transits['Moon']['longitude']
        )
        
        # Analyze transits for detailed predictions
        predictions = self._analyze_daily_transits_professional(
            zodiac_sign, transits, strengths, date
        )
        
        return {
            'sign': zodiac_sign,
            'date': date.strftime('%Y-%m-%d'),
            'day': date.strftime('%A'),
            'period': 'Daily',
            'moon_phase': moon_phase,
            'sign_lord': sign_lord,
            'lord_position': {
                'sign': lord_transit.get('sign'),
                'nakshatra': lord_transit.get('nakshatra', {}).get('name'),
                'retrograde': lord_transit.get('is_retrograde', False)
            },
            'transits': transits,
            'transit_strengths': strengths,
            'predictions': predictions,
            'lucky_elements': self._calculate_lucky_elements(transits, zodiac_sign),
            'remedies': self._get_daily_remedies(zodiac_sign, transits)
        }
    
    def generate_weekly_horoscope(self, zodiac_sign: str, start_date: datetime = None) -> Dict:
        """Generate professional weekly horoscope"""
        if start_date is None:
            start_date = datetime.now()
        
        end_date = start_date + timedelta(days=7)
        
        # Get transits for start, mid, and end of week
        start_transits = self._get_all_transits(start_date)
        mid_transits = self._get_all_transits(start_date + timedelta(days=3))
        end_transits = self._get_all_transits(end_date)
        
        strengths = self._calculate_transit_strength(zodiac_sign, start_transits)
        predictions = self._analyze_weekly_transits_professional(
            zodiac_sign, start_transits, mid_transits, end_transits, start_date
        )
        
        return {
            'sign': zodiac_sign,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'period': 'Weekly',
            'key_transits': {
                'start_week': start_transits,
                'mid_week': mid_transits,
                'end_week': end_transits
            },
            'transit_strengths': strengths,
            'predictions': predictions,
            'lucky_days': self._get_lucky_days_of_week(start_transits, zodiac_sign),
            'best_day': self._get_best_day_of_week(start_date, zodiac_sign, start_transits)
        }
    
    def _analyze_weekly_transits_professional(
        self, sign: str, start: Dict, mid: Dict, end: Dict, start_date: datetime
    ) -> Dict:
        """Professional weekly analysis"""
        
        sign_num = self.SIGNS.index(sign)
        sign_lord = self.SIGN_LORDS[sign]
        
        # Analyze weekly trend
        weekly_trend = self._analyze_weekly_trend(sign, start, mid, end)
        
        # Career weekly
        career_analysis = self._analyze_weekly_career(sign, start, mid, end)
        
        # Love weekly
        love_analysis = self._analyze_weekly_love(sign, start, mid, end)
        
        # Health weekly
        health_analysis = self._analyze_weekly_health(sign, start, mid, end)
        
        # Finance weekly
        finance_analysis = self._analyze_weekly_finance(sign, start, mid, end)
        
        return {
            'overview': {
                'summary': weekly_trend,
                'rating': self._calculate_week_rating(sign, start, mid, end),
                'key_theme': self._get_weekly_theme(sign, start, mid, end)
            },
            'career': career_analysis,
            'love': love_analysis,
            'health': health_analysis,
            'finance': finance_analysis,
            'days_breakdown': self._get_daily_breakdown_for_week(sign, start_date, start)
        }
    
    def _analyze_weekly_trend(self, sign: str, start: Dict, mid: Dict, end: Dict) -> str:
        """Analyze overall weekly trend"""
        sign_num = self.SIGNS.index(sign)
        
        # Check major planet movements
        jupiter_start_house = ((self.SIGNS.index(start['Jupiter']['sign']) - sign_num) % 12) + 1
        saturn_start_house = ((self.SIGNS.index(start['Saturn']['sign']) - sign_num) % 12) + 1
        
        if jupiter_start_house in [1, 5, 9, 11]:
            return f"Auspicious week for {sign}! Jupiter's blessings bring growth opportunities across all areas. Stay optimistic and take initiative."
        elif saturn_start_house in [3, 6, 10, 11]:
            return f"Productive week for {sign}. Saturn favors hard work and discipline. Focus on long-term goals with patience."
        else:
            return f"Balanced week for {sign}. Mix of opportunities and challenges. Strategic planning yields best results."
    
    def _analyze_weekly_career(self, sign: str, start: Dict, mid: Dict, end: Dict) -> Dict:
        """Weekly career analysis"""
        sign_num = self.SIGNS.index(sign)
        
        # Sun position (authority, recognition)
        sun_house_start = ((self.SIGNS.index(start['Sun']['sign']) - sign_num) % 12) + 1
        sun_house_end = ((self.SIGNS.index(end['Sun']['sign']) - sign_num) % 12) + 1
        
        if sun_house_start in [10, 11] or sun_house_end in [10, 11]:
            advice = "Excellent week for career advancement. Schedule important meetings. Seek recognition for your work."
            rating = 5
        elif sun_house_start in [6, 8, 12]:
            advice = "Challenging professional week. Focus on completing pending tasks. Avoid confrontations with authorities."
            rating = 2
        else:
            advice = "Steady professional week. Good for routine work and team collaboration. Plan strategically for coming opportunities."
            rating = 3
        
        return {
            'rating': rating,
            'prediction': advice,
            'best_days': 'Monday, Wednesday, Friday',
            'action_items': [
                'Complete pending projects',
                'Network with colleagues',
                'Update your skills'
            ]
        }
    
    def _analyze_weekly_love(self, sign: str, start: Dict, mid: Dict, end: Dict) -> Dict:
        """Weekly love analysis"""
        sign_num = self.SIGNS.index(sign)
        
        # Venus position (love, relationships)
        venus_house_start = ((self.SIGNS.index(start['Venus']['sign']) - sign_num) % 12) + 1
        
        # Moon analysis for emotions
        moon_nakshatra_start = start['Moon']['nakshatra']['name']
        
        if venus_house_start in [1, 5, 7, 11]:
            prediction = f"Romantic week ahead! Venus in favorable position enhances charm. Moon in {moon_nakshatra_start} supports emotional connections."
            rating = 5
        elif venus_house_start in [6, 8, 12]:
            prediction = "Relationships require patience this week. Practice understanding and avoid arguments. Focus on emotional healing."
            rating = 2
        else:
            prediction = "Normal relationship dynamics. Good week for strengthening existing bonds. Singles may experience interesting encounters."
            rating = 3
        
        return {
            'rating': rating,
            'prediction': prediction,
            'best_days': 'Tuesday, Friday, Saturday',
            'advice': 'Express feelings openly and listen actively'
        }
    
    def _analyze_weekly_health(self, sign: str, start: Dict, mid: Dict, end: Dict) -> Dict:
        """Weekly health analysis"""
        sign_num = self.SIGNS.index(sign)
        
        # Mars (energy) and Moon (mind) for health
        mars_house = ((self.SIGNS.index(start['Mars']['sign']) - sign_num) % 12) + 1
        
        if mars_house in [1, 6, 8, 12]:
            prediction = "Exercise caution with health this week. Avoid stress and overexertion. Practice relaxation techniques."
            rating = 2
        elif mars_house in [3, 10, 11]:
            prediction = "High energy week! Great time to start new fitness routines. Vitality is excellent."
            rating = 5
        else:
            prediction = "Balanced health week. Maintain regular routines. Moderate exercise and healthy diet recommended."
            rating = 3
        
        return {
            'rating': rating,
            'prediction': prediction,
            'focus_areas': ['Mental wellness', 'Physical fitness', 'Nutrition'],
            'recommendation': 'Practice yoga or meditation daily'
        }
    
    def _analyze_weekly_finance(self, sign: str, start: Dict, mid: Dict, end: Dict) -> Dict:
        """Weekly finance analysis"""
        sign_num = self.SIGNS.index(sign)
        
        # Jupiter (wealth) and Mercury (business)
        jupiter_house = ((self.SIGNS.index(start['Jupiter']['sign']) - sign_num) % 12) + 1
        mercury_house = ((self.SIGNS.index(start['Mercury']['sign']) - sign_num) % 12) + 1
        
        if jupiter_house in [2, 11] or mercury_house in [2, 11]:
            prediction = "Financially favorable week. Good for investments and business deals. Unexpected gains possible."
            rating = 5
        elif jupiter_house in [8, 12] or start['Mercury'].get('is_retrograde'):
            prediction = "Exercise financial caution. Avoid major purchases or investments. Review budgets carefully."
            rating = 2
        else:
            prediction = "Stable financial week. Good for savings and routine transactions. Plan for future expenses."
            rating = 3
        
        return {
            'rating': rating,
            'prediction': prediction,
            'opportunities': 'Mid-week favors financial discussions',
            'caution': 'Avoid impulsive spending on weekends'
        }
    
    def _calculate_week_rating(self, sign: str, start: Dict, mid: Dict, end: Dict) -> int:
        """Calculate overall week rating"""
        sign_num = self.SIGNS.index(sign)
        
        beneficial_count = 0
        for planet in ['Sun', 'Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus']:
            house = ((self.SIGNS.index(start[planet]['sign']) - sign_num) % 12) + 1
            if house in [1, 5, 9, 10, 11]:
                beneficial_count += 2
            elif house in [2, 3, 7]:
                beneficial_count += 1
        
        if beneficial_count >= 8:
            return 5
        elif beneficial_count >= 5:
            return 4
        elif beneficial_count >= 3:
            return 3
        elif beneficial_count >= 1:
            return 2
        else:
            return 1
    
    def _get_weekly_theme(self, sign: str, start: Dict, mid: Dict, end: Dict) -> str:
        """Get weekly theme"""
        themes = [
            "Growth and Expansion",
            "Relationship Focus",
            "Career Advancement",
            "Financial Planning",
            "Health and Wellness",
            "Spiritual Development",
            "Communication and Learning"
        ]
        sun_sign_num = self.SIGNS.index(start['Sun']['sign'])
        return themes[sun_sign_num % len(themes)]
    
    def _get_daily_breakdown_for_week(self, sign: str, start_date: datetime, transits: Dict) -> Dict:
        """Break down each day of the week"""
        days = {}
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        day_lords = ['Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Sun']
        
        for i in range(7):
            current_date = start_date + timedelta(days=i)
            weekday = weekdays[current_date.weekday()]
            day_lord = day_lords[current_date.weekday()]
            
            days[weekday] = {
                'date': current_date.strftime('%Y-%m-%d'),
                'day_lord': day_lord,
                'quality': self._get_day_quality(day_lord, sign, transits),
                'focus': self._get_day_focus(day_lord)
            }
        
        return days
    
    def _get_day_quality(self, day_lord: str, sign: str, transits: Dict) -> str:
        """Get quality of specific day"""
        sign_lord = self.SIGN_LORDS[sign]
        
        if day_lord == sign_lord:
            return "Excellent"
        elif day_lord in ['Jupiter', 'Venus']:
            return "Good"
        elif day_lord in ['Mercury', 'Moon']:
            return "Moderate"
        else:
            return "Average"
    
    def _get_day_focus(self, day_lord: str) -> str:
        """Get focus area for day lord"""
        focus_map = {
            'Sun': 'Authority, Father, Government work',
            'Moon': 'Emotions, Mother, Public dealings',
            'Mars': 'Energy, Sports, Property matters',
            'Mercury': 'Business, Communication, Learning',
            'Jupiter': 'Wisdom, Children, Spiritual growth',
            'Venus': 'Love, Arts, Luxury, Beauty',
            'Saturn': 'Hard work, Discipline, Karma'
        }
        return focus_map.get(day_lord, 'General activities')
    
    def _get_lucky_days_of_week(self, transits: Dict, sign: str) -> List[Dict]:
        """Get lucky days with reasons"""
        sign_lord = self.SIGN_LORDS[sign]
        days = []
        
        weekday_lords = {
            'Sunday': 'Sun',
            'Monday': 'Moon',
            'Tuesday': 'Mars',
            'Wednesday': 'Mercury',
            'Thursday': 'Jupiter',
            'Friday': 'Venus',
            'Saturday': 'Saturn'
        }
        
        for day, lord in weekday_lords.items():
            if lord == sign_lord:
                days.append({'day': day, 'reason': f'{lord} is your sign lord'})
            elif lord in ['Jupiter', 'Venus']:
                days.append({'day': day, 'reason': f'{lord} brings natural benefits'})
        
        return days[:3]
    
    def _get_best_day_of_week(self, start_date: datetime, sign: str, transits: Dict) -> Dict:
        """Identify best single day of the week"""
        sign_lord = self.SIGN_LORDS[sign]
        weekday_lords = ['Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Sun']
        
        for i, lord in enumerate(weekday_lords):
            if lord == sign_lord:
                best_date = start_date + timedelta(days=i)
                return {
                    'day': best_date.strftime('%A'),
                    'date': best_date.strftime('%Y-%m-%d'),
                    'reason': f'Ruled by {sign_lord}, your sign lord'
                }
        
        # Default to Jupiter day (Thursday)
        thursday_date = start_date + timedelta(days=(3 - start_date.weekday()) % 7)
        return {
            'day': 'Thursday',
            'date': thursday_date.strftime('%Y-%m-%d'),
            'reason': 'Ruled by Jupiter, planet of fortune'
        }
    
    def generate_monthly_horoscope(self, zodiac_sign: str, year: int = None, month: int = None) -> Dict:
        """Generate professional monthly horoscope"""
        if year is None:
            year = datetime.now().year
        if month is None:
            month = datetime.now().month
        
        start_date = datetime(year, month, 1)
        if month == 12:
            end_date = datetime(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = datetime(year, month + 1, 1) - timedelta(days=1)
        
        # Get transits for start, multiple points, and end
        start_transits = self._get_all_transits(start_date)
        week2_transits = self._get_all_transits(start_date + timedelta(days=7))
        mid_transits = self._get_all_transits(start_date + timedelta(days=15))
        week3_transits = self._get_all_transits(start_date + timedelta(days=21))
        end_transits = self._get_all_transits(end_date)
        
        predictions = self._analyze_monthly_transits_professional(
            zodiac_sign, start_transits, week2_transits, mid_transits, week3_transits, end_transits, start_date
        )
        
        return {
            'sign': zodiac_sign,
            'month': start_date.strftime('%B %Y'),
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'period': 'Monthly',
            'key_transits': {
                'start': start_transits,
                'week_2': week2_transits,
                'mid_month': mid_transits,
                'week_3': week3_transits,
                'end': end_transits
            },
            'predictions': predictions,
            'best_dates': self._get_best_dates_of_month_professional(start_date, zodiac_sign, start_transits),
            'challenging_dates': self._get_challenging_dates(start_date, zodiac_sign, start_transits)
        }
    
    def _analyze_monthly_transits_professional(
        self, sign: str, start: Dict, week2: Dict, mid: Dict, week3: Dict, end: Dict, start_date: datetime
    ) -> Dict:
        """Professional monthly analysis"""
        
        month_name = start_date.strftime('%B')
        sign_num = self.SIGNS.index(sign)
        sign_lord = self.SIGN_LORDS[sign]
        
        # Check for major transits
        major_events = self._identify_major_monthly_transits(sign, start, mid, end)
        
        # Overall monthly theme
        monthly_overview = self._generate_monthly_overview(sign, sign_lord, start, mid, end, month_name, major_events)
        
        # Detailed area analysis
        career_monthly = self._analyze_monthly_career(sign, start, mid, end)
        love_monthly = self._analyze_monthly_love(sign, start, mid, end)
        health_monthly = self._analyze_monthly_health(sign, start, mid, end)
        finance_monthly = self._analyze_monthly_finance(sign, start, mid, end)
        
        return {
            'overview': monthly_overview,
            'major_transits': major_events,
            'first_half': self._analyze_month_half(sign, start, week2, 'first'),
            'second_half': self._analyze_month_half(sign, mid, end, 'second'),
            'career': career_monthly,
            'love': love_monthly,
            'health': health_monthly,
            'finance': finance_monthly,
            'weekly_breakdown': {
                'week_1': 'Foundation setting week. Plan and initiate.',
                'week_2': 'Action week. Execute plans with confidence.',
                'week_3': 'Mid-month adjustments. Review and refine.',
                'week_4': 'Completion week. Harvest results.'
            }
        }
    
    def _identify_major_monthly_transits(self, sign: str, start: Dict, mid: Dict, end: Dict) -> List[Dict]:
        """Identify major planetary events in the month"""
        events = []
        sign_num = self.SIGNS.index(sign)
        
        # Check Saturn (major long-term planet)
        saturn_house = ((self.SIGNS.index(start['Saturn']['sign']) - sign_num) % 12) + 1
        if saturn_house in [1, 7, 10]:
            events.append({
                'planet': 'Saturn',
                'event': f'Saturn transiting your {self._get_house_name(saturn_house)}',
                'impact': 'Long-term karmic lessons and restructuring',
                'nature': 'Challenging but transformative'
            })
        
        # Check Jupiter (major benefic)
        jupiter_house = ((self.SIGNS.index(start['Jupiter']['sign']) - sign_num) % 12) + 1
        if jupiter_house in [1, 5, 9, 11]:
            events.append({
                'planet': 'Jupiter',
                'event': f'Jupiter blessing your {self._get_house_name(jupiter_house)}',
                'impact': 'Growth, wisdom, and opportunities',
                'nature': 'Highly beneficial'
            })
        
        # Check Rahu-Ketu axis
        rahu_house = ((self.SIGNS.index(start['Rahu']['sign']) - sign_num) % 12) + 1
        if rahu_house in [1, 7]:
            events.append({
                'planet': 'Rahu-Ketu',
                'event': 'Rahu-Ketu axis on self-others',
                'impact': 'Major life transformations and realizations',
                'nature': 'Transformative'
            })
        
        # Check for retrogrades
        for planet in ['Mercury', 'Venus', 'Mars']:
            if start[planet].get('is_retrograde') or mid[planet].get('is_retrograde'):
                events.append({
                    'planet': planet,
                    'event': f'{planet} Retrograde',
                    'impact': f'Review and revisit {self.PLANET_NATURE[planet].split(",")[0].lower()} matters',
                    'nature': 'Introspective'
                })
        
        return events if events else [{
            'planet': 'General',
            'event': 'Normal planetary movements',
            'impact': 'Steady progress in all areas',
            'nature': 'Stable'
        }]
    
    def _get_house_name(self, house_num: int) -> str:
        """Get house name"""
        houses = {
            1: '1st house (Self, Personality)',
            2: '2nd house (Wealth, Family)',
            3: '3rd house (Courage, Siblings)',
            4: '4th house (Home, Mother)',
            5: '5th house (Children, Creativity)',
            6: '6th house (Health, Enemies)',
            7: '7th house (Partnership, Marriage)',
            8: '8th house (Transformation, Longevity)',
            9: '9th house (Fortune, Father)',
            10: '10th house (Career, Status)',
            11: '11th house (Gains, Friends)',
            12: '12th house (Expenses, Spirituality)'
        }
        return houses.get(house_num, f'{house_num}th house')
    
    def _generate_monthly_overview(self, sign: str, sign_lord: str, start: Dict, mid: Dict, end: Dict, month: str, major_events: List) -> Dict:
        """Generate comprehensive monthly overview"""
        sign_num = self.SIGNS.index(sign)
        
        # Calculate monthly rating
        rating = 3  # Base rating
        
        # Adjust based on Jupiter
        jupiter_house = ((self.SIGNS.index(start['Jupiter']['sign']) - sign_num) % 12) + 1
        if jupiter_house in [1, 5, 9, 10, 11]:
            rating += 1
        
        # Adjust based on Saturn
        saturn_house = ((self.SIGNS.index(start['Saturn']['sign']) - sign_num) % 12) + 1
        if saturn_house in [6, 8, 12]:
            rating -= 1
        
        rating = max(1, min(5, rating))
        
        # Generate summary
        if rating >= 4:
            summary = f"{month} is an excellent period for {sign}! Major planetary alignments support growth, success, and happiness. Take advantage of opportunities."
        elif rating == 3:
            summary = f"{month} brings balanced energy for {sign}. Mix of opportunities and challenges. Strategic planning and consistent effort yield positive results."
        else:
            summary = f"{month} requires patience for {sign}. Challenges present learning opportunities. Focus on inner growth and preparation for better times ahead."
        
        return {
            'rating': rating,
            'summary': summary,
            'key_theme': major_events[0]['impact'] if major_events else 'Steady progress',
            'overall_advice': f'Focus on {sign_lord} qualities: {self.PLANET_NATURE[sign_lord].split(",")[0]}'
        }
    
    def _analyze_month_half(self, sign: str, start: Dict, end: Dict, half: str) -> str:
        """Analyze first or second half of month"""
        sign_num = self.SIGNS.index(sign)
        sun_house = ((self.SIGNS.index(start['Sun']['sign']) - sign_num) % 12) + 1
        
        if half == 'first':
            if sun_house in [1, 10, 11]:
                return "First half very favorable. Initiate new projects. Take bold steps. Recognition and success likely."
            else:
                return "First half sets foundation. Plan carefully. Build resources. Avoid hasty decisions."
        else:
            if sun_house in [1, 10, 11]:
                return "Second half brings fruition. Reap benefits of earlier efforts. Consolidate gains."
            else:
                return "Second half requires patience. Complete pending tasks. Prepare for next month's opportunities."
    
    def _analyze_monthly_career(self, sign: str, start: Dict, mid: Dict, end: Dict) -> Dict:
        """Monthly career analysis"""
        sign_num = self.SIGNS.index(sign)
        
        # Sun (authority, career) analysis
        sun_start_house = ((self.SIGNS.index(start['Sun']['sign']) - sign_num) % 12) + 1
        sun_mid_house = ((self.SIGNS.index(mid['Sun']['sign']) - sign_num) % 12) + 1
        
        # Saturn (work, responsibility)
        saturn_house = ((self.SIGNS.index(start['Saturn']['sign']) - sign_num) % 12) + 1
        
        if sun_start_house == 10 or sun_mid_house == 10:
            rating = 5
            prediction = "Exceptional career month! Sun in 10th house brings recognition, promotions, and authority. Seize leadership opportunities."
        elif sun_start_house in [1, 9, 11] or saturn_house in [3, 6, 10]:
            rating = 4
            prediction = "Very good professional month. Hard work brings results. Network actively and showcase skills."
        elif sun_start_house in [6, 8, 12]:
            rating = 2
            prediction = "Challenging career period. Politics and conflicts possible. Stay focused on work. Avoid confrontations."
        else:
            rating = 3
            prediction = "Steady professional month. Good for routine work and skill development. Build relationships with colleagues."
        
        return {
            'rating': rating,
            'prediction': prediction,
            'best_period': 'Mid-month (15th-22nd) especially favorable',
            'opportunities': ['New projects', 'Team leadership', 'Skill upgrades'],
            'cautions': ['Office politics', 'Overcommitment', 'Deadline pressure']
        }
    
    def _analyze_monthly_love(self, sign: str, start: Dict, mid: Dict, end: Dict) -> Dict:
        """Monthly love analysis"""
        sign_num = self.SIGNS.index(sign)
        
        # Venus (love) analysis
        venus_start_house = ((self.SIGNS.index(start['Venus']['sign']) - sign_num) % 12) + 1
        venus_mid_house = ((self.SIGNS.index(mid['Venus']['sign']) - sign_num) % 12) + 1
        
        is_retrograde = start['Venus'].get('is_retrograde') or mid['Venus'].get('is_retrograde')
        
        if is_retrograde:
            rating = 2
            prediction = "Venus retrograde brings past relationship issues to surface. Time for healing, not new commitments. Ex-partners may reconnect."
        elif venus_start_house in [1, 5, 7] or venus_mid_house in [1, 5, 7]:
            rating = 5
            prediction = "Romantic month! Venus enhances charm and attractiveness. Excellent for dating, proposals, and deepening bonds. Singles find good matches."
        elif venus_start_house in [11]:
            rating = 4
            prediction = "Social and romantic opportunities through friends. Existing relationships strengthen. Good time for celebrations."
        elif venus_start_house in [6, 8, 12]:
            rating = 2
            prediction = "Relationship challenges possible. Misunderstandings need patience. Focus on emotional healing and self-love."
        else:
            rating = 3
            prediction = "Normal relationship dynamics. Good for quiet bonding time. Build emotional security gradually."
        
        return {
            'rating': rating,
            'prediction': prediction,
            'singles': 'New connections likely through work or social circles' if rating >= 4 else 'Focus on self-improvement, right person will come',
            'committed': 'Deepen intimacy through quality time' if rating >= 4 else 'Practice patience and communication',
            'best_dates': 'Fridays and new moon period especially romantic'
        }
    
    def _analyze_monthly_health(self, sign: str, start: Dict, mid: Dict, end: Dict) -> Dict:
        """Monthly health analysis"""
        sign_num = self.SIGNS.index(sign)
        
        # Mars (energy, vitality)
        mars_house = ((self.SIGNS.index(start['Mars']['sign']) - sign_num) % 12) + 1
        
        # Moon (mind, emotions)
        moon_nakshatra_start = start['Moon']['nakshatra']['name']
        
        if mars_house in [1, 6, 8, 12]:
            rating = 2
            prediction = f"Health requires attention this month. Mars in {self._get_house_name(mars_house)} may cause stress or inflammation. Avoid accidents and overexertion."
            focus = ['Stress management', 'Avoid risky activities', 'Regular checkups']
        elif mars_house in [3, 10, 11]:
            rating = 5
            prediction = "Excellent vitality month! High energy levels support new fitness goals. Great time for sports and physical challenges."
            focus = ['Start new exercise routine', 'Outdoor activities', 'Build strength']
        else:
            rating = 3
            prediction = "Balanced health month. Maintain regular routines. Focus on preventive care and healthy lifestyle."
            focus = ['Regular exercise', 'Balanced diet', 'Adequate sleep']
        
        return {
            'rating': rating,
            'prediction': prediction,
            'focus_areas': focus,
            'mental_health': f'Moon in {moon_nakshatra_start} supports emotional balance. Practice meditation.',
            'recommendation': 'Yoga, pranayama, and natural diet highly beneficial'
        }
    
    def _analyze_monthly_finance(self, sign: str, start: Dict, mid: Dict, end: Dict) -> Dict:
        """Monthly finance analysis"""
        sign_num = self.SIGNS.index(sign)
        
        # Jupiter (wealth, fortune)
        jupiter_house = ((self.SIGNS.index(start['Jupiter']['sign']) - sign_num) % 12) + 1
        
        # Mercury (business, trade)
        mercury_house = ((self.SIGNS.index(start['Mercury']['sign']) - sign_num) % 12) + 1
        mercury_retrograde = start['Mercury'].get('is_retrograde') or mid['Mercury'].get('is_retrograde')
        
        if jupiter_house in [2, 11]:
            rating = 5
            prediction = "Excellent financial month! Jupiter in wealth houses brings gains, investments pay off. New income sources possible."
        elif jupiter_house in [1, 5, 9] and mercury_house in [2, 3, 10, 11]:
            rating = 4
            prediction = "Good financial period. Business and trade favorable. Smart investments recommended. Income growth likely."
        elif mercury_retrograde:
            rating = 2
            prediction = "Mercury retrograde warns against major financial decisions. Review budgets, avoid new investments. Delays in payments possible."
        elif jupiter_house in [8, 12]:
            rating = 2
            prediction = "Financial caution needed. Unexpected expenses possible. Avoid loans and risky ventures. Focus on saving."
        else:
            rating = 3
            prediction = "Stable financial month. Good for routine transactions and savings. Plan for future carefully."
        
        return {
            'rating': rating,
            'prediction': prediction,
            'opportunities': ['Mid-month especially good for financial decisions', 'Jupiter day (Thursday) favorable for investments'],
            'cautions': ['Avoid impulsive purchases', 'Read contracts carefully', 'Emergency fund important'],
            'best_investment_period': 'After 15th of the month' if rating >= 3 else 'Wait for next month'
        }
    
    def _get_best_dates_of_month_professional(self, start_date: datetime, sign: str, transits: Dict) -> List[Dict]:
        """Get best dates with detailed reasoning"""
        best_dates = []
        sign_lord = self.SIGN_LORDS[sign]
        
        # Day lord matching sign lord
        weekday_lords = ['Moon', 'Mars', 'Mercury', 'Jupiter', 'Venus', 'Saturn', 'Sun']
        
        current_date = start_date
        count = 0
        while current_date.month == start_date.month and count < 5:
            weekday = current_date.weekday()
            day_lord = weekday_lords[weekday]
            
            if day_lord == sign_lord or day_lord in ['Jupiter', 'Venus']:
                best_dates.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'day': current_date.strftime('%A'),
                    'reason': f'Ruled by {day_lord}' + (' - your sign lord' if day_lord == sign_lord else ' - natural benefic'),
                    'recommendation': 'Excellent for important activities, meetings, and new beginnings'
                })
                count += 1
            
            current_date += timedelta(days=1)
        
        return best_dates[:5]
    
    def _get_challenging_dates(self, start_date: datetime, sign: str, transits: Dict) -> List[Dict]:
        """Get challenging dates to be cautious"""
        challenging = []
        
        # Saturn days (Saturdays) generally require caution
        current_date = start_date
        saturdays = 0
        while current_date.month == start_date.month and saturdays < 2:
            if current_date.weekday() == 5:  # Saturday
                challenging.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'day': 'Saturday',
                    'reason': 'Saturn day requires patience and caution',
                    'advice': 'Avoid major decisions, focus on routine work, practice discipline'
                })
                saturdays += 1
            current_date += timedelta(days=1)
        
        # Add new moon (Amavasya) and full moon if applicable
        # This is simplified - in production you'd calculate exact lunar positions
        
        return challenging
    
    def generate_yearly_horoscope(self, zodiac_sign: str, year: int = None) -> Dict:
        """Generate professional yearly horoscope"""
        if year is None:
            year = datetime.now().year
        
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        
        # Get quarterly transits for comprehensive analysis
        q1_transits = self._get_all_transits(datetime(year, 1, 15))
        q2_transits = self._get_all_transits(datetime(year, 4, 15))
        q3_transits = self._get_all_transits(datetime(year, 7, 15))
        q4_transits = self._get_all_transits(datetime(year, 10, 15))
        
        predictions = self._analyze_yearly_transits_professional(
            zodiac_sign, q1_transits, q2_transits, q3_transits, q4_transits, year
        )
        
        return {
            'sign': zodiac_sign,
            'year': year,
            'period': 'Yearly',
            'quarterly_transits': {
                'Q1_Jan_Mar': q1_transits,
                'Q2_Apr_Jun': q2_transits,
                'Q3_Jul_Sep': q3_transits,
                'Q4_Oct_Dec': q4_transits
            },
            'predictions': predictions,
            'best_months': self._get_best_months_professional(year, zodiac_sign, q1_transits, q2_transits, q3_transits, q4_transits),
            'challenging_periods': self._get_challenging_periods(year, zodiac_sign)
        }
    
    def _analyze_yearly_transits_professional(
        self, sign: str, q1: Dict, q2: Dict, q3: Dict, q4: Dict, year: int
    ) -> Dict:
        """Professional yearly analysis with deep insights"""
        
        sign_num = self.SIGNS.index(sign)
        sign_lord = self.SIGN_LORDS[sign]
        
        # Analyze Jupiter's year-long influence (most important for yearly predictions)
        jupiter_q1_house = ((self.SIGNS.index(q1['Jupiter']['sign']) - sign_num) % 12) + 1
        jupiter_q4_house = ((self.SIGNS.index(q4['Jupiter']['sign']) - sign_num) % 12) + 1
        
        # Analyze Saturn's year-long influence
        saturn_q1_house = ((self.SIGNS.index(q1['Saturn']['sign']) - sign_num) % 12) + 1
        
        # Overall year rating
        year_rating = self._calculate_year_rating(sign, q1, q2, q3, q4)
        
        # Generate comprehensive overview
        year_overview = self._generate_year_overview(sign, year, year_rating, jupiter_q1_house, saturn_q1_house)
        
        # Quarterly breakdown
        quarters = {
            'Q1_January_to_March': self._analyze_quarter(sign, q1, 'Q1', year),
            'Q2_April_to_June': self._analyze_quarter(sign, q2, 'Q2', year),
            'Q3_July_to_September': self._analyze_quarter(sign, q3, 'Q3', year),
            'Q4_October_to_December': self._analyze_quarter(sign, q4, 'Q4', year)
        }
        
        # Life area predictions for entire year
        career_yearly = self._analyze_yearly_career(sign, q1, q2, q3, q4, year)
        love_yearly = self._analyze_yearly_love(sign, q1, q2, q3, q4, year)
        health_yearly = self._analyze_yearly_health(sign, q1, q2, q3, q4, year)
        finance_yearly = self._analyze_yearly_finance(sign, q1, q2, q3, q4, year)
        
        return {
            'overview': year_overview,
            'quarterly_predictions': quarters,
            'career_business': career_yearly,
            'love_relationships': love_yearly,
            'health_wellness': health_yearly,
            'finance_wealth': finance_yearly,
            'spiritual_growth': self._analyze_yearly_spirituality(sign, q1, q2, q3, q4),
            'major_themes': self._identify_yearly_themes(sign, q1, q2, q3, q4, year)
        }
    
    def _calculate_year_rating(self, sign: str, q1: Dict, q2: Dict, q3: Dict, q4: Dict) -> int:
        """Calculate overall year rating"""
        sign_num = self.SIGNS.index(sign)
        total_score = 0
        
        # Weight Jupiter heavily (40%)
        for q in [q1, q2, q3, q4]:
            jupiter_house = ((self.SIGNS.index(q['Jupiter']['sign']) - sign_num) % 12) + 1
            if jupiter_house in [1, 5, 9, 11]:
                total_score += 2
            elif jupiter_house in [2, 10]:
                total_score += 1
        
        # Weight Saturn (30%)
        for q in [q1, q2, q3, q4]:
            saturn_house = ((self.SIGNS.index(q['Saturn']['sign']) - sign_num) % 12) + 1
            if saturn_house in [3, 6, 10, 11]:
                total_score += 1
            elif saturn_house in [1, 4, 7, 8, 12]:
                total_score -= 1
        
        # Other benefics (30%)
        for q in [q1, q2, q3, q4]:
            venus_house = ((self.SIGNS.index(q['Venus']['sign']) - sign_num) % 12) + 1
            if venus_house in [1, 5, 7, 11]:
                total_score += 1
        
        # Normalize to 1-5
        if total_score >= 15:
            return 5
        elif total_score >= 10:
            return 4
        elif total_score >= 5:
            return 3
        elif total_score >= 0:
            return 2
        else:
            return 1
    
    def _generate_year_overview(self, sign: str, year: int, rating: int, jupiter_house: int, saturn_house: int) -> Dict:
        """Generate year overview summary"""
        
        summaries = {
            5: f"Exceptional year ahead for {sign}! {year} brings tremendous growth, success, and fulfillment. Major planetary alignments support all your endeavors.",
            4: f"Very promising year for {sign}! {year} offers excellent opportunities for advancement and happiness. Stay proactive and optimistic.",
            3: f"Balanced year for {sign}. {year} presents mix of opportunities and challenges. Careful planning and persistent effort bring success.",
            2: f"Challenging year for {sign}. {year} requires patience, perseverance, and inner strength. Focus on learning and building foundations.",
            1: f"Difficult period for {sign}. {year} tests your resilience. Practice detachment, strengthen spirituality, and prepare for better times."
        }
        
        summary = summaries[rating]
        
        # Add Jupiter insight
        if jupiter_house in [1, 5, 9, 11]:
            jupiter_insight = f"Jupiter's blessings in your {self._get_house_name(jupiter_house)} bring fortune, wisdom, and expansion."
        elif jupiter_house in [6, 8, 12]:
            jupiter_insight = f"Jupiter's transit through {self._get_house_name(jupiter_house)} teaches valuable life lessons through challenges."
        else:
            jupiter_insight = f"Jupiter's steady influence in {self._get_house_name(jupiter_house)} supports gradual growth."
        
        # Add Saturn insight
        if saturn_house in [1, 7, 10]:
            saturn_insight = f"Saturn's presence in {self._get_house_name(saturn_house)} demands responsibility and hard work, but rewards patience."
        else:
            saturn_insight = f"Saturn's transit brings necessary discipline and karmic lessons."
        
        return {
            'rating': rating,
            'summary': summary,
            'jupiter_influence': jupiter_insight,
            'saturn_influence': saturn_insight,
            'key_message': f'This is a year of {self._get_year_theme(rating, jupiter_house)} for {sign}.'
        }
    
    def _get_year_theme(self, rating: int, jupiter_house: int) -> str:
        """Get main theme of the year"""
        if rating >= 4:
            if jupiter_house in [1, 5]:
                return "personal transformation and creative expression"
            elif jupiter_house in [9, 10]:
                return "fortune, recognition, and career success"
            elif jupiter_house in [7, 11]:
                return "partnerships, relationships, and social gains"
            else:
                return "growth, opportunity, and positive change"
        elif rating == 3:
            return "balanced progress and steady development"
        else:
            return "resilience, inner growth, and karmic lessons"
    
    def _analyze_quarter(self, sign: str, transits: Dict, quarter: str, year: int) -> Dict:
        """Analyze specific quarter"""
        sign_num = self.SIGNS.index(sign)
        
        # Key planetary positions
        sun_house = ((self.SIGNS.index(transits['Sun']['sign']) - sign_num) % 12) + 1
        jupiter_house = ((self.SIGNS.index(transits['Jupiter']['sign']) - sign_num) % 12) + 1
        
        quarter_themes = {
            'Q1': f"Beginning of {year} sets the tone. Focus on planning, goal-setting, and building momentum.",
            'Q2': "Spring energy brings action and growth. Execute plans with confidence and enthusiasm.",
            'Q3': "Mid-year requires consolidation. Review progress and make necessary adjustments.",
            'Q4': "Year-end brings completion. Harvest results and prepare for next year's opportunities."
        }
        
        return {
            'summary': quarter_themes[quarter],
            'focus': self._get_quarter_focus(quarter, jupiter_house),
            'opportunities': self._get_quarter_opportunities(sign, transits, quarter),
            'challenges': self._get_quarter_challenges(sign, transits, quarter)
        }
    
    def _get_quarter_focus(self, quarter: str, jupiter_house: int) -> str:
        """Get focus for the quarter"""
        if quarter == 'Q1':
            return "New beginnings, goal setting, and foundation building"
        elif quarter == 'Q2':
            return "Action, expansion, and seizing opportunities"
        elif quarter == 'Q3':
            return "Relationships, partnerships, and collaboration"
        else:
            return "Completion, harvest, and future planning"
    
    def _get_quarter_opportunities(self, sign: str, transits: Dict, quarter: str) -> List[str]:
        """Identify quarter opportunities"""
        return [
            f"{quarter} brings favorable energy for new initiatives",
            "Jupiter's influence supports expansion and growth",
            "Good period for networking and building connections"
        ]
    
    def _get_quarter_challenges(self, sign: str, transits: Dict, quarter: str) -> List[str]:
        """Identify quarter challenges"""
        if transits['Saturn'].get('is_retrograde') or transits['Mars'].get('is_retrograde'):
            return [
                "Retrograde planets require patience and review",
                "Avoid rushing major decisions",
                "Focus on completing pending tasks"
            ]
        return [
            "Maintain consistent effort despite obstacles",
            "Balance ambition with practical limitations"
        ]
    
    def _analyze_yearly_career(self, sign: str, q1: Dict, q2: Dict, q3: Dict, q4: Dict, year: int) -> Dict:
        """Yearly career predictions"""
        sign_num = self.SIGNS.index(sign)
        
        # Check Saturn (career karma) position throughout year
        saturn_house = ((self.SIGNS.index(q1['Saturn']['sign']) - sign_num) % 12) + 1
        
        if saturn_house == 10:
            return {
                'summary': f"Career-defining year! Saturn in 10th house brings major responsibilities, recognition, and potential promotions. Hard work pays off.",
                'opportunities': ['Leadership roles', 'Industry recognition', 'Long-term career advancement'],
                'challenges': ['Heavy workload', 'Increased pressure', 'Work-life balance'],
                'best_months': ['March', 'June', 'September'],
                'advice': 'Embrace responsibilities. Stay disciplined. Long-term success is assured with patience.'
            }
        elif saturn_house in [3, 6, 11]:
            return {
                'summary': f"Progressive career year. Steady growth through consistent effort. New skills and opportunities emerge.",
                'opportunities': ['Skill development', 'Team leadership', 'Industry networking'],
                'challenges': ['Competition', 'Changing priorities', 'Learning curve'],
                'best_months': ['February', 'May', 'October'],
                'advice': 'Stay adaptable. Invest in learning. Build strong professional relationships.'
            }
        else:
            return {
                'summary': f"Mixed professional year. Some periods favor advancement while others require patience.",
                'opportunities': ['New projects', 'Lateral moves', 'Skill enhancement'],
                'challenges': ['Uncertainty', 'Competition', 'Slow progress at times'],
                'best_months': ['April', 'July', 'November'],
                'advice': 'Focus on consistent performance. Network actively. Be patient with results.'
            }
    
    def _analyze_yearly_love(self, sign: str, q1: Dict, q2: Dict, q3: Dict, q4: Dict, year: int) -> Dict:
        """Yearly love predictions"""
        sign_num = self.SIGNS.index(sign)
        
        # Check Venus throughout year
        venus_positions = []
        for q in [q1, q2, q3, q4]:
            venus_house = ((self.SIGNS.index(q['Venus']['sign']) - sign_num) % 12) + 1
            venus_positions.append(venus_house)
        
        favorable_count = sum(1 for h in venus_positions if h in [1, 5, 7, 11])
        
        if favorable_count >= 3:
            return {
                'summary': f"Romantic year for {sign}! Venus brings love, harmony, and relationship fulfillment. Singles find meaningful connections.",
                'singles': 'High probability of meeting life partner. Spring and autumn especially favorable.',
                'committed': 'Relationships deepen significantly. Good year for engagement, marriage, or starting family.',
                'challenges': ['Managing expectations', 'Balancing independence and togetherness'],
                'best_months': ['March', 'May', 'September', 'November'],
                'advice': 'Be open to love. Communicate honestly. Nurture relationships with care and attention.'
            }
        elif favorable_count >= 2:
            return {
                'summary': f"Good relationship year with periods of romance and harmony. Existing bonds strengthen.",
                'singles': 'Opportunities for dating and connections. Be patient for right match.',
                'committed': 'Relationship stability improves. Work through challenges together.',
                'challenges': ['Occasional misunderstandings', 'External pressures'],
                'best_months': ['May', 'August', 'November'],
                'advice': 'Practice patience. Build emotional intimacy. Enjoy quality time together.'
            }
        else:
            return {
                'summary': f"Relationship year requires effort and understanding. Focus on inner growth and self-love.",
                'singles': 'Year favors self-development over finding partner. Right person comes at right time.',
                'committed': 'Work through relationship challenges. Couples therapy beneficial. Commit to growth.',
                'challenges': ['Communication issues', 'Different priorities', 'External stress'],
                'best_months': ['April', 'August', 'December'],
                'advice': 'Prioritize communication. Practice forgiveness. Focus on long-term relationship health.'
            }
    
    def _analyze_yearly_health(self, sign: str, q1: Dict, q2: Dict, q3: Dict, q4: Dict, year: int) -> Dict:
        """Yearly health predictions"""
        sign_num = self.SIGNS.index(sign)
        
        # Check Mars (vitality) throughout year
        mars_positions = []
        for q in [q1, q2, q3, q4]:
            mars_house = ((self.SIGNS.index(q['Mars']['sign']) - sign_num) % 12) + 1
            mars_positions.append(mars_house)
        
        challenging_count = sum(1 for h in mars_positions if h in [1, 6, 8, 12])
        
        if challenging_count >= 2:
            return {
                'summary': f"Health requires attention this year. Mars positions suggest need for preventive care and lifestyle changes.",
                'focus_areas': ['Stress management', 'Regular checkups', 'Balanced diet', 'Adequate rest'],
                'vulnerable_periods': ['Q1 and Q3 require extra caution'],
                'recommended_practices': ['Daily yoga or meditation', 'Anti-inflammatory diet', 'Regular exercise routine'],
                'advice': 'Prioritize health over ambition. Listen to body signals. Consult healthcare professionals proactively.'
            }
        else:
            return {
                'summary': f"Generally healthy year with good vitality. Minor health issues easily manageable.",
                'focus_areas': ['Maintaining fitness', 'Mental wellness', 'Preventive care'],
                'best_periods': ['Q2 and Q4 especially favorable for fitness goals'],
                'recommended_practices': ['Outdoor activities', 'Sports or athletics', 'Yoga and pranayama'],
                'advice': 'Excellent year to establish healthy habits. Start new fitness routines. Focus on holistic wellness.'
            }
    
    def _analyze_yearly_finance(self, sign: str, q1: Dict, q2: Dict, q3: Dict, q4: Dict, year: int) -> Dict:
        """Yearly finance predictions"""
        sign_num = self.SIGNS.index(sign)
        
        # Check Jupiter (wealth) throughout year
        jupiter_positions = []
        for q in [q1, q2, q3, q4]:
            jupiter_house = ((self.SIGNS.index(q['Jupiter']['sign']) - sign_num) % 12) + 1
            jupiter_positions.append(jupiter_house)
        
        wealth_favorable = sum(1 for h in jupiter_positions if h in [1, 2, 5, 9, 11])
        
        if wealth_favorable >= 3:
            return {
                'summary': f"Financially prosperous year! Jupiter brings wealth, gains, and financial security. Multiple income sources possible.",
                'opportunities': ['Salary increase or bonuses', 'Investment returns', 'Business expansion', 'Property gains'],
                'best_investments': ['Real estate', 'Mutual funds', 'Gold', 'Business ventures'],
                'best_months': ['March-April', 'August-September', 'November-December'],
                'cautions': ['Avoid overconfidence', 'Diversify investments', 'Save for future'],
                'advice': 'Excellent year for financial planning. Invest wisely. Build long-term wealth systematically.'
            }
        elif wealth_favorable >= 2:
            return {
                'summary': f"Stable financial year with growth opportunities. Income increases gradually through consistent effort.",
                'opportunities': ['Regular income growth', 'Smart investments', 'Side income'],
                'best_investments': ['Systematic investment plans', 'Fixed deposits', 'Government bonds'],
                'best_months': ['May', 'August', 'November'],
                'cautions': ['Avoid risky ventures', 'Control unnecessary expenses', 'Emergency fund essential'],
                'advice': 'Focus on savings and prudent investments. Avoid speculation. Build financial discipline.'
            }
        else:
            return {
                'summary': f"Financial caution needed. Year requires careful money management and avoiding risks.",
                'opportunities': ['Learning financial management', 'Debt reduction', 'Budget discipline'],
                'best_investments': ['Only safe, proven options', 'Focus on debt clearance', 'Build emergency corpus'],
                'best_months': ['April', 'September'],
                'cautions': ['Avoid new loans', 'No speculation or gambling', 'Control expenses strictly'],
                'advice': 'Conservative financial approach essential. Clear debts. Focus on earning stability over quick gains.'
            }
    
    def _analyze_yearly_spirituality(self, sign: str, q1: Dict, q2: Dict, q3: Dict, q4: Dict) -> Dict:
        """Yearly spiritual growth predictions"""
        sign_num = self.SIGNS.index(sign)
        
        # Check Ketu (moksha) and Jupiter (wisdom)
        ketu_house = ((self.SIGNS.index(q1['Ketu']['sign']) - sign_num) % 12) + 1
        jupiter_house = ((self.SIGNS.index(q1['Jupiter']['sign']) - sign_num) % 12) + 1
        
        if ketu_house in [1, 4, 9, 12] or jupiter_house in [9, 12]:
            return {
                'summary': 'Spiritually significant year. Deep inner transformation and wisdom seeking.',
                'focus': ['Meditation and mindfulness', 'Philosophical studies', 'Pilgrimage or spiritual retreats'],
                'benefits': 'Enhanced intuition, inner peace, and life purpose clarity',
                'practices': ['Daily meditation', 'Study of scriptures', 'Service to others']
            }
        else:
            return {
                'summary': 'Material focus year with opportunities for spiritual practices.',
                'focus': ['Balancing material and spiritual', 'Regular prayer or meditation', 'Charity work'],
                'benefits': 'Stress management and emotional balance',
                'practices': ['Weekend spiritual activities', 'Nature connection', 'Gratitude journaling']
            }
    
    def _identify_yearly_themes(self, sign: str, q1: Dict, q2: Dict, q3: Dict, q4: Dict, year: int) -> List[str]:
        """Identify major themes for the year"""
        themes = []
        sign_num = self.SIGNS.index(sign)
        
        # Jupiter theme
        jupiter_house = ((self.SIGNS.index(q1['Jupiter']['sign']) - sign_num) % 12) + 1
        if jupiter_house in [1, 5, 9]:
            themes.append("Personal Growth and Self-Discovery")
        elif jupiter_house in [2, 11]:
            themes.append("Financial Prosperity and Wealth Building")
        elif jupiter_house in [7, 10]:
            themes.append("Partnership and Career Success")
        
        # Saturn theme
        saturn_house = ((self.SIGNS.index(q1['Saturn']['sign']) - sign_num) % 12) + 1
        if saturn_house in [1, 7, 10]:
            themes.append("Responsibility and Karmic Lessons")
        elif saturn_house in [4, 8, 12]:
            themes.append("Inner Transformation and Letting Go")
        
        # Rahu-Ketu theme
        rahu_house = ((self.SIGNS.index(q1['Rahu']['sign']) - sign_num) % 12) + 1
        if rahu_house in [1, 7]:
            themes.append("Identity and Relationship Evolution")
        elif rahu_house in [10, 4]:
            themes.append("Career-Home Balance and Priorities")
        
        return themes if themes else ["Steady Progress and Development"]
    
    def _get_best_months_professional(
        self, year: int, sign: str, q1: Dict, q2: Dict, q3: Dict, q4: Dict
    ) -> List[Dict]:
        """Get best months with detailed reasoning"""
        sign_num = self.SIGNS.index(sign)
        months_data = []
        
        # Analyze each quarter's midpoint
        quarters = [
            (q1, 'February', 'Q1'),
            (q2, 'May', 'Q2'),
            (q3, 'August', 'Q3'),
            (q4, 'November', 'Q4')
        ]
        
        for transits, month, quarter in quarters:
            jupiter_house = ((self.SIGNS.index(transits['Jupiter']['sign']) - sign_num) % 12) + 1
            venus_house = ((self.SIGNS.index(transits['Venus']['sign']) - sign_num) % 12) + 1
            
            rating = 0
            reasons = []
            
            if jupiter_house in [1, 5, 9, 10, 11]:
                rating += 2
                reasons.append(f"Jupiter in {self._get_house_name(jupiter_house)}")
            
            if venus_house in [1, 5, 7, 11]:
                rating += 1
                reasons.append("Venus favors relationships and luxury")
            
            if rating >= 2:
                months_data.append({
                    'month': month,
                    'quarter': quarter,
                    'rating': min(5, rating),
                    'reasons': reasons,
                    'best_for': self._get_month_best_activities(jupiter_house, venus_house)
                })
        
        # Sort by rating and return top months
        months_data.sort(key=lambda x: x['rating'], reverse=True)
        return months_data[:4] if months_data else [{
            'month': 'March',
            'rating': 3,
            'reasons': ['Spring energy favors new beginnings'],
            'best_for': ['General activities', 'Planning', 'New initiatives']
        }]
    
    def _get_month_best_activities(self, jupiter_house: int, venus_house: int) -> List[str]:
        """Get best activities for the month"""
        activities = []
        
        if jupiter_house in [1, 5]:
            activities.extend(['Personal projects', 'Creative pursuits'])
        elif jupiter_house in [9, 10]:
            activities.extend(['Career initiatives', 'Education'])
        elif jupiter_house in [2, 11]:
            activities.extend(['Financial planning', 'Investments'])
        
        if venus_house in [5, 7]:
            activities.extend(['Romance', 'Socializing'])
        elif venus_house in [2, 11]:
            activities.extend(['Shopping', 'Luxury purchases'])
        
        return activities if activities else ['General life activities']
    
    def _get_challenging_periods(self, year: int, sign: str) -> List[Dict]:
        """Identify challenging periods in the year"""
        return [
            {
                'period': 'Late January - Early February',
                'reason': 'Saturn-Sun conjunction may bring authority challenges',
                'advice': 'Stay humble, work diligently, avoid conflicts'
            },
            {
                'period': 'Any Mercury retrograde periods',
                'reason': 'Communication and technology issues',
                'advice': 'Double-check details, backup data, review contracts'
            },
            {
                'period': 'Eclipse seasons',
                'reason': 'Rahu-Ketu axis brings unexpected changes',
                'advice': 'Practice flexibility, avoid major decisions near eclipses'
            }
        ]


# Global instance
transit_horoscope = TransitHoroscope()

