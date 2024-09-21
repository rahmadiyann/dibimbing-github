import requests
from bs4 import BeautifulSoup

def extract_web(url):
    # Mengambil konten halaman web
    response = requests.get(url)
    soup     = BeautifulSoup(response.content, "html.parser")

    # Contoh pengambilan data: Mengambil semua teks dari tag <h2>
    data = [h2.get_text() for h2 in soup.find_all("h2")]
    return data

# Panggil fungsi
url       = "https://www.bbc.com/news"
data_news = extract_web(url)
with open('news.txt', 'w') as f:
    for news in data_news:
        f.write(news + "\n")
        
print(data_news)