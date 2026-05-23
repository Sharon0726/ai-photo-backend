from fastapi import FastAPI
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