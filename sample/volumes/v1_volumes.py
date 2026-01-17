from fastapi import APIRouter
from fastapi import Depends
from typing import Annotated
from fastapi_versionizer import api_version

from sample.volumes.models.volumes import VolumeModel
from sample.volumes.services.volume_service import VolumeService

routes = APIRouter(
    prefix="/volumes",
    tags=["volumes"],
)

@routes.get("", response_model=list[VolumeModel])
@api_version(1)
async def list_volumes(
        volume_service: Annotated[VolumeService, Depends()],
):
    return await volume_service.list_volumes()

# Ignore GET method, just testing session.add
@routes.get("/create")
@api_version(1)
async def create(
        volume_service: Annotated[VolumeService, Depends()],
):
    return await volume_service.create_volumes()


@routes.get("/expand")
@api_version(1)
async def expand_volumes(
        volume_service: Annotated[VolumeService, Depends()],
):
    return await volume_service.expand_volumes()
