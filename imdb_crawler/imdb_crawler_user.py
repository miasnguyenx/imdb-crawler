from collections import Counter
from bs4 import BeautifulSoup
from numpy import empty
import pandas as pd
import requests
import regex as re


df = pd.read_csv('data/imdb_full_3.csv')
ids = list(df['user_id'])
# print(ids)
# exit()
user_ids = list()
# tmp = ids.index(72734720)
# print(tmp)
# print(ids[tmp+1])
# exit()
movie_ids = list()
user_ratings = list()

for user_id in ids[10000:]:
    url = "https://www.imdb.com/user/ur"+str(user_id)+"/ratings"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # return ko phai none dcm
    containers = soup.find_all('div', class_="lister-item-content")

    if not containers:
        print("url review")
        try:
            url = "https://www.imdb.com/user/ur"+str(user_id)+"/reviews"
            page = requests.get(url)
            soup = BeautifulSoup(page.content, "html.parser")
            containers = soup.find_all('div', class_="lister-item-content")
        except:
            continue
        for container in containers:
            movie_id = container.find('div', class_="lister-item-header")
            movie_id = movie_id.find('a')
            movie_id = movie_id['href']
            movie_id = re.findall('[0-9]+', movie_id)
            movie_id = movie_id[0]
            try:
                rating = container.find('div', class_="ipl-ratings-bar")
                rating = rating.find('span', class_="rating-other-user-rating")
                rating = rating.findNext('span').text.strip()
            except:
                continue

            user_ratings.append(rating)
            movie_ids.append(movie_id)
            user_ids.append(user_id)
        print(user_id)
        print(len(user_ratings))
        print(len(user_ids))
        print(len(movie_ids))
        print("--------------")

    else:
        for container in containers:
            movie_id = container.find('h3')
            movie_id = movie_id.find('a')
            movie_id = movie_id['href']
            movie_id = re.findall('[0-9]+', movie_id)
            movie_id = movie_id[0]

            try:
                rating = container.find('div', class_="ipl-rating-widget")
                rating = rating.find(
                    'div', class_="ipl-rating-star ipl-rating-star--other-user small")
                rating = rating.find('span', class_="ipl-rating-star__rating")
                rating = rating.text
            except:
                continue
            user_ratings.append(rating)
            movie_ids.append(movie_id)
            user_ids.append(user_id)

        print(user_id)
        print(len(user_ratings))
        print(len(user_ids))
        print(len(movie_ids))
        print("--------------")

    df = pd.DataFrame({
        'movie_id': movie_ids,
        'user_id': user_ids,
        'rating': user_ratings,
    })
    df.to_csv('data/user13000.csv', index=False, encoding='utf-8')
