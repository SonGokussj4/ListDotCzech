from sqlalchemy import Column, Integer, JSON

from database import Base


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    data = Column(JSON)
