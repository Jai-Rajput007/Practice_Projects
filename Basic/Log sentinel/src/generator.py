import random 
from datetime import datetime, timedelta
import pathlib
from resource import paths,path_weights,user_agents,us_weights

fake_ips = []
http_methods =[]
status_codes =[]
response_size=[]
fake_paths = []

Total_lines = 85000




with open("server.log","w") as f:
    for i in range(Total_lines):
        start_date = datetime(2025,11,1)
        random_seconds = random.randint(0,25*24*60*60)
        timestamp = start_date + timedelta(seconds= random_seconds)
        timestamp_str = timestamp.strftime("%d/%b/%Y:%H:%M:%S +0000")

        methods = ['GET','POST','PUT','DELETE']
        weightis = [70,20,8,2]
        method = random.choices(methods,weights=weightis,k=1)[0]

        statuses = [200,301,302,404,500]
        weights = [70,5,7,15,3]
        status = random.choices(statuses,weights=weights,k=1)[0]

        ip = f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"

        r_size = max(100,min(500000,int(random.gauss(8000,15000))))

        path = random.choices(paths,weights=path_weights)[0]

        user_agent = random.choices(user_agents,weights=us_weights)[0]

        line = f"{ip} - - [{timestamp_str}] \"{method} {path} HTTP/1.1\" {status} {r_size} \"{user_agent}\""

        f.write(line+"\n")
        
