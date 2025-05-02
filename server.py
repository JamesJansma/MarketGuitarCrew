# server.py
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List
from src.guitarmarket.crew import Guitarmarket

app = FastAPI()

from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or replace with your frontend domain like ["https://your-site.netlify.app"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

class RunCrewInput(BaseModel):
    email: str

@app.get("/api/hello")
def hello():
    return {"message": "Hello from James's Guitar Market!"}


@app.post("/api/runcrew")
def run_full_pipeline(input_data: RunCrewInput):
    try:
        result = Guitarmarket().crew().kickoff(inputs={
            "topic": "Guitar",
            "email": input_data.email
            })
        return result.raw
    except Exception as e:
        raise HTTPException(500, f"Pipeline failed: {e}")
