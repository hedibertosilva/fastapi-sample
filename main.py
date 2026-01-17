from fastapi import FastAPI
from fastapi_versionizer import Versionizer

from sample.routes import router

app = FastAPI()

def versionize(app: FastAPI):
    Versionizer(
        app=app,
        prefix_format="/v{major}",
        default_version=(0,0),
        include_main_docs=True,
        sort_routes=True,
        semantic_version_format='{major}'
    ).versionize()

app.include_router(router)
versionize(app)

# python -m uvicorn main:app --reload
