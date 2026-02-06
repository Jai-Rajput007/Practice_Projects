import requests

url = 'http://api.open-notify.org/iss-now.json'
data = requests.get(url=url)
print(data)
print(data.json())