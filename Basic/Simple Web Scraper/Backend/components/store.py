import psycopg2
import psycopg2.extras
import sys
import os
from typing import List, Dict
from exception_handler.exception import WebscraperException
from log_handler.logger import logging

class Storer:
    def __init__(self):
        self.conn = None
        try:
            logging.info("Attempting to connect database")
            self.conn = psycopg2.connect(
                dbname = os.getenv("DB_NAME"),
                user = os.getenv("DB_USER"),
                password = os.getenv("DB_PASSWORD"),
                host = os.getenv("DB_HOST","localhost"),
                port = os.getenv("DB_PORT","5432"))
            self.cursor = self.conn.cursor()
            logging.info("Database connection successful")
        except Exception as e:
            raise WebscraperException(e,sys)
    
    def setup_database_table(self):
        try:
            logging.info("Verifying existing data")
            create_table_query = """
            CREATE TABLE IF NOT EXISTS scraped_data(
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            content TEXT,
            scraped_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
            );
            """
            self.cursor.execute(create_table_query)
            self.conn.commit()
            logging.info("'Scraped_data' table is ready.")
        except Exception as e:
            self.conn.rollback()
            raise WebscraperException(e,sys)
    
    def store_data(self,data:List[Dict[str,str]]):
        if not data:
            logging.warning("No data provided to store , skipping database insertion")
            return 
        try:
            logging.info("Inserting")
            insert_query = "INSERT INTO scraped_data (title,content) VALUES %s;"
            records_to_insert = [(item['title'],item['content']) for item in data]

            psycopg2.extras.execute_values(
                self.cursor,
                insert_query,
                records_to_insert,
                template = None,
                page_size = 100
            )
            self.conn.commit()
            logging.info(f"Successfully inserted {len(records_to_insert)}")
        except Exception as e:
            self.conn.rollback()
            raise WebscraperException(e,sys)
    
    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
            logging.info("Connection closed")