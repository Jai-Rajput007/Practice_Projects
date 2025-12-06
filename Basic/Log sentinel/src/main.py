import re
import csv
from collections import Counter
import argparse




parser = argparse.ArgumentParser(description='Find IPs causing a specific error code',prog="Tool")
parser.add_argument("--status",nargs="?",default='404')
parser.add_argument("--top",type=int,default=0)
args = parser.parse_args()

target_status = args.status
show_top = args.top


INPUT_FILE = 'server.log'
OUTPUT_FILE = f'output/{target_status}_errors_report.csv'

errors_by_ip ={}

full_data = []

log_pattern = re.compile(r'(\d+\.\d+\.\d+\.\d+)\s+-\s+-\s+\[(.*?)\].*?\s+(\d{3})\s')

print(f"Reading....{INPUT_FILE} for status {target_status}...")


with open(INPUT_FILE,'r') as f:
    for line in f:
        match = log_pattern.search(line)

        if match:
            ip = match.group(1)
            timestamp = match.group(2)
            status = match.group(3)

            if status == target_status:
                print(f"{ip} {timestamp}")
                full_data.append({
                    'IP':ip,
                    'Timestamp':timestamp,
                    'Status':status,
                    'Full log line':line.rstrip()
                })

print(f"\nFound {len(full_data)} matches -> saving full details to {OUTPUT_FILE}")
with open(OUTPUT_FILE,'w',newline='',encoding='utf-8') as csvfile:
    fieldnames = ['IP','Timestamp','Status','Full log line']
    writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(full_data)

print("Done !!")

                    



                