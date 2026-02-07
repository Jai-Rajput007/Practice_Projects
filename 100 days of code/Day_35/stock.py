
## Here we have to fetch stock price of stock, and price change of it , if price change is more that 10 percent we will later fetch the news of why it happened
from fastapi import FastAPI,Query,HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field,field_validator
from typing import List,Dict,Any,Optional,Literal
from datetime import date
import httpx
load_dotenv()

stock_api_key = os.getenv("ALPHA_API_KEY")

app =  FastAPI(
    title="News Alert app"
)
## CORS setup
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    )


class Stock_response(BaseModel):
    symbol: str             = Field(..., alias="01. symbol")
    open_price: float       = Field(..., alias="02. open")
    high: float             = Field(..., alias="03. high")
    low: float              = Field(..., alias="04. low")
    price: float            = Field(..., alias="05. price")
    volume: int             = Field(..., alias="06. volume")
    latest_trading_day: date = Field(..., alias="07. latest trading day")
    previous_close: float   = Field(..., alias="08. previous close")
    change: float           = Field(..., alias="09. change")
    change_percent: str     = Field(..., alias="10. change percent")

    class Config:
        populate_by_name = True
    
    @property
    def change_percent_float(self)->float:
        return float(self.change_percent.rstrip("% "))

class AlphaVantageResponse(BaseModel):
    quote: Stock_response = Field(alias="Global Quote")

@app.get("/stock/{symbol}",response_model=Stock_response,response_model_by_alias=False)
async def get_stock_quote(symbol:str):
    url = "https://www.alphavantage.co/query"
    api_symbol = f"{symbol.upper()}.BSE"
    params ={
        "function" : "GLOBAL_QUOTE",
        "symbol":api_symbol,
        "apikey":stock_api_key
    }
    async with httpx.AsyncClient(timeout=15.0) as client:
        try:
            response = await client.get(url,params=params)
            response.raise_for_status()
            data = response.json()

            if "Error Message" in data:
                raise HTTPException(404, detail=f"Invalid symbol or API error: {data['Error Message']}")
            
            if "Information" in data or "Note" in data:
                raise HTTPException(429, detail=f"API limit or note: {data.get('Information') or data.get('Note')}")
            
            if "Global Quote" not in data or not data["Global Quote"]:
                raise HTTPException(status_code=404,detail="Stock not found")
            
            parsed_data = AlphaVantageResponse.model_validate(data)
            return parsed_data.quote
        
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=500, detail=f"External API Error: {e}")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

