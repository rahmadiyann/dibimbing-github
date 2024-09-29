import requests
import json
import csv
import pandas as pd
from flatten_dict import flatten

def fetch_data(url):
    response = requests.get(url)
    return response.json()['users']

def flatten_user_data(user):
    flat_user = flatten(user, reducer='dot')
    return {k: str(v) for k, v in flat_user.items()}

def export_to_parquet(data, filename):
    df = pd.DataFrame(data)
    df.to_parquet(filename, index=False)

def export_to_csv(data, filename):
    keys = set().union(*(d.keys() for d in data))
    with open(filename, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data)

def export_to_json(data, filename):
    with open(filename, 'a', encoding='utf-8') as jsonfile:
        json.dump(data, jsonfile, indent=2)

def main():
    url = 'https://dummyjson.com/users'
    users = fetch_data(url)
    
    flattened_users = [flatten_user_data(user) for user in users]
    
    export_to_parquet(flattened_users, 'users_data.parquet')
    export_to_csv(flattened_users, 'users_data.csv')
    export_to_json(flattened_users, 'users_data.json')
    
    print("Data has been exported to users_data.csv and users_data.json")

if __name__ == "__main__":
    for i in range(1,10):
        main()