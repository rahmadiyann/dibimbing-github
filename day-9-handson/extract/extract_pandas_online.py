import pandas as pd

pd.options.display.max_columns = None

def extract_json_from_online_with_pandas(url):
    # Mengambil data dari URL
    df = pd.read_json(url)
    return df

# Panggil fungsi
url      = "https://jsonplaceholder.typicode.com/posts"
df_posts = extract_json_from_online_with_pandas(url)

with open ('pandas_online_posts.json', 'w') as f:
    f.write(df_posts.to_json())

print(df_posts)