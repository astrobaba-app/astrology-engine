"""
Enhanced Kundli Matching endpoints - AstroTalk level compatibility
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
from typing import Dict, List
from pydantic import BaseModel
from app.api.v1.models import BirthData, MatchingRequest
from app.core.chart_engine import chart_engine
from app.core.matching.ashtakoot import ashtakoot_matching
from app.core.matching.dashakoot import dashakoot_matching
from app.core.vedic.yogas_doshas import yoga_dosha_calculator
from app.core.vedic.dasha import dasha_calculator

router = APIRouter()


class EnhancedMatchingRequest(BaseModel):
    """Enhanced matching request"""
    male_data: BirthData
    female_data: BirthData
    include_detailed_analysis: bool = True


@router.post("/comprehensive")
async def comprehensive_kundli_matching(request: EnhancedMatchingRequest):
    """
    Comprehensive Kundli matching with:
    - Ashtakoot (36 Gunas)
    - Mangal Dosha analysis for both
    - Dashas compatibility
    - Planetary friendship
    - Longevity analysis
    - Children prospects
    - Financial compatibility
    - Detailed recommendations
    """
    try:
        male_data = request.male_data
        female_data = request.female_data
        
        # Parse datetimes
        male_date_str = f"{male_data.date} {male_data.time}"
        male_datetime = datetime.strptime(male_date_str, '%Y-%m-%d %H:%M:%S')
        
        female_date_str = f"{female_data.date} {female_data.time}"
        female_datetime = datetime.strptime(female_date_str, '%Y-%m-%d %H:%M:%S')
        
        # Get charts
        male_chart = chart_engine.calculate_birth_chart(
            date=male_datetime,
            latitude=male_data.latitude,
            longitude=male_data.longitude,
            timezone=male_data.timezone
        )
        
        female_chart = chart_engine.calculate_birth_chart(
            date=female_datetime,
            latitude=female_data.latitude,
            longitude=female_data.longitude,
            timezone=female_data.timezone
        )
        
        # 1. Ashtakoot Matching (36 Gunas)
        male_moon = male_chart['planets']['Moon']
        female_moon = female_chart['planets']['Moon']
        
        ashtakoot = ashtakoot_matching.calculate_ashtakoot_matching(
            male_moon_sign=male_moon['sign'],
            male_moon_sign_num=male_moon['sign_num'],
            male_nakshatra=male_moon['nakshatra'],
            male_nakshatra_num=male_moon['nakshatra_num'],
            female_moon_sign=female_moon['sign'],
            female_moon_sign_num=female_moon['sign_num'],
            female_nakshatra=female_moon['nakshatra'],
            female_nakshatra_num=female_moon['nakshatra_num']
        )
        
        # 1b. Dashakoot Matching (10 Gunas) - Extended version
        dashakoot = dashakoot_matching.calculate_dashakoot_matching(
            male_moon_sign=male_moon['sign'],
            male_moon_sign_num=male_moon['sign_num'],
            male_nakshatra=male_moon['nakshatra'],
            male_nakshatra_num=male_moon['nakshatra_num'],
            female_moon_sign=female_moon['sign'],
            female_moon_sign_num=female_moon['sign_num'],
            female_nakshatra=female_moon['nakshatra'],
            female_nakshatra_num=female_moon['nakshatra_num']
        )
        
        # 2. Mangal Dosha Analysis
        male_mangal = yoga_dosha_calculator.detect_mangal_dosha(
            male_chart['planets'],
            male_chart['planet_houses']
        )
        
        female_mangal = yoga_dosha_calculator.detect_mangal_dosha(
            female_chart['planets'],
            female_chart['planet_houses']
        )
        
        mangal_compatibility = _analyze_mangal_dosha_compatibility(male_mangal, female_mangal)
        
        # 3. Dasha Compatibility
        male_moon_long = male_chart['planets']['Moon']['longitude']
        female_moon_long = female_chart['planets']['Moon']['longitude']
        
        male_dashas = dasha_calculator.calculate_vimshottari_dasha(
            moon_longitude=male_moon_long,
            birth_date=male_datetime,
            years=120
        )
        
        female_dashas = dasha_calculator.calculate_vimshottari_dasha(
            moon_longitude=female_moon_long,
            birth_date=female_datetime,
            years=120
        )
        
        dasha_compatibility = _analyze_dasha_compatibility(male_dashas, female_dashas)
        
        # 4. Planetary Compatibility
        planetary_compatibility = _analyze_planetary_compatibility(male_chart, female_chart)
        
        # 5. House Analysis for Marriage
        marriage_analysis = _analyze_marriage_houses(male_chart, female_chart)
        
        # 6. Children Prospects
        children_analysis = _analyze_children_prospects(male_chart, female_chart)
        
        # 7. Financial Compatibility
        financial_analysis = _analyze_financial_compatibility(male_chart, female_chart)
        
        # 8. Longevity & Health
        health_compatibility = _analyze_health_longevity(male_chart, female_chart)
        
        # 9. Overall Compatibility Score
        overall_score = _calculate_overall_compatibility(
            ashtakoot, mangal_compatibility, dasha_compatibility,
            planetary_compatibility, marriage_analysis
        )
        
        # 10. Recommendations
        recommendations = _generate_matching_recommendations(
            overall_score, ashtakoot, mangal_compatibility, 
            male_chart, female_chart
        )
        
        return {
            "success": True,
            "male_name": male_data.name,
            "female_name": female_data.name,
            "overall_compatibility": {
                "score": overall_score['score'],
                "percentage": overall_score['percentage'],
                "rating": overall_score['rating'],
                "verdict": overall_score['verdict']
            },
            "ashtakoot_matching": ashtakoot,
            "dashakoot_matching": dashakoot,
            "mangal_dosha": {
                "male": male_mangal,
                "female": female_mangal,
                "compatibility": mangal_compatibility
            },
            "dasha_compatibility": dasha_compatibility,
            "planetary_compatibility": planetary_compatibility,
            "marriage_prospects": marriage_analysis,
            "children_prospects": children_analysis,
            "financial_compatibility": financial_analysis,
            "health_longevity": health_compatibility,
            "recommendations": recommendations,
            "remedies": _get_matching_remedies(overall_score, mangal_compatibility)
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/quick-match")
async def quick_kundli_matching(request: MatchingRequest):
    """
    Quick Kundli matching - Ashtakoot + Mangal Dosha only
    """
    try:
        male_data = request.male_data
        female_data = request.female_data
        
        male_date_str = f"{male_data.date} {male_data.time}"
        male_datetime = datetime.strptime(male_date_str, '%Y-%m-%d %H:%M:%S')
        
        female_date_str = f"{female_data.date} {female_data.time}"
        female_datetime = datetime.strptime(female_date_str, '%Y-%m-%d %H:%M:%S')
        
        male_chart = chart_engine.calculate_birth_chart(
            date=male_datetime,
            latitude=male_data.latitude,
            longitude=male_data.longitude,
            timezone=male_data.timezone
        )
        
        female_chart = chart_engine.calculate_birth_chart(
            date=female_datetime,
            latitude=female_data.latitude,
            longitude=female_data.longitude,
            timezone=female_data.timezone
        )
        
        male_moon = male_chart['planets']['Moon']
        female_moon = female_chart['planets']['Moon']
        
        ashtakoot = ashtakoot_matching.calculate_ashtakoot_matching(
            male_moon_sign=male_moon['sign'],
            male_moon_sign_num=male_moon['sign_num'],
            male_nakshatra=male_moon['nakshatra'],
            male_nakshatra_num=male_moon['nakshatra_num'],
            female_moon_sign=female_moon['sign'],
            female_moon_sign_num=female_moon['sign_num'],
            female_nakshatra=female_moon['nakshatra'],
            female_nakshatra_num=female_moon['nakshatra_num']
        )
        
        # Dashakoot (10 Gunas)
        dashakoot = dashakoot_matching.calculate_dashakoot_matching(
            male_moon_sign=male_moon['sign'],
            male_moon_sign_num=male_moon['sign_num'],
            male_nakshatra=male_moon['nakshatra'],
            male_nakshatra_num=male_moon['nakshatra_num'],
            female_moon_sign=female_moon['sign'],
            female_moon_sign_num=female_moon['sign_num'],
            female_nakshatra=female_moon['nakshatra'],
            female_nakshatra_num=female_moon['nakshatra_num']
        )
        
        male_mangal = yoga_dosha_calculator.detect_mangal_dosha(
            male_chart['planets'],
            male_chart['planet_houses']
        )
        
        female_mangal = yoga_dosha_calculator.detect_mangal_dosha(
            female_chart['planets'],
            female_chart['planet_houses']
        )
        
        mangal_compatibility = _analyze_mangal_dosha_compatibility(male_mangal, female_mangal)
        
        # Quick verdict
        total_score = ashtakoot.get('total_score', 0)
        verdict = "Excellent Match" if total_score >= 28 else \
                 "Very Good Match" if total_score >= 24 else \
                 "Good Match" if total_score >= 18 else \
                 "Average Match" if total_score >= 12 else \
                 "Below Average Match"
        
        return {
            "success": True,
            "male_name": male_data.name,
            "female_name": female_data.name,
            "guna_score": f"{total_score}/36",
            "dashakoot_score": f"{dashakoot.get('total_points', 0)}/38",
            "percentage": round((total_score / 36) * 100, 1),
            "verdict": verdict,
            "ashtakoot_details": ashtakoot,
            "dashakoot_details": dashakoot,
            "mangal_dosha": {
                "male": male_mangal,
                "female": female_mangal,
                "compatible": mangal_compatibility['compatible']
            }
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


# Helper Functions

def _analyze_mangal_dosha_compatibility(male_mangal: Dict, female_mangal: Dict) -> Dict:
    """Analyze Mangal Dosha compatibility between couple"""
    male_has = male_mangal.get('has_dosha', False)
    female_has = female_mangal.get('has_dosha', False)
    
    if not male_has and not female_has:
        return {
            "compatible": True,
            "status": "Excellent - No Mangal Dosha",
            "description": "Neither partner has Mangal Dosha. This is ideal for marital harmony."
        }
    elif male_has and female_has:
        return {
            "compatible": True,
            "status": "Good - Both have Mangal Dosha (Cancellation)",
            "description": "Both partners have Mangal Dosha which cancels out. Marriage is auspicious."
        }
    else:
        affected_person = "Male" if male_has else "Female"
        return {
            "compatible": False,
            "status": f"Challenging - Only {affected_person} has Mangal Dosha",
            "description": f"{affected_person} has Mangal Dosha while partner doesn't. Remedies strongly recommended.",
            "severity": male_mangal.get('severity', 'Medium') if male_has else female_mangal.get('severity', 'Medium')
        }


def _analyze_dasha_compatibility(male_dashas: Dict, female_dashas: Dict) -> Dict:
    """Analyze Dasha period compatibility"""
    current_date = datetime.now()
    
    # Get current mahadashas
    male_current = None
    female_current = None
    
    for maha in male_dashas.get('mahadasha_periods', []):
        start = datetime.fromisoformat(maha['start_date'].replace('Z', '+00:00'))
        end = datetime.fromisoformat(maha['end_date'].replace('Z', '+00:00'))
        if start <= current_date <= end:
            male_current = maha['planet']
            break
    
    for maha in female_dashas.get('mahadasha_periods', []):
        start = datetime.fromisoformat(maha['start_date'].replace('Z', '+00:00'))
        end = datetime.fromisoformat(maha['end_date'].replace('Z', '+00:00'))
        if start <= current_date <= end:
            female_current = maha['planet']
            break
    
    # Analyze compatibility
    compatible_pairs = [
        ('Sun', 'Moon'), ('Moon', 'Sun'),
        ('Jupiter', 'Venus'), ('Venus', 'Jupiter'),
        ('Mercury', 'Venus'), ('Venus', 'Mercury'),
        ('Sun', 'Jupiter'), ('Jupiter', 'Sun')
    ]
    
    challenging_pairs = [
        ('Saturn', 'Mars'), ('Mars', 'Saturn'),
        ('Sun', 'Saturn'), ('Saturn', 'Sun'),
        ('Moon', 'Saturn'), ('Saturn', 'Moon')
    ]
    
    pair = (male_current, female_current)
    
    if pair in compatible_pairs:
        compatibility = "Excellent"
        description = f"{male_current} and {female_current} Mahadashas are highly compatible"
    elif pair in challenging_pairs:
        compatibility = "Challenging"
        description = f"{male_current} and {female_current} Mahadashas may face some challenges"
    else:
        compatibility = "Moderate"
        description = f"{male_current} and {female_current} Mahadashas are moderately compatible"
    
    return {
        "male_current_mahadasha": male_current,
        "female_current_mahadasha": female_current,
        "compatibility": compatibility,
        "description": description
    }


def _analyze_planetary_compatibility(male_chart: Dict, female_chart: Dict) -> Dict:
    """Analyze planetary positions compatibility"""
    compatibility_scores = {}
    
    # Venus compatibility (love, romance)
    male_venus_house = male_chart['planet_houses']['Venus']
    female_venus_house = female_chart['planet_houses']['Venus']
    
    venus_score = 10 if abs(male_venus_house - female_venus_house) <= 2 else \
                  7 if abs(male_venus_house - female_venus_house) <= 4 else 4
    
    compatibility_scores['venus_love'] = {
        "score": venus_score,
        "description": "Venus position compatibility for love and romance"
    }
    
    # Jupiter compatibility (growth, wisdom)
    male_jupiter_house = male_chart['planet_houses']['Jupiter']
    female_jupiter_house = female_chart['planet_houses']['Jupiter']
    
    jupiter_score = 10 if abs(male_jupiter_house - female_jupiter_house) <= 3 else 6
    
    compatibility_scores['jupiter_growth'] = {
        "score": jupiter_score,
        "description": "Jupiter compatibility for mutual growth and wisdom"
    }
    
    # Moon compatibility (emotions - already in Ashtakoot)
    # Mars compatibility (passion, energy)
    male_mars_house = male_chart['planet_houses']['Mars']
    female_mars_house = female_chart['planet_houses']['Mars']
    
    mars_score = 10 if male_mars_house not in [1, 4, 7, 8, 12] and \
                      female_mars_house not in [1, 4, 7, 8, 12] else 5
    
    compatibility_scores['mars_passion'] = {
        "score": mars_score,
        "description": "Mars compatibility for passion and physical chemistry"
    }
    
    total = sum(score['score'] for score in compatibility_scores.values())
    max_score = len(compatibility_scores) * 10
    percentage = round((total / max_score) * 100, 1)
    
    return {
        "scores": compatibility_scores,
        "total_score": total,
        "max_score": max_score,
        "percentage": percentage,
        "verdict": "Excellent" if percentage >= 80 else \
                  "Very Good" if percentage >= 65 else \
                  "Good" if percentage >= 50 else "Average"
    }


def _analyze_marriage_houses(male_chart: Dict, female_chart: Dict) -> Dict:
    """Analyze 7th house (marriage) for both"""
    
    # Male 7th house analysis
    male_7th_planets = [p for p, h in male_chart['planet_houses'].items() if h == 7]
    male_7th_sign = male_chart['houses'][7]['sign']
    
    # Female 7th house analysis
    female_7th_planets = [p for p, h in female_chart['planet_houses'].items() if h == 7]
    female_7th_sign = female_chart['houses'][7]['sign']
    
    return {
        "male_7th_house": {
            "sign": male_7th_sign,
            "planets": male_7th_planets,
            "analysis": f"Marriage house in {male_7th_sign} indicates specific partnership traits"
        },
        "female_7th_house": {
            "sign": female_7th_sign,
            "planets": female_7th_planets,
            "analysis": f"Marriage house in {female_7th_sign} indicates specific partnership traits"
        },
        "compatibility": "Strong" if len(male_7th_planets) <= 2 and len(female_7th_planets) <= 2 else "Moderate"
    }


def _analyze_children_prospects(male_chart: Dict, female_chart: Dict) -> Dict:
    """Analyze 5th house (children) for both"""
    
    male_5th_planets = [p for p, h in male_chart['planet_houses'].items() if h == 5]
    female_5th_planets = [p for p, h in female_chart['planet_houses'].items() if h == 5]
    
    # Jupiter's position (karaka for children)
    male_jupiter_house = male_chart['planet_houses']['Jupiter']
    female_jupiter_house = female_chart['planet_houses']['Jupiter']
    
    favorable_jupiter = (male_jupiter_house in [1, 5, 9] or female_jupiter_house in [1, 5, 9])
    
    prospects = "Excellent" if favorable_jupiter and \
                               'Jupiter' in male_5th_planets or 'Jupiter' in female_5th_planets else \
               "Very Good" if favorable_jupiter else \
               "Good" if len(male_5th_planets) > 0 or len(female_5th_planets) > 0 else \
               "Average"
    
    return {
        "prospects": prospects,
        "male_5th_house": {
            "planets": male_5th_planets,
            "jupiter_position": f"House {male_jupiter_house}"
        },
        "female_5th_house": {
            "planets": female_5th_planets,
            "jupiter_position": f"House {female_jupiter_house}"
        },
        "description": f"Children prospects are {prospects.lower()} based on 5th house and Jupiter positions"
    }


def _analyze_financial_compatibility(male_chart: Dict, female_chart: Dict) -> Dict:
    """Analyze 2nd and 11th houses (wealth) for both"""
    
    # 2nd house (wealth, family)
    male_2nd_planets = [p for p, h in male_chart['planet_houses'].items() if h == 2]
    female_2nd_planets = [p for p, h in female_chart['planet_houses'].items() if h == 2]
    
    # 11th house (gains, income)
    male_11th_planets = [p for p, h in male_chart['planet_houses'].items() if h == 11]
    female_11th_planets = [p for p, h in female_chart['planet_houses'].items() if h == 11]
    
    # Jupiter's influence on wealth
    male_jupiter_house = male_chart['planet_houses']['Jupiter']
    female_jupiter_house = female_chart['planet_houses']['Jupiter']
    
    wealth_houses = [2, 5, 9, 11]
    strong_jupiter = (male_jupiter_house in wealth_houses or female_jupiter_house in wealth_houses)
    
    compatibility = "Excellent" if strong_jupiter and \
                                   (len(male_11th_planets) > 0 or len(female_11th_planets) > 0) else \
                   "Very Good" if strong_jupiter else \
                   "Good" if len(male_2nd_planets) > 0 or len(female_2nd_planets) > 0 else \
                   "Average"
    
    return {
        "compatibility": compatibility,
        "male_wealth_indicators": {
            "2nd_house_planets": male_2nd_planets,
            "11th_house_planets": male_11th_planets,
            "jupiter_house": male_jupiter_house
        },
        "female_wealth_indicators": {
            "2nd_house_planets": female_2nd_planets,
            "11th_house_planets": female_11th_planets,
            "jupiter_house": female_jupiter_house
        },
        "description": f"Financial compatibility is {compatibility.lower()} based on wealth houses and Jupiter"
    }


def _analyze_health_longevity(male_chart: Dict, female_chart: Dict) -> Dict:
    """Analyze health and longevity indicators"""
    
    # 8th house (longevity)
    male_8th_planets = [p for p, h in male_chart['planet_houses'].items() if h == 8]
    female_8th_planets = [p for p, h in female_chart['planet_houses'].items() if h == 8]
    
    # Saturn's position (longevity karaka)
    male_saturn_house = male_chart['planet_houses']['Saturn']
    female_saturn_house = female_chart['planet_houses']['Saturn']
    
    favorable_saturn = (male_saturn_house in [3, 6, 10, 11] and female_saturn_house in [3, 6, 10, 11])
    
    longevity = "Excellent" if favorable_saturn and \
                              len(male_8th_planets) <= 1 and len(female_8th_planets) <= 1 else \
               "Very Good" if favorable_saturn else \
               "Good"
    
    return {
        "longevity_prospects": longevity,
        "male_indicators": {
            "8th_house_planets": male_8th_planets,
            "saturn_house": male_saturn_house
        },
        "female_indicators": {
            "8th_house_planets": female_8th_planets,
            "saturn_house": female_saturn_house
        },
        "description": f"Health and longevity prospects are {longevity.lower()}"
    }


def _calculate_overall_compatibility(ashtakoot: Dict, mangal: Dict, dasha: Dict, 
                                    planetary: Dict, marriage: Dict) -> Dict:
    """Calculate overall compatibility score"""
    
    # Ashtakoot score (50% weightage)
    guna_score = ashtakoot.get('total_score', 0)
    guna_percentage = (guna_score / 36) * 50
    
    # Mangal Dosha (15% weightage)
    mangal_score = 15 if mangal['compatible'] else 7
    
    # Dasha (10% weightage)
    dasha_score = 10 if dasha['compatibility'] == 'Excellent' else \
                 7 if dasha['compatibility'] == 'Moderate' else 4
    
    # Planetary (15% weightage)
    planetary_percentage = (planetary['percentage'] / 100) * 15
    
    # Marriage house (10% weightage)
    marriage_score = 10 if marriage['compatibility'] == 'Strong' else 6
    
    total_score = guna_percentage + mangal_score + dasha_score + planetary_percentage + marriage_score
    
    rating = "★★★★★" if total_score >= 85 else \
            "★★★★☆" if total_score >= 70 else \
            "★★★☆☆" if total_score >= 55 else \
            "★★☆☆☆" if total_score >= 40 else \
            "★☆☆☆☆"
    
    verdict = "Excellent Match - Highly Recommended" if total_score >= 85 else \
             "Very Good Match - Recommended" if total_score >= 70 else \
             "Good Match - Compatible" if total_score >= 55 else \
             "Average Match - Proceed with Caution" if total_score >= 40 else \
             "Below Average - Not Recommended"
    
    return {
        "score": round(total_score, 1),
        "percentage": round(total_score, 1),
        "rating": rating,
        "verdict": verdict
    }


def _generate_matching_recommendations(overall: Dict, ashtakoot: Dict, 
                                      mangal: Dict, male_chart: Dict, 
                                      female_chart: Dict) -> List[str]:
    """Generate detailed recommendations"""
    recommendations = []
    
    score = overall['score']
    
    if score >= 70:
        recommendations.append("This is a highly compatible match. Marriage is auspicious and recommended.")
        recommendations.append("Perform marriage ceremony during auspicious muhurta for best results.")
    elif score >= 55:
        recommendations.append("This is a good match with positive compatibility indicators.")
        recommendations.append("Some minor remedies may enhance marital harmony.")
    else:
        recommendations.append("This match shows moderate compatibility. Careful consideration advised.")
        recommendations.append("Strong remedies recommended before proceeding with marriage.")
    
    # Ashtakoot specific
    if ashtakoot.get('total_score', 0) < 18:
        recommendations.append("Guna score is below recommended 18. Consider performing Guna dosha remedies.")
    
    # Mangal Dosha specific
    if not mangal['compatible']:
        recommendations.append("Mangal Dosha mismatch detected. Perform Mangal Dosha remedies before marriage.")
        recommendations.append("Consult experienced astrologer for specific Mangal Dosha nivaran puja.")
    
    # General recommendations
    recommendations.append("Worship Lord Vishnu and Goddess Lakshmi together for marital bliss.")
    recommendations.append("Perform compatibility-enhancing rituals 40 days before marriage.")
    recommendations.append("Exchange kundlis with family priest for detailed analysis.")
    
    return recommendations


def _get_matching_remedies(overall: Dict, mangal: Dict) -> Dict:
    """Get remedies for improving compatibility"""
    remedies = {
        "general_remedies": [
            {
                "remedy": "Joint worship",
                "description": "Worship Lord Shiva and Parvati together every Monday",
                "benefit": "Enhances marital harmony and love"
            },
            {
                "remedy": "Compatibility puja",
                "description": "Perform Vivah Muhurat Shanti Puja before marriage",
                "benefit": "Removes obstacles and ensures smooth married life"
            },
            {
                "remedy": "Gemstone therapy",
                "description": "Wear compatible gemstones after consulting astrologer",
                "benefit": "Strengthens planetary positions"
            }
        ],
        "mangal_dosha_remedies": []
    }
    
    if not mangal.get('compatible', True):
        remedies["mangal_dosha_remedies"] = [
            {
                "remedy": "Mangal Dosha Nivaran Puja",
                "description": "Perform at Mangalnath Temple, Ujjain or local Mars temple",
                "benefit": "Neutralizes negative effects of Mangal Dosha"
            },
            {
                "remedy": "Hanuman worship",
                "description": "Recite Hanuman Chalisa daily and visit Hanuman temple on Tuesdays",
                "benefit": "Mars (Mangal) is appeased through Lord Hanuman"
            },
            {
                "remedy": "Red Coral gemstone",
                "description": "Wear Red Coral (Moonga) in gold ring on Tuesday after proper energization",
                "benefit": "Strengthens Mars and reduces dosha effects"
            },
            {
                "remedy": "Fasting",
                "description": "Fast on Tuesdays and donate red items to needy",
                "benefit": "Appeases Mars and reduces malefic effects"
            }
        ]
    
    return remedies
