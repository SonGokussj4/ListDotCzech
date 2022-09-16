#!/usr/bin/env python3

import os
import re
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
    # URL = "https://noffirgoku.gi"
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

@app.get("/getFilterItems")
async def get_filter_items(name: str = "") -> dict[str, list[str]]:
    """Get all filter items. (only from DB, so not real time data)"""
    print("GETTING VIDEOS")
    print("NAME: ", name)
    res = await get_videos(name)
    videos: Videos = res.get("videos", {"count": 0, "videos": []})

    # print(f'videos: {videos}')

    # with db():
    #     videos = db.session.query(ModelVideo).all()
    #     videos = [SchemaVideo.from_orm(video).data for video in videos]

    # Extract filter items by "key" name from Videos
    filter_items: dict[str, list[str]] = {
        "name": [],
        "disabled": [],
        "features": []
    }
    for video in videos:
        for key, value in video.items():
            if key in filter_items:
                if value not in filter_items[key]:
                    filter_items[key].append(value)

    # Filter titles to get only the first part until "(, w/, ," starts
    filter_items["name"] = list({re.split(r"[(]|w/|,", name)[0].strip() for name in filter_items["name"]})

    # Filter unique features
    filter_items["features"] = list({item for sublist in filter_items["features"] for item in sublist})

    return filter_items

@app.on_event("startup")
@repeat_every(seconds=60 * 60)  # 1 hour
async def save_videos_periodically():
    """Save videos (JSON response from remote API) to database periodically."""
    print("[ DEBUG ] Saving videos to database...")
    data = await get_videos()
    videos = data["videos"]
    assert isinstance(videos, list)
    save_videos(videos)
    print("[ DEBUG ] Saving videos to database... DONE")


def save_videos(videos: list[VideoItem]) -> None:
    """Save videos to database."""
    with db():
        db.session.query(ModelVideo).delete()
        db.session.execute("ALTER SEQUENCE videos_id_seq RESTART WITH 1")
        for video in videos:
            _video = ModelVideo(data=video)
            db.session.add(_video)
        db.session.commit()
