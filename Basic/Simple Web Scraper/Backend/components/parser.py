from exception_handler.exception import WebscraperException
from log_handler.logger import logging
import sys
from bs4 import BeautifulSoup
from typing import List , Dict
class Parser :
    def __init__(self,html_content : str) -> None :
        self.html_content = html_content
        logging.info(f"Parser initialized ")

    def parsing (self) -> List[Dict[str,str]]:
        try:
            soup = BeautifulSoup(self.html_content,'html.parser')
            results = []
            headings = soup.find_all(['h1','h2','h3'])
            for heading in headings:
                title = heading.get_text(strip=True) if heading else "Untitled"
                content = []
                next_element = heading.find_next()
                while next_element and next_element.name not in ['h1','h2','h3'] :
                    if next_element.name == 'p':
                        content_text = next_element.get_text(strip=True)
                        if content_text:
                            content.append(content_text)
                    next_element = next_element.find_next()
                content_text = ' '.join(content) if content else ''
                if title or content_text :
                    results.append({
                        'title':title,
                        'content':content_text
                    })
            logging.info(f"Successfully parsed and extracted {len(results)} items")
            return results
        except Exception as e:
            raise WebscraperException(e,sys)
            
