from bs4 import BeautifulSoup
import requests
import regex as re
import pandas as pd


title_ids = list()
genres = list()
movies = list()
for i in range(1, 20000, 50):
    url = "http://www.imdb.com/search/title?at=0&genres=action&sort=moviemeter,asc&start=" + \
        str(i)+"&title_type=feature"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    genre_tags = soup.find_all("span", class_="genre")
    print(len(genre_tags))
    for genre_tag in genre_tags:
        genre = genre_tag.text.strip()
        genres.append(genre)

    a_tags = soup.find_all('span', class_="lister-item-index unbold text-primary")

    for a_tag in a_tags:
        a_tag = a_tag.find_next_sibling("a")
        a_href = a_tag['href']
        movie_id = re.findall('[0-9]+', a_href)
        movies.append(movie_id[0])
        title_ids.append(a_tag['href'])
    print("total_genres: ",len(genres))
    print("total_movies: ",len(movies))
    
    df = pd.DataFrame({
    'movie_id': movies,
    'genre': genres, 
    })
    df.to_csv('data/film.csv', index=False, encoding='utf-8')