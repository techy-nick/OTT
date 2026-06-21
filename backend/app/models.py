from sqlalchemy import Column, Integer, String
from .database import Base
from sqlalchemy import DateTime
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    hashed_password = Column(
        String,
        nullable=False
    )
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String, nullable=False)

    description = Column(String)

    filename = Column(String, nullable=False)

    blob_url = Column(String, nullable=False)

    hls_url = Column(String)

    uploaded_by = Column(
        Integer,
        ForeignKey("users.id")
    )

class WatchHistory(Base):
    __tablename__ = "watch_history"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    video_id = Column(
        Integer,
        ForeignKey("videos.id")
    )

    position = Column(Integer)

    updated_at = Column(
        DateTime,
        default=datetime.utcnow
    )
