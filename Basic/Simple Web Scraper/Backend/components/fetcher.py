import requests
import sys

from log_handler.logger import logging
from exception_handler.exception import WebscraperException


class Fetcher :
    def __init__(self,url:str):
        self.url = url
        self.headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"}
        logging.info(f"Fetcher initialized for {self.url}")

    def fetch_content(self) -> str :
        try:
            logging.info(f"Sending GET request to {self.url}")
            response = requests.get(self.url,headers=self.headers,timeout=10)
            response.raise_for_status
            logging.info(f"Sucessful response from {self.url} with status code {response.status_code}")
            return response.text
            
        except requests.RequestException as e:
            raise WebscraperException(e,sys)
        
       

    