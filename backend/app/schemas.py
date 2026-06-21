from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    email: str

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class VideoResponse(BaseModel):
    id: int
    title: str
    description: str | None
    blob_url: str

    hls_url: str | None

    class Config:
        from_attributes = True

class WatchProgress(BaseModel):
    video_id: int
    position: int
