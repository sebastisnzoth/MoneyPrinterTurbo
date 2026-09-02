"""Application configuration - root APIRouter

Defines all FastAPI application endpoints.

Resources:
    1. https://fastapi.tiangolo.com/tutorial/bigger-applications

"""

from fastapi import APIRouter

from app.controllers import music_video, ping
from app.controllers.v1 import llm, video

root_api_router = APIRouter()
root_api_router.include_router(ping.router)
root_api_router.include_router(music_video.router)

# v1
root_api_router.include_router(video.router)
root_api_router.include_router(llm.router)
