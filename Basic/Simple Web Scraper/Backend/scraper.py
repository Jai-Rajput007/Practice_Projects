from components.fetcher import Fetcher
from log_handler.logger import logging
from exception_handler.exception import WebscraperException
import sys
from components.parser import Parser
from components.store  import Storer
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def validate_url(url:str) -> str:
    if not url.startswith(('http://','https://')):
        logging.error(f"Invalid url -> {url}")
        raise WebscraperException("Invalid url",sys)
    return url

def parse_arguments() -> str:
    parser  = argparse.ArgumentParser(
        description="WEB scraper"
    )
    parser.add_argument(
        '--url',
        type = str,
        required=True,
        help="Target URL to scrape (e.g., http://books.toscrape.com/)"

    )
    args = parser.parse_args()
    return validate_url(args.url)

def main(url:str)-> None:
    storer = None
    try:
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
        else :
            logging.warning("Parser returned no data to store")
        logging.info("Scraped Successfully")
    except WebscraperException as e:
        logging.error("Error occured")
        sys.exit(1)
    finally:
        if storer:
            storer.close_connection()

if __name__ == "__main__":
    try:
        target_url = parse_arguments()
        main(target_url)
    except WebscraperException as e:
        logging.error("Failed to scrape")
        sys.exit(1)
    

