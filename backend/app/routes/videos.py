from azure.core.exceptions import ResourceNotFoundError
from fastapi import HTTPException
from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Form,
    Depends
)

from sqlalchemy.orm import Session

import os

from ..database import get_db
from ..models import Video
from ..schemas import VideoResponse
from ..blob_storage import container_client
from ..video_processor import convert_to_hls
from ..auth import get_current_user
from ..models import User
from ..models import WatchHistory
from ..schemas import WatchProgress

router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)

@router.get("")
def get_videos(
    db: Session = Depends(get_db)
):
    return db.query(Video).all()

@router.post(
    "/upload",
    response_model=VideoResponse
)
async def upload_video(
    title: str = Form(...),
    description: str = Form(""),
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    # Read uploaded file
    contents = await file.read()

    # Save MP4 locally
    os.makedirs("uploads", exist_ok=True)

    local_mp4 = f"uploads/{file.filename}"

    with open(local_mp4, "wb") as f:
        f.write(contents)

    # Convert MP4 to HLS
    hls_folder = f"hls_output/{file.filename}"

    playlist_path = convert_to_hls(
        local_mp4,
        hls_folder
    )

    # Upload generated HLS files to Azure Blob Storage
    for root, dirs, files in os.walk(hls_folder):

        for filename in files:

            filepath = os.path.join(
                root,
                filename
            )

            blob_name = (
                f"{file.filename}/{filename}"
            )

            with open(filepath, "rb") as data:

                container_client.upload_blob(
                    name=blob_name,
                    data=data,
                    overwrite=True
                )

    # Build playlist URL
    playlist_blob = (
        f"{file.filename}/index.m3u8"
    )

    hls_url = (
        f"{container_client.url}/"
        f"{playlist_blob}"
    )

    # Save metadata in database
    db_user = (
	db.query(User)
	.filter(User.email == current_user)
	.first()
    )

    video = Video(
        title=title,
        description=description,
        filename=file.filename,
        blob_url="stored_as_hls",
        hls_url=hls_url,
        uploaded_by=db_user.id
    )

    db.add(video)
    db.commit()
    db.refresh(video)

    return video

@router.get("/{video_id}")
def get_video(
	video_id: int,
	db: Session = Depends(get_db)
):
	video = (
		db.query(Video)
		.filter(Video.id == video_id)
		.first()
	)

	if not video:
		raise HTTPException(
			status_code=404,
			detail = "Video not found"
		)
	return video

@router.delete("/{video_id}")
def delete_video(
    video_id: int,
    db: Session = Depends(get_db)
):
    video = (
        db.query(Video)
        .filter(Video.id == video_id)
        .first()
    )

    if not video:
        raise HTTPException(
            status_code=404,
            detail="Video not found"
        )

    prefix = f"{video.filename}/"

    blobs = container_client.list_blobs(
        name_starts_with=prefix
    )

    for blob in blobs:
        try:
            container_client.delete_blob(blob.name)
        except ResourceNotFoundError:
            pass

    db.delete(video)
    db.commit()

    return {
        "message": "Video deleted"
    }

@router.post("/watch-progress")
def save_progress(
    data: WatchProgress,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == current_user)
        .first()
    )

    existing = (
        db.query(WatchHistory)
        .filter(
            WatchHistory.user_id == user.id,
            WatchHistory.video_id == data.video_id
        )
        .first()
    )

    if existing:

        existing.position = data.position

        db.commit()

        return {
            "message": "updated"
        }

    progress = WatchHistory(
        user_id=user.id,
        video_id=data.video_id,
        position=data.position
    )

    db.add(progress)
    db.commit()

    return {
        "message": "saved"
    }

@router.get("/continue-watching")
def continue_watching(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = (
        db.query(User)
        .filter(User.email == current_user)
        .first()
    )

    return (
        db.query(WatchHistory)
        .filter(
            WatchHistory.user_id == user.id
        )
        .all()
    )
