from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
import httpx
from typing import List, Optional, Dict, Any

app = FastAPI(
    title="Trivia API Proxy",
    description="Fetches questions from Open Trivia Database (opentdb.com)",
    version="1.0.0"
)

# Response model (helps with automatic docs + validation)
class TriviaQuestion(BaseModel):
    category: str
    type: str  # "multiple" or "boolean"
    difficulty: str
    question: str
    correct_answer: str
    incorrect_answers: List[str]

class TriviaResponse(BaseModel):
    response_code: int
    results: List[TriviaQuestion]


@app.get("/trivia", response_model=TriviaResponse)
async def get_trivia_questions(
    amount: int = Query(10, ge=1, le=50, description="Number of questions (1–50)"),
    category: Optional[int] = Query(None, ge=9, le=32, description="Category ID (9–32)"),
    difficulty: Optional[str] = Query(None, pattern="^(easy|medium|hard)$", description="easy | medium | hard"),
    type: Optional[str] = Query(None, pattern="^(multiple|boolean)$", description="multiple | boolean"),
    token: Optional[str] = Query(None, description="Session token to avoid repeated questions")
):
    """
    Fetch trivia questions from Open Trivia DB API.
    
    - All parameters are optional except amount (defaults to 10)
    - Visit https://opentdb.com/api_config.php to generate your URL / see category IDs
    """
    base_url = "https://opentdb.com/api.php"

    params: Dict[str, Any] = {"amount": amount}

    if category is not None:
        params["category"] = category
    if difficulty is not None:
        params["difficulty"] = difficulty.lower()
    if type is not None:
        params["type"] = type
    if token is not None:
        params["token"] = token

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(base_url, params=params, timeout=10.0)
            response.raise_for_status()  # raise exception for 4xx/5xx
            data = response.json()
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=e.response.status_code, detail="Error from Trivia API")
        except httpx.RequestError as e:
            raise HTTPException(status_code=503, detail=f"Network error: {str(e)}")

    # OpenTDB returns response_code: 0 = success, 1 = no results, etc.
    if data.get("response_code") != 0:
        error_messages = {
            1: "No Results – could not find questions matching your criteria",
            2: "Invalid parameter – contains an invalid parameter",
            3: "Token Not Found – session token does not exist",
            4: "Token Empty – all questions for this token have been returned"
        }
        msg = error_messages.get(data["response_code"], "Unknown error from Trivia API")
        raise HTTPException(status_code=400, detail=msg)

    return data

