from fastapi import FastAPI, UploadFile, File, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import shutil
import uuid

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 開發階段先全部允許
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Hello FastAPI"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/hello")
def say_hello(name: str):
    return {"message": f"Hello, {name}"}


class PhotoRequest(BaseModel):
    style: str
    prompt: str
    celebrity_name: str | None = None


@app.post("/generate-photo")
def generate_photo(request: PhotoRequest):
    return {
        "message": "AI photo generation request received",
        "style": request.style,
        "prompt": request.prompt,
        "celebrity_name": request.celebrity_name,
        "status": "mock_success"
    }

@app.post("/upload-photo")
async def upload_photo(
    request: Request,
    file: UploadFile = File(...),
    style: str = Form("photo_booth"),
    prompt: str = Form("")
):
    ext = os.path.splitext(file.filename)[1]
    saved_filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(UPLOAD_DIR, saved_filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    file_url = f"{request.base_url}uploads/{saved_filename}"

    return {
        "message": "Photo upload received",
        "filename": file.filename,
        "saved_filename": saved_filename,
        "content_type": file.content_type,
        "file_url": file_url,
        "style": style,
        "prompt": prompt,
        "status": "upload_success"
    }