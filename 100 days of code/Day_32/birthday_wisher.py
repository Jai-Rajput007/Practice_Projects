import smtplib
import datetime as dt
import random
import pandas as pd
import os


def excel_data_processor(filepath,row:int)->list[str]:
    df = pd.read_excel(filepath)           
    row_data = df.iloc[row].tolist()       
    name, birthday_str, mail = row_data[:3]
    now = dt.datetime.now()
    day, month = map(int, birthday_str.split("-")) 
    parsed_bday = str(dt.datetime(now.year, month, day))
    return [name, parsed_bday, mail]   


def birthday_checker(filepath)->int:
    data = pd.read_excel(filepath) 
    Birthday_persons = []
    now = dt.datetime.now()
    for i in range(len(data)):
        name,date,mail = excel_data_processor(filepath,row=i)
        if now <= pd.to_datetime(date):
            Birthday_persons.append(i)
    return Birthday_persons

def mail_selecter_creator(folderpath):
    all_items = os.listdir(folderpath)
    files_only = [f for f in all_items if os.path.isfile(os.path.join(folderpath,f))]
    if not files_only:
        print("No files found in the folder!")
    else:
        random_file = random.choice(files_only)
        print(f"Random file: {random_file}")
    placeholder = "[name]"
    my_name_placeholder = "[Your name]"

    birthday_persons = birthday_checker("birthday.xlsx")
    name_mail_dict = {}
    for i in range(len(birthday_persons)):
        name,date,mail = excel_data_processor(filepath="birthday.xlsx",row=birthday_persons[i])
        name_mail_dict[name] = mail

    if not os.path.exists("sent mails"):
        os.makedirs("sent mails")
    

    try:
        with open(random_file,'r') as f:
            content = f.read()
    except FileNotFoundError:
        print(f"Error: File '{random_file}' not found.")
        exit(1)
    
    for recipient,email in name_mail_dict.items():

        new_content  = content.replace("[name]",recipient)
        new_content = content.replace("[Your name]","Jai Singh Rajput")
        safe_name = recipient.replace(" ", "_").replace(".", "").replace(",", "")
        output_filename = f"Birthday_{safe_name}.txt"
        output_path = os.path.join("sent mails", output_filename)
        return output_filename,email
