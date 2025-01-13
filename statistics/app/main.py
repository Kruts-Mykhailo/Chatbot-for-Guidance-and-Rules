from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from app.routes import router
from dotenv import load_dotenv
import os

load_dotenv()

GAMEPLATFORM_URL = os.getenv("GAMEPLATFORM_URL")

if not GAMEPLATFORM_URL:
    raise ValueError("GAMEPLATFORM_URL environment variable is not set or empty.")

app = FastAPI()

app.include_router(router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[GAMEPLATFORM_URL],  
    allow_credentials=True,
    allow_methods=["POST"], 
    allow_headers=["*"],  
)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9090)
