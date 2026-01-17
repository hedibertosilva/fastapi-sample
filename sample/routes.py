from fastapi import APIRouter

from sample.volumesRouter import api_router as volumes_router


router = APIRouter()
router.include_router(volumes_router)
