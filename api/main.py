#!/usr/bin/env python3

import os
import requests

from fastapi import FastAPI
from dotenv import load_dotenv

from models.videos import Videos

load_dotenv()

# CONSTANTS
URL = os.getenv("URL", "")

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/videos")
async def get_videos(name: str = "") -> dict[str, int | Videos]:
    """Get videos from fixed URL endpoint.

    Returns:
        {'count': int, 'videos': Videos}
    """
    response = requests.get(URL)
    videos =  response.json()

    if name:
        videos = [video for video in videos if name.lower() in video["name"].lower()]

    count = len(videos)

    return {"count": count, "videos": videos}
