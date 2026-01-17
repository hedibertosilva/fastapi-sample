from fastapi import APIRouter
from fastapi_versionizer import api_version

routes = APIRouter(
    prefix="/volumes",
    tags=["volumes"],
)

@routes.get("")
@api_version(0)
async def list_volumes():
    return {"volumes": [
        {
            "id": 1,
            "name": "volume 1",
        },
        {
            "id": 2,
            "name": "volume 2",
        }
    ]}

