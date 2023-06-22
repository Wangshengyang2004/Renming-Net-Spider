import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

USER_AGENT_LIST = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.90 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
]

def get_random_user_agent():
    return random.choice(USER_AGENT_LIST)

def get_article_content(article_url):
    headers = {
        'User-Agent':  get_random_user_agent()
    }
    print(headers)
    response = requests.get(article_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Extract the article content
    # This will depend on the structure of the webpage
    article_content = soup.find('div', {'class': 'article-content'}).text

    return article_content

def extract_links(url):
    headers = {
        'User-Agent':  get_random_user_agent()
    }
    print(headers)
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    base_url = 'http://jhsjk.people.cn/'
    links = [base_url + a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('article')]

    return links

def get_article_links(page_url):
    headers = {
        'User-Agent':  get_random_user_agent()
    }
    print(headers)
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all article links on the page
    article_links = [a['href'] for a in soup.select('a') if a['href'].startswith('http://jhsjk.people.cn/article/')]

    return article_links

def generate_page_urls(base_url, num_pages):
    return [f"{base_url}?page={i}" for i in range(1, num_pages + 1)]


def extract_info(url):
    headers = {
        'User-Agent':  get_random_user_agent()
    }
    print(headers)
    response = requests.get(url, headers=headers)
    response.encoding = 'utf-8'  # Set the correct encoding
    soup = BeautifulSoup(response.text, 'html.parser')

    title = soup.find('h1').text
    content_div = soup.find('div', class_='d2txt_con clearfix')
    content_paragraphs = content_div.find_all('p')

    content = ''
    for p in content_paragraphs:
        if p.find('img') is None and '新华社记者' not in p.get_text(strip=True):  # Skip paragraphs containing images and captions
            content += p.get_text(strip=True) + '\n'

    # Remove unnecessary information
    content = content.split('责任编辑')[0]
    content = content.split('（原标题')[0]
    content = content.split('分享让更多人看到')[0]

    return title, content


base_url = "http://jhsjk.people.cn/result"
page_urls = generate_page_urls(base_url, 200)
db = []
for page_url in page_urls:
    article_links = extract_links(page_url)
    for link in article_links:
        db.append(link)
print(db)


data = []
for url in db:
    title, content = extract_info(url)
    print(title,content)
    data.append({'Title': title, 'Content': content})
    time.sleep(random.random()*3)
df = pd.DataFrame(data)
df.to_csv('data_xjp.csv', index=False)


#Will Do:  http://cpc.people.com.cn/GB/64192/105996/352007/index1.html
