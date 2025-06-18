# Entry point of FastAPI app


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import router

app = FastAPI(
    title="Meet Summary AI",
    description="Transcribe and summarize meetings using Whisper + GPT",
    version="1.0.0"
)

# Allow all CORS origins (you can restrict later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes from routes.py
app.include_router(router)
