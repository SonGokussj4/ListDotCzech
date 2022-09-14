#!/usr/bin/env python3

import os
import requests
from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db

from videos import Videos

from models import Video as ModelVideo
from schema import Video as SchemaVideo

from dotenv import load_dotenv
load_dotenv()

# CONSTANTS
URL = os.getenv("URL", "")
DATABASE_URL = os.getenv("DATABASE_URL", "")

# API
app = FastAPI()
app.add_middleware(DBSessionMiddleware, db_url=DATABASE_URL)
# Base = declarative_base()


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


@app.post("/video/", response_model=SchemaVideo)
def create_user(user: SchemaVideo) -> SchemaVideo:
    _video = ModelVideo(data=user.data)
    db.session.add(_video)
    db.session.commit()
    return _video
