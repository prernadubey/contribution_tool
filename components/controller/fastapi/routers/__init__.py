from fastapi import APIRouter
from starlette.responses import JSONResponse

from components.controller.fastapi.routers.v1 import v1_router

home_router = APIRouter()
home_router.include_router(v1_router)


@home_router.get("/", response_model=str, tags=["Home"])
async def home():
    """Hello World! endpoint"""

    return JSONResponse(
        "Welcome to RD Compensation Tool backend service.", status_code=200
    )
