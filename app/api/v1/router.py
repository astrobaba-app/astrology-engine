"""
API Router
"""
from fastapi import APIRouter
from app.api.v1.endpoints import chart, dasha, panchang, divisional, kp, matching, yogas, horoscope, daily_horoscope

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(chart.router, prefix="/chart", tags=["Chart"])
api_router.include_router(dasha.router, prefix="/dasha", tags=["Dasha"])
api_router.include_router(panchang.router, prefix="/panchang", tags=["Panchang"])
api_router.include_router(divisional.router, prefix="/divisional", tags=["Divisional Charts"])
api_router.include_router(kp.router, prefix="/kp", tags=["KP System"])
api_router.include_router(matching.router, prefix="/matching", tags=["Matching"])
api_router.include_router(yogas.router, prefix="/yogas", tags=["Yogas & Doshas"])
api_router.include_router(horoscope.router, prefix="/horoscope", tags=["Horoscope & Ashtakavarga"])
api_router.include_router(daily_horoscope.router, prefix="/horoscope", tags=["Daily/Weekly/Monthly/Yearly Horoscope"])
