#!/usr/bin/env python3

import os
import requests
from fastapi_utils.tasks import repeat_every

from fastapi import FastAPI
from fastapi_sqlalchemy import DBSessionMiddleware
from fastapi_sqlalchemy import db

from videos import Videos, VideoItem

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


@app.get("/")
async def root():
    """Just for testing."""
    return {"message": "Hello World"}


@app.get("/videos")
async def get_videos(name: str = "") -> dict[str, int | str | Videos]:
    """Get videos from fixed URL endpoint.
    If URL is not accessible, return videos from database.

    Returns:
        {'count': int, 'videos': Videos, 'source': str}
    """
    try:
        response = requests.get(URL)
        data = response.json()
    except requests.exceptions.ConnectionError:
        print("[ DEBUG ] URL is not accessible.")
        data = None

    if not data:
        # Get videos from database
        with db():
            videos = db.session.query(ModelVideo).all()
            videos = [SchemaVideo.from_orm(video).data for video in videos]
            source = "database"
    else:
        # Get videos from URL
        videos = response.json()
        source = "URL"

    # Filter videos by name
    if name:
        videos = [video for video in videos if name.lower() in video["name"].lower()]

    return {"count": len(videos), "videos": videos, "source": source}


@app.post("/video/", response_model=SchemaVideo)
def create_user(user: SchemaVideo) -> SchemaVideo:
    """Create a new video entry."""
    _video = ModelVideo(data=user.data)
    db.session.add(_video)
    db.session.commit()
    return _video


@app.on_event("startup")
@repeat_every(seconds=60 * 60)  # 1 hour
async def save_videos_periodically():
    """Save videos (JSON response from remote API) to database periodically."""
    print("[ DEBUG ] Saving videos to database...")
    data = await get_videos()
    videos = data["videos"]
    assert isinstance(videos, list)
    save_videos(videos)


def save_videos(videos: list[VideoItem]) -> None:
    """Save videos to database."""
    with db():
        db.session.query(ModelVideo).delete()
        db.session.execute("ALTER SEQUENCE videos_id_seq RESTART WITH 1")
        for video in videos:
            _video = ModelVideo(data=video)
            db.session.add(_video)
        db.session.commit()
