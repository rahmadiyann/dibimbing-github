import requests
import json

def extract_api(url):
    # Mengambil data dari API
    response = requests.get(url)
    response.raise_for_status()
   
    # Convert data ke json
    data = response.json()
    return data

# Panggil fungsi
url         = "https://api.spacexdata.com/v4/launches/latest"
data_spacex = extract_api(url)

with open('spacex.json', 'w') as f:
    json.dump(data_spacex, f)

print(json.dumps(data_spacex, indent=2))