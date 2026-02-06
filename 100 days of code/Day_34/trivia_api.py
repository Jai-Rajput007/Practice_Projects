from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware # <--- IMPORT THIS
from pydantic import BaseModel
import httpx
from typing import List, Optional, Dict, Any
import random

app = FastAPI(
    title="Trivia API Proxy",
    description="Fetches questions from Open Trivia Database (opentdb.com)",
    version="1.0.0"
)

# <--- ADD THIS SECTION
origins = [
    "http://localhost:3000",  # Allow Next.js
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# ---> END ADD SECTION

class TriviaQuestion(BaseModel):
    category: str
    type: str 
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]

class TriviaResponse(BaseModel):
    response_code: int
    results: List[TriviaQuestion]

@app.get("/trivia", response_model=TriviaResponse)
async def get_trivia_questions(
    amount: int = Query(10, ge=1, le=50),
    category: Optional[int] = Query(None, ge=9, le=32),
    difficulty: Optional[str] = Query(None, pattern="^(easy|medium|hard)$"),
    type: Optional[str] = Query(None, pattern="^(multiple|boolean)$"),
    token: Optional[str] = Query(None)
):
    # ... (Your existing logic here remains exactly the same) ...
    base_url = "https://opentdb.com/api.php"
    params: Dict[str, Any] = {"amount": amount}

    if category is not None: params["category"] = category
    if difficulty is not None: params["difficulty"] = difficulty.lower()
    if type is not None: params["type"] = type
    if token is not None: params["token"] = token

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params, timeout=10.0)
            response.raise_for_status()
            data = response.json()
        except Exception as e:
            raise HTTPException(status_code=503, detail=str(e))

    if data.get("response_code") != 0:
        raise HTTPException(status_code=400, detail="API Error")

    return data