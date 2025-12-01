"""
Pydantic Models for API
"""
from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime


class BirthData(BaseModel):
    """Birth data model"""
    name: str = Field(..., description="Person's name")
    date: str = Field(..., description="Birth date (YYYY-MM-DD)")
    time: str = Field(..., description="Birth time (HH:MM:SS)")
    latitude: float = Field(..., description="Birth place latitude", ge=-90, le=90)
    longitude: float = Field(..., description="Birth place longitude", ge=-180, le=180)
    timezone: str = Field(default="Asia/Kolkata", description="Timezone")
    
    @field_validator('date')
    @classmethod
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%Y-%m-%d')
            return v
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
    
    @field_validator('time')
    @classmethod
    def validate_time(cls, v):
        try:
            datetime.strptime(v, '%H:%M:%S')
            return v
        except ValueError:
            raise ValueError('Time must be in HH:MM:SS format')


class ChartRequest(BaseModel):
    """Birth chart request"""
    birth_data: BirthData
    house_system: str = Field(default="PLACIDUS", description="House system")


class DivisionalChartRequest(BaseModel):
    """Divisional chart request"""
    birth_data: BirthData
    division: str = Field(..., description="Division (D1, D9, D10, etc.)")


class DashaRequest(BaseModel):
    """Dasha calculation request"""
    birth_data: BirthData
    years: int = Field(default=120, description="Years to calculate", ge=1, le=120)


class PanchangRequest(BaseModel):
    """Panchang request"""
    date: str = Field(..., description="Date (YYYY-MM-DD)")
    latitude: float = Field(..., description="Location latitude", ge=-90, le=90)
    longitude: float = Field(..., description="Location longitude", ge=-180, le=180)
    timezone: str = Field(default="Asia/Kolkata", description="Timezone")


class MatchingRequest(BaseModel):
    """Matching request"""
    male_data: BirthData
    female_data: BirthData


class KPRequest(BaseModel):
    """KP system request"""
    birth_data: BirthData


class YogasRequest(BaseModel):
    """Yogas and Doshas request"""
    birth_data: BirthData
