# these should be the only imports you need

import requests
from bs4 import BeautifulSoup

# write your code here
# usage should be python3 part3.py

url = "https://www.michigandaily.com"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, 'html.parser')

most_reads = []

for div in soup.find_all('div', class_ = 'view-most-read'):
    for ol in div.find_all('ol'):
        for li in ol.find_all('li'):
            title = li.text
            article_data = requests.get(url+li.a['href']).text
            article_soup = BeautifulSoup(article_data, 'html.parser')
            for byline in article_soup.find_all('div', class_='byline'):
                for link in byline.find_all('div', class_='link'):
                    first_author = link.text.replace('and',',').split(',')[0].strip()
                    most_reads.append( (title, first_author) )

print('Michigan Daily -- MOST READ')
for title, author in most_reads:
    print(title)
    print('  by {}'.format(author))
