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
    name: str
    style: str


@app.post("/generate-photo")
def generate_photo(request: PhotoRequest):
    return {
        "message": "Photo generation request received",
        "name": request.name,
        "style": request.style
    }