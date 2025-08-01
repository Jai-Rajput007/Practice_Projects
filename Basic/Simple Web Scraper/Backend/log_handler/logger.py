import logging
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%d-%m-%Y_%H-%M-%S')}.log"

logs_path = os.path.join(os.getcwd(),"logs")
os.makedirs(logs_path,exist_ok=True)

Logs_file_path = os.path.join(logs_path,LOG_FILE)

logging.basicConfig(
    filename= Logs_file_path,
    format= "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s" ,
    level= logging.INFO,
)
