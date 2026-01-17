from fastapi import APIRouter

from sample.volumes.v0_volumes import routes as v0_volume
from sample.volumes.v1_volumes import routes as v1_volume

api_router = APIRouter()
api_router.include_router(v0_volume)
api_router.include_router(v1_volume)
