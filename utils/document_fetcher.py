import requests
from bs4 import BeautifulSoup

def fetch_documentation(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def parse_documentation(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    return soup.get_text()