# server.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from src.guitarmarket.crew import Guitarmarket

app = FastAPI()

@app.get("/api/hello")
def hello():
    return {"message": "Hello from James's Guitar Market!"}


@app.post("/api/runcrew")
def run_full_pipeline():
    try:
        result = Guitarmarket().crew().kickoff(inputs={"topic": "Guitar"})
        return result.raw
    except Exception as e:
        raise HTTPException(500, f"Pipeline failed: {e}")