from fastapi import FastAPI, HTTPException
from components.fetcher import Fetcher
from components.parser import Parser
from components.store  import Storer
from log_handler.logger import logging
from exception_handler.exception import WebscraperException
import sys
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],

)
class  ScrapeRequest(BaseModel):
    url:str

def validate_url(url:str) -> str:
    if not url.startswith(('http://','https://')):
        logging.error(f"Invalid url -> {url}")
        raise WebscraperException("Invalid url",sys)
    return url

@app.post("/scrape")
async def scrape_url(request:ScrapeRequest):
    try:
        logging.info(f"Scrape request for url :{request.url}")
        url = validate_url(request.url)

        #Setup
        logging.info('Scraping Started')
        storer = Storer()
        storer.setup_database_table()
        #Fetching
        fetcher_instance =  Fetcher(url =url)
        html_content = fetcher_instance.fetch_content()
        logging.info("Successfully fetched")

        #Parser
        parser_instance = Parser(html_content)
        parsed_data = parser_instance.parsing()
        logging.info("Parsed successfully")

        #Store
        if parsed_data:
            storer.store_data(data=parsed_data)
            logging.info(f"Stored {len(parsed_data)} items")
        else :
            logging.warning("Parser returned no data to store")
        return {"message":"Scraping successful","items_scraped":len(parsed_data)}
    except WebscraperException as e:
        logging.error("Error occured")
        raise HTTPException(status_code=400,detail=str(e))
    except Exception as e:
        logging.error(f"Unexpected Error")
        raise HTTPException(status_code=500,detail="Internal Server error")
    finally:
        if storer:
            storer.close_connection()


    

