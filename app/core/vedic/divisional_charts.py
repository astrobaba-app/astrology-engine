"""
Divisional Charts (Varga) Calculator
"""
from typing import Dict


class DivisionalCharts:
    """Calculate all divisional charts (D1-D60)"""
    
    # Division schemes for various charts
    DIVISIONS = {
        'D1': {'name': 'Rashi', 'divisions': 1, 'matters': 'Body, overall life'},
        'D2': {'name': 'Hora', 'divisions': 2, 'matters': 'Wealth'},
        'D3': {'name': 'Drekkana', 'divisions': 3, 'matters': 'Siblings, courage'},
        'D4': {'name': 'Chaturthamsa', 'divisions': 4, 'matters': 'Fortune, property'},
        'D7': {'name': 'Saptamsa', 'divisions': 7, 'matters': 'Children, creativity'},
        'D9': {'name': 'Navamsa', 'divisions': 9, 'matters': 'Marriage, dharma'},
        'D10': {'name': 'Dasamsa', 'divisions': 10, 'matters': 'Career, profession'},
        'D12': {'name': 'Dwadasamsa', 'divisions': 12, 'matters': 'Parents'},
        'D16': {'name': 'Shodasamsa', 'divisions': 16, 'matters': 'Vehicles, luxuries'},
        'D20': {'name': 'Vimsamsa', 'divisions': 20, 'matters': 'Spiritual progress'},
        'D24': {'name': 'Chaturvimsamsa', 'divisions': 24, 'matters': 'Learning, education'},
        'D27': {'name': 'Saptavimsamsa', 'divisions': 27, 'matters': 'Strengths, weaknesses'},
        'D30': {'name': 'Trimsamsa', 'divisions': 30, 'matters': 'Evils, misfortunes'},
        'D40': {'name': 'Khavedamsa', 'divisions': 40, 'matters': 'Maternal heritage'},
        'D45': {'name': 'Akshavedamsa', 'divisions': 45, 'matters': 'Paternal heritage'},
        'D60': {'name': 'Shashtiamsa', 'divisions': 60, 'matters': 'Past life, karma'},
    }
    
    def calculate_divisional_position(
        self,
        longitude: float,
        division: int
    ) -> Dict:
        """
        Calculate divisional chart position
        
        Args:
            longitude: Planet longitude in D1 (0-360)
            division: Division number (e.g., 9 for D9)
            
        Returns:
            Divisional position with sign and degree
        """
        # Get sign (0-11) and degree within sign (0-30)
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        
        # Calculate division within the sign
        division_size = 30.0 / division
        division_num = int(degree_in_sign / division_size)
        
        # Calculate new sign based on division
        if division == 1:  # D1 (Rashi)
            new_sign = sign
            new_degree = degree_in_sign
        
        elif division == 2:  # D2 (Hora)
            # Odd signs: First 15° → same sign, Last 15° → 5th sign
            # Even signs: First 15° → 4th sign, Last 15° → same sign
            if sign % 2 == 0:  # Even sign
                new_sign = (sign + 3) % 12 if division_num == 0 else sign
            else:  # Odd sign
                new_sign = sign if division_num == 0 else (sign + 4) % 12
            new_degree = (degree_in_sign % 15) * 2
        
        elif division == 3:  # D3 (Drekkana)
            # Each 10° segment
            new_sign = (sign + (division_num * 4)) % 12
            new_degree = (degree_in_sign % 10) * 3
        
        elif division == 4:  # D4 (Chaturthamsa)
            # Each 7.5° segment
            new_sign = (sign + (division_num * 3)) % 12
            new_degree = (degree_in_sign % 7.5) * 4
        
        elif division == 7:  # D7 (Saptamsa)
            # Each 4.285714° segment
            if sign % 2 == 0:  # Even sign
                new_sign = (sign + division_num) % 12
            else:  # Odd sign
                new_sign = (sign + 6 + division_num) % 12
            new_degree = (degree_in_sign % (30/7)) * 7
        
        elif division == 9:  # D9 (Navamsa) - Most important
            # Each 3.333333° segment
            new_sign = (sign + division_num) % 12
            if sign % 2 == 1:  # Odd signs start from own sign
                pass
            else:  # Even signs have different counting
                new_sign = (new_sign + 8) % 12
            new_degree = (degree_in_sign % (30/9)) * 9
        
        elif division == 10:  # D10 (Dasamsa)
            # Each 3° segment
            if sign % 2 == 0:  # Even sign
                new_sign = (sign + division_num) % 12
            else:  # Odd sign
                new_sign = (sign + 8 + division_num) % 12
            new_degree = (degree_in_sign % 3) * 10
        
        elif division == 12:  # D12 (Dwadasamsa)
            # Each 2.5° segment
            new_sign = (sign + division_num) % 12
            new_degree = (degree_in_sign % 2.5) * 12
        
        elif division == 16:  # D16 (Shodasamsa)
            # Each 1.875° segment
            if sign in [0, 1, 2, 3, 4, 5]:  # Movable signs
                start_sign = (sign + 0) % 12
            elif sign in [6, 7, 8, 9]:  # Fixed signs
                start_sign = (sign + 4) % 12
            else:  # Dual signs
                start_sign = (sign + 8) % 12
            new_sign = (start_sign + division_num) % 12
            new_degree = (degree_in_sign % (30/16)) * 16
        
        elif division == 20:  # D20 (Vimsamsa)
            # Each 1.5° segment
            if sign % 2 == 0:  # Even sign (movable)
                new_sign = (sign + division_num) % 12
            else:  # Odd sign
                new_sign = (sign + 8 + division_num) % 12
            new_degree = (degree_in_sign % 1.5) * 20
        
        elif division == 24:  # D24 (Chaturvimsamsa)
            # Each 1.25° segment
            if sign % 2 == 0:  # Even sign
                new_sign = (sign + 3 + division_num) % 12
            else:  # Odd sign
                new_sign = (sign + division_num) % 12
            new_degree = (degree_in_sign % 1.25) * 24
        
        elif division == 27:  # D27 (Saptavimsamsa)
            # Each 1.111111° segment
            new_sign = (sign * 4 + division_num) % 12
            new_degree = (degree_in_sign % (30/27)) * 27
        
        elif division == 30:  # D30 (Trimsamsa)
            # Complex rulership scheme
            if sign % 2 == 0:  # Even signs
                rulers = [
                    (5, 4), (5, 10), (8, 7), (7, 5), (5, 6)  # Mars, Saturn, Jupiter, Mercury, Venus
                ]
            else:  # Odd signs
                rulers = [
                    (5, 4), (7, 5), (8, 7), (6, 5), (10, 5)  # Mars, Mercury, Jupiter, Venus, Saturn
                ]
            
            cumulative = 0
            for deg_range, ruler_sign in rulers:
                if degree_in_sign < cumulative + deg_range:
                    new_sign = ruler_sign
                    new_degree = ((degree_in_sign - cumulative) / deg_range) * 30
                    break
                cumulative += deg_range
            else:
                new_sign = sign
                new_degree = 0
        
        elif division == 40:  # D40 (Khavedamsa)
            # Each 0.75° segment
            new_sign = (sign + division_num) % 12
            new_degree = (degree_in_sign % 0.75) * 40
        
        elif division == 45:  # D45 (Akshavedamsa)
            # Each 0.666667° segment
            new_sign = (sign + division_num) % 12
            new_degree = (degree_in_sign % (30/45)) * 45
        
        elif division == 60:  # D60 (Shashtiamsa)
            # Each 0.5° segment
            new_sign = (sign + division_num) % 12
            new_degree = (degree_in_sign % 0.5) * 60
        
        else:
            # Generic calculation for other divisions
            new_sign = (sign + division_num) % 12
            new_degree = (degree_in_sign % division_size) * division
        
        # Normalize degree
        new_degree = new_degree % 30
        
        # Get sign name
        signs = [
            'Aries', 'Taurus', 'Gemini', 'Cancer',
            'Leo', 'Virgo', 'Libra', 'Scorpio',
            'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
        ]
        
        # Calculate new longitude
        new_longitude = new_sign * 30 + new_degree
        
        return {
            'sign': signs[new_sign],
            'sign_num': new_sign,
            'degree': round(new_degree, 6),
            'longitude': round(new_longitude, 6)
        }
    
    def calculate_chart(
        self,
        planets: Dict,
        division: str = 'D9'
    ) -> Dict:
        """
        Calculate complete divisional chart for all planets
        
        Args:
            planets: Dictionary of planet positions from D1
            division: Division code (D1, D9, etc.)
            
        Returns:
            Complete divisional chart
        """
        if division not in self.DIVISIONS:
            raise ValueError(f"Unknown division: {division}")
        
        div_info = self.DIVISIONS[division]
        div_num = div_info['divisions']
        
        divisional_planets = {}
        
        for planet_name, planet_data in planets.items():
            longitude = planet_data['longitude']
            div_position = self.calculate_divisional_position(longitude, div_num)
            
            divisional_planets[planet_name] = {
                'original_longitude': longitude,
                **div_position
            }
        
        return {
            'division': division,
            'name': div_info['name'],
            'matters': div_info['matters'],
            'planets': divisional_planets
        }
    
    def calculate_all_charts(self, planets: Dict) -> Dict[str, Dict]:
        """Calculate all major divisional charts"""
        major_divisions = ['D1', 'D2', 'D3', 'D4', 'D7', 'D9', 'D10', 
                          'D12', 'D16', 'D20', 'D24', 'D27', 'D30', 
                          'D40', 'D45', 'D60']
        
        all_charts = {}
        for division in major_divisions:
            all_charts[division] = self.calculate_chart(planets, division)
        
        return all_charts


# Global instance
divisional_charts = DivisionalCharts()
