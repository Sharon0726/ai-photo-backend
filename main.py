from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

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
    file: UploadFile = File(...),
    style: str = Form("photo_booth"),
    prompt: str = Form("")
):
    return {
        "message": "Photo upload received",
        "filename": file.filename,
        "content_type": file.content_type,
        "style": style,
        "prompt": prompt,
        "status": "upload_success"
    }