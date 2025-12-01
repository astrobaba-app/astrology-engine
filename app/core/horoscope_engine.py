"""
Horoscope Generation Engine
"""
from typing import Dict, List
from datetime import datetime


class HoroscopeEngine:
    """Generate comprehensive horoscope reports"""
    
    def generate_birth_horoscope(
        self,
        chart_data: Dict,
        yogas_doshas: Dict,
        dashas: Dict,
        divisional_charts: Dict,
        ashtakavarga: Dict = None
    ) -> Dict:
        """
        Generate comprehensive birth horoscope report
        
        Args:
            chart_data: Complete birth chart
            yogas_doshas: Yoga and dosha analysis
            dashas: Dasha periods
            divisional_charts: All divisional charts
            ashtakavarga: Ashtakavarga analysis
            
        Returns:
            Comprehensive horoscope report
        """
        report = {
            'basic_details': self._extract_basic_details(chart_data),
            'personality_analysis': self._analyze_personality(chart_data),
            'life_areas': self._analyze_life_areas(chart_data),
            'planetary_analysis': self._analyze_planets(chart_data),
            'yoga_analysis': self._format_yogas(yogas_doshas.get('yogas', {})),
            'dosha_analysis': self._format_doshas(yogas_doshas.get('doshas', {})),
            'dasha_predictions': self._format_dasha_predictions(dashas),
            'divisional_insights': self._analyze_divisional_charts(divisional_charts),
            'strengths_weaknesses': self._identify_strengths_weaknesses(chart_data, yogas_doshas),
            'career_guidance': self._generate_career_guidance(chart_data, divisional_charts),
            'relationship_guidance': self._generate_relationship_guidance(chart_data, divisional_charts),
            'health_indications': self._analyze_health(chart_data),
            'financial_prospects': self._analyze_finances(chart_data, yogas_doshas),
            'spiritual_path': self._analyze_spirituality(chart_data),
            'recommendations': self._generate_recommendations(chart_data, yogas_doshas)
        }
        
        if ashtakavarga:
            report['ashtakavarga_insights'] = self._format_ashtakavarga(ashtakavarga)
        
        return report
    
    def _extract_basic_details(self, chart_data: Dict) -> Dict:
        """Extract basic birth details"""
        birth_details = chart_data['birth_details']
        ascendant = chart_data['ascendant']
        
        return {
            'birth_date': birth_details['date'],
            'birth_location': f"Lat: {birth_details['latitude']}, Long: {birth_details['longitude']}",
            'timezone': birth_details['timezone'],
            'ayanamsa': f"{birth_details['ayanamsa']}°",
            'ascendant_sign': ascendant['sign'],
            'ascendant_degree': f"{ascendant['degree']:.2f}°",
            'chart_type': 'Vedic (Sidereal)'
        }
    
    def _analyze_personality(self, chart_data: Dict) -> Dict:
        """Analyze personality based on ascendant and Moon"""
        ascendant = chart_data['ascendant']
        moon = chart_data['planets']['Moon']
        sun = chart_data['planets']['Sun']
        
        # Ascendant-based personality
        asc_personality = self._get_sign_personality(ascendant['sign'])
        
        # Moon sign emotional nature
        moon_nature = self._get_moon_nature(moon['sign'])
        
        # Sun sign ego/soul
        sun_nature = self._get_sun_nature(sun['sign'])
        
        return {
            'ascendant_influence': {
                'sign': ascendant['sign'],
                'description': asc_personality,
                'physical_appearance': self._get_physical_traits(ascendant['sign'])
            },
            'moon_influence': {
                'sign': moon['sign'],
                'nakshatra': moon['nakshatra'],
                'description': moon_nature,
                'emotional_nature': self._get_emotional_traits(moon['sign'])
            },
            'sun_influence': {
                'sign': sun['sign'],
                'description': sun_nature,
                'life_purpose': self._get_life_purpose(sun['sign'])
            },
            'overall_personality': self._synthesize_personality(ascendant['sign'], moon['sign'], sun['sign'])
        }
    
    def _analyze_life_areas(self, chart_data: Dict) -> Dict:
        """Analyze all 12 houses and life areas"""
        houses_analysis = {}
        
        house_meanings = {
            1: {'area': 'Self & Personality', 'description': 'Physical body, health, appearance'},
            2: {'area': 'Wealth & Family', 'description': 'Money, speech, family values'},
            3: {'area': 'Courage & Siblings', 'description': 'Communication, short travels, siblings'},
            4: {'area': 'Home & Mother', 'description': 'Property, vehicles, emotional peace'},
            5: {'area': 'Children & Education', 'description': 'Creativity, intelligence, romance'},
            6: {'area': 'Health & Service', 'description': 'Enemies, diseases, daily work'},
            7: {'area': 'Marriage & Partnership', 'description': 'Spouse, business partners'},
            8: {'area': 'Longevity & Transformation', 'description': 'Occult, inheritance, sudden events'},
            9: {'area': 'Fortune & Dharma', 'description': 'Higher education, father, spirituality'},
            10: {'area': 'Career & Status', 'description': 'Profession, reputation, authority'},
            11: {'area': 'Gains & Friends', 'description': 'Income, social circle, desires'},
            12: {'area': 'Losses & Liberation', 'description': 'Expenses, foreign lands, moksha'}
        }
        
        planet_houses = chart_data['planet_houses']
        
        for house_num in range(1, 13):
            # Find planets in this house
            planets_in_house = [p for p, h in planet_houses.items() if h == house_num]
            
            house_info = house_meanings[house_num]
            
            houses_analysis[f'house_{house_num}'] = {
                'area': house_info['area'],
                'description': house_info['description'],
                'planets': planets_in_house,
                'strength': self._assess_house_strength(house_num, planets_in_house, chart_data),
                'prediction': self._predict_house_results(house_num, planets_in_house)
            }
        
        return houses_analysis
    
    def _analyze_planets(self, chart_data: Dict) -> Dict:
        """Detailed planetary analysis"""
        planets = chart_data['planets']
        strengths = chart_data['strengths']
        
        analysis = {}
        
        planet_significations = {
            'Sun': 'Soul, father, authority, government',
            'Moon': 'Mind, mother, emotions, public',
            'Mars': 'Energy, courage, siblings, property',
            'Mercury': 'Intelligence, communication, business',
            'Jupiter': 'Wisdom, children, wealth, dharma',
            'Venus': 'Love, luxury, arts, spouse',
            'Saturn': 'Discipline, karma, delays, longevity',
            'Rahu': 'Materialism, foreign, sudden events',
            'Ketu': 'Spirituality, detachment, moksha'
        }
        
        for planet_name, planet_data in planets.items():
            strength_data = strengths.get(planet_name, {})
            
            analysis[planet_name] = {
                'position': f"{planet_data['sign']} {planet_data['sign_degree']:.2f}°",
                'nakshatra': planet_data['nakshatra'],
                'house': chart_data['planet_houses'][planet_name],
                'strength_percentage': strength_data.get('percentage', 0),
                'is_retrograde': planet_data.get('is_retrograde', False),
                'significations': planet_significations.get(planet_name, ''),
                'condition': self._assess_planet_condition(planet_data, strength_data),
                'effects': self._predict_planet_effects(planet_name, planet_data, chart_data)
            }
        
        return analysis
    
    def _format_yogas(self, yogas: Dict) -> List[Dict]:
        """Format yoga analysis for report"""
        formatted = []
        
        for yoga_type, yoga_list in yogas.items():
            for yoga in yoga_list:
                formatted.append({
                    'type': yoga_type.replace('_', ' ').title(),
                    'name': yoga['name'],
                    'strength': yoga.get('strength', 'Medium'),
                    'description': yoga['description'],
                    'effects': self._get_yoga_effects(yoga)
                })
        
        return formatted
    
    def _format_doshas(self, doshas: Dict) -> List[Dict]:
        """Format dosha analysis for report"""
        formatted = []
        
        for dosha_name, dosha_data in doshas.items():
            if dosha_data.get('present'):
                formatted.append({
                    'name': dosha_name.replace('_', ' ').title(),
                    'severity': dosha_data.get('severity', 'Medium'),
                    'description': dosha_data.get('description', ''),
                    'effects': dosha_data.get('effects', ''),
                    'remedies': dosha_data.get('remedies', []),
                    'cancellations': dosha_data.get('cancellations', [])
                })
        
        return formatted
    
    def _format_dasha_predictions(self, dashas: Dict) -> Dict:
        """Format dasha predictions"""
        if not dashas:
            return {}
        
        current_time = datetime.now().strftime('%Y-%m-%d')
        
        # Find current dasha
        current_dasha = None
        for dasha in dashas.get('dashas', []):
            if dasha['start_date'] <= current_time <= dasha['end_date']:
                current_dasha = dasha
                break
        
        return {
            'birth_nakshatra': dashas.get('birth_nakshatra', ''),
            'birth_dasha_lord': dashas.get('birth_nakshatra_lord', ''),
            'current_dasha': current_dasha,
            'dasha_interpretation': self._interpret_dasha(current_dasha) if current_dasha else None
        }
    
    def _analyze_divisional_charts(self, div_charts: Dict) -> Dict:
        """Analyze key divisional charts"""
        insights = {}
        
        key_charts = {
            'D9': 'Marriage and spiritual evolution',
            'D10': 'Career and professional success',
            'D7': 'Children and progeny',
            'D12': 'Parents and ancestry'
        }
        
        for div, significance in key_charts.items():
            if div in div_charts:
                insights[div] = {
                    'name': div_charts[div]['name'],
                    'significance': significance,
                    'key_placements': self._analyze_div_chart_placements(div_charts[div])
                }
        
        return insights
    
    def _identify_strengths_weaknesses(self, chart_data: Dict, yogas_doshas: Dict) -> Dict:
        """Identify person's strengths and weaknesses"""
        strengths = chart_data['strengths']
        
        strong_planets = [p for p, s in strengths.items() if s.get('percentage', 0) >= 60]
        weak_planets = [p for p, s in strengths.items() if s.get('percentage', 0) < 40]
        
        return {
            'strengths': {
                'strong_planets': strong_planets,
                'beneficial_yogas': len(yogas_doshas.get('yogas', {}).get('raj_yogas', [])),
                'positive_traits': self._get_positive_traits(strong_planets),
                'natural_talents': self._get_talents(chart_data)
            },
            'weaknesses': {
                'weak_planets': weak_planets,
                'doshas_present': len([d for d in yogas_doshas.get('doshas', {}).values() if d.get('present')]),
                'challenges': self._get_challenges(weak_planets),
                'areas_for_improvement': self._get_improvement_areas(chart_data)
            }
        }
    
    def _generate_career_guidance(self, chart_data: Dict, div_charts: Dict) -> Dict:
        """Generate career guidance"""
        tenth_house = chart_data['planet_houses']
        planets_in_10th = [p for p, h in tenth_house.items() if h == 10]
        
        return {
            'suitable_professions': self._suggest_professions(chart_data),
            'career_strength': 'High' if len(planets_in_10th) > 0 else 'Medium',
            'best_career_periods': 'During favorable Dasha periods',
            'business_vs_job': self._assess_business_job(chart_data),
            'success_indicators': self._identify_career_success(chart_data)
        }
    
    def _generate_relationship_guidance(self, chart_data: Dict, div_charts: Dict) -> Dict:
        """Generate relationship and marriage guidance"""
        seventh_house = chart_data['planet_houses']
        planets_in_7th = [p for p, h in seventh_house.items() if h == 7]
        
        venus = chart_data['planets']['Venus']
        
        return {
            'marriage_timing': self._predict_marriage_timing(chart_data),
            'spouse_characteristics': self._describe_spouse(chart_data),
            'relationship_harmony': self._assess_relationship_harmony(chart_data),
            'compatibility_factors': self._get_compatibility_factors(chart_data)
        }
    
    def _analyze_health(self, chart_data: Dict) -> Dict:
        """Analyze health indications"""
        sixth_house = chart_data['planet_houses']
        planets_in_6th = [p for p, h in sixth_house.items() if h == 6]
        
        ascendant = chart_data['ascendant']['sign']
        
        return {
            'constitution': self._get_constitution(ascendant),
            'vulnerable_areas': self._identify_health_vulnerabilities(chart_data),
            'health_strength': 'Good' if len(planets_in_6th) == 0 else 'Requires attention',
            'preventive_measures': self._suggest_health_measures(chart_data)
        }
    
    def _analyze_finances(self, chart_data: Dict, yogas_doshas: Dict) -> Dict:
        """Analyze financial prospects"""
        wealth_houses = [2, 5, 9, 11]
        planets_in_wealth = [p for p, h in chart_data['planet_houses'].items() if h in wealth_houses]
        
        dhana_yogas = yogas_doshas.get('yogas', {}).get('dhana_yogas', [])
        
        return {
            'wealth_potential': 'High' if len(dhana_yogas) > 0 else 'Medium',
            'income_sources': self._identify_income_sources(chart_data),
            'savings_ability': self._assess_savings(chart_data),
            'financial_periods': 'Best during Jupiter and Venus periods'
        }
    
    def _analyze_spirituality(self, chart_data: Dict) -> Dict:
        """Analyze spiritual inclinations"""
        ninth_house = chart_data['planet_houses']
        twelfth_house = chart_data['planet_houses']
        
        jupiter = chart_data['planets']['Jupiter']
        ketu = chart_data['planets']['Ketu']
        
        return {
            'spiritual_inclination': self._assess_spiritual_nature(chart_data),
            'recommended_practices': self._suggest_spiritual_practices(chart_data),
            'moksha_indicators': self._identify_moksha_indicators(chart_data),
            'guru_connection': self._assess_guru_connection(jupiter)
        }
    
    def _generate_recommendations(self, chart_data: Dict, yogas_doshas: Dict) -> Dict:
        """Generate overall recommendations"""
        return {
            'favorable_periods': 'Jupiter and Venus Mahadashas',
            'challenging_periods': 'Saturn and Rahu Mahadashas - use remedies',
            'lucky_days': self._get_lucky_days(chart_data),
            'lucky_numbers': self._get_lucky_numbers(chart_data),
            'lucky_colors': self._get_lucky_colors(chart_data),
            'gemstone_recommendations': 'See detailed remedies section',
            'general_advice': [
                'Follow dharmic path for best results',
                'Strengthen weak planets through remedies',
                'Utilize favorable Dasha periods for major decisions',
                'Regular spiritual practice recommended',
                'Maintain good health through preventive care'
            ]
        }
    
    # Helper methods (simplified implementations)
    def _get_sign_personality(self, sign: str) -> str:
        personalities = {
            'Aries': 'Dynamic, energetic, leadership qualities',
            'Taurus': 'Stable, practical, artistic',
            'Gemini': 'Communicative, intellectual, versatile',
            'Cancer': 'Emotional, nurturing, intuitive',
            'Leo': 'Confident, generous, authoritative',
            'Virgo': 'Analytical, perfectionist, service-oriented',
            'Libra': 'Balanced, diplomatic, relationship-focused',
            'Scorpio': 'Intense, transformative, mysterious',
            'Sagittarius': 'Philosophical, optimistic, adventurous',
            'Capricorn': 'Disciplined, ambitious, practical',
            'Aquarius': 'Innovative, humanitarian, independent',
            'Pisces': 'Spiritual, compassionate, imaginative'
        }
        return personalities.get(sign, 'Unique personality')
    
    def _get_moon_nature(self, sign: str) -> str:
        return f"Emotionally {self._get_sign_personality(sign).lower()}"
    
    def _get_sun_nature(self, sign: str) -> str:
        return f"Core identity: {self._get_sign_personality(sign)}"
    
    def _get_physical_traits(self, sign: str) -> str:
        return "Refer to ascendant sign characteristics"
    
    def _get_emotional_traits(self, sign: str) -> str:
        return "Refer to moon sign characteristics"
    
    def _get_life_purpose(self, sign: str) -> str:
        return "Self-realization through Sun sign path"
    
    def _synthesize_personality(self, asc: str, moon: str, sun: str) -> str:
        return f"Personality is a blend of {asc} ascendant, {moon} moon, and {sun} sun influences"
    
    def _assess_house_strength(self, house: int, planets: List, chart: Dict) -> str:
        return 'Strong' if len(planets) > 0 else 'Average'
    
    def _predict_house_results(self, house: int, planets: List) -> str:
        return 'Positive results expected' if len(planets) > 0 else 'Requires effort'
    
    def _assess_planet_condition(self, planet: Dict, strength: Dict) -> str:
        percentage = strength.get('percentage', 0)
        if percentage >= 60:
            return 'Excellent'
        elif percentage >= 40:
            return 'Good'
        else:
            return 'Needs strengthening'
    
    def _predict_planet_effects(self, name: str, planet: Dict, chart: Dict) -> str:
        return f"{name} will give results according to its placement and strength"
    
    def _get_yoga_effects(self, yoga: Dict) -> str:
        return "Beneficial effects in life"
    
    def _interpret_dasha(self, dasha: Dict) -> str:
        return f"Current {dasha['planet']} period brings specific results"
    
    def _analyze_div_chart_placements(self, chart: Dict) -> str:
        return "Key planetary positions analyzed"
    
    def _get_positive_traits(self, planets: List) -> List[str]:
        return [f"Strong {p} indicates positive traits" for p in planets]
    
    def _get_talents(self, chart: Dict) -> List[str]:
        return ["Natural talents based on chart analysis"]
    
    def _get_challenges(self, planets: List) -> List[str]:
        return [f"Weak {p} may cause challenges" for p in planets]
    
    def _get_improvement_areas(self, chart: Dict) -> List[str]:
        return ["Areas identified for personal growth"]
    
    def _suggest_professions(self, chart: Dict) -> List[str]:
        return ["Professions based on 10th house analysis"]
    
    def _assess_business_job(self, chart: Dict) -> str:
        return "Job recommended" # Simplified
    
    def _identify_career_success(self, chart: Dict) -> List[str]:
        return ["Success indicators identified"]
    
    def _predict_marriage_timing(self, chart: Dict) -> str:
        return "Marriage timing based on 7th house and Venus"
    
    def _describe_spouse(self, chart: Dict) -> str:
        return "Spouse characteristics from 7th house"
    
    def _assess_relationship_harmony(self, chart: Dict) -> str:
        return "Harmony assessment based on Venus"
    
    def _get_compatibility_factors(self, chart: Dict) -> List[str]:
        return ["Compatibility factors identified"]
    
    def _get_constitution(self, sign: str) -> str:
        return "Constitutional type based on ascendant"
    
    def _identify_health_vulnerabilities(self, chart: Dict) -> List[str]:
        return ["Health areas needing attention"]
    
    def _suggest_health_measures(self, chart: Dict) -> List[str]:
        return ["Preventive health measures"]
    
    def _identify_income_sources(self, chart: Dict) -> List[str]:
        return ["Potential income sources"]
    
    def _assess_savings(self, chart: Dict) -> str:
        return "Savings ability assessment"
    
    def _assess_spiritual_nature(self, chart: Dict) -> str:
        return "Spiritual inclination analysis"
    
    def _suggest_spiritual_practices(self, chart: Dict) -> List[str]:
        return ["Recommended spiritual practices"]
    
    def _identify_moksha_indicators(self, chart: Dict) -> List[str]:
        return ["Liberation indicators"]
    
    def _assess_guru_connection(self, jupiter: Dict) -> str:
        return "Guru/teacher connection strength"
    
    def _get_lucky_days(self, chart: Dict) -> List[str]:
        return ["Lucky days of week"]
    
    def _get_lucky_numbers(self, chart: Dict) -> List[int]:
        return [1, 3, 5, 9]  # Example
    
    def _get_lucky_colors(self, chart: Dict) -> List[str]:
        return ["Colors based on planetary influences"]
    
    def _format_ashtakavarga(self, ashtak: Dict) -> Dict:
        return {"summary": "Ashtakavarga analysis included"}


# Global instance
horoscope_engine = HoroscopeEngine()
