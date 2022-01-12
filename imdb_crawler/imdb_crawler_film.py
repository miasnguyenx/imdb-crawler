from typing import Container
from bs4 import BeautifulSoup
import requests
import regex as re
import pandas as pd

movie_ids = list()
genres = list()
for i in range(0, 10000, 250):
    url = "https://www.imdb.com/search/title/?moviemeter=" + \
        str(1+i)+","+str(251+i)+"&count=250"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    containers = soup.find_all('div', class_="lister-item-content")
    
    print("Num of containers: ", len(containers))
    for container in containers:
        movie_id = container.find('h3', class_="lister-item-header")
        movie_id = movie_id.find('a')
        movie_name = movie_id
        movie_id = movie_id['href']
        movie_id = re.findall('[0-9]+', movie_id)
        movie_id = "tt" + str(movie_id[0])
        try:
            genre = container.find('p', class_="text-muted")
            genre = genre.find('span', class_="genre")
            genre = genre.text.strip()
        except:
            if not genre:
                print("Movie name with no genre: ", movie_name)
                print("+++++++++++++++++++++")
                continue

    
        genres.append(genre)
        movie_ids.append(movie_id)
        
    print("url: ", url)
    print("Movies with genres in this page: ", len(movie_ids))
    print("Genres in this page: ", len(genres))
    print("---------------------")
    
    df = pd.DataFrame({
        'movie_id': movie_ids,
        'genre': genres,
    })
    df.to_csv('data/film_5.csv', index=False, encoding='utf-8')
