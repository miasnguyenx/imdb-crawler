from bs4 import BeautifulSoup
import requests
import regex as re
import pandas as pd


title_ids = list()
genres = list()
movies = list()
for i in range(1, 20000, 250):
    url = "https://www.imdb.com/search/title/?moviemeter="+str(10001+i)+","+str(10251+i)+"&count=250"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    
    genre_tags = soup.find_all("span", class_="genre")

    if (len(genre_tags) < 250):
        continue
    for genre_tag in genre_tags:
        genre = genre_tag.text.strip()
        if not genre:
            genre = "NaN"
        genres.append(genre)

    a_tags = soup.find_all(
        'span', class_="lister-item-index unbold text-primary")

    for a_tag in a_tags:
        a_tag = a_tag.find_next_sibling("a")
        a_href = a_tag['href']
        movie_id = re.findall('[0-9]+', a_href)
        movie_id = str(movie_id[0])
        movies.append(movie_id)
        title_ids.append(a_tag['href'])
    print("total_genres: ", len(genres))
    print("total_movies: ", len(movies))

    df = pd.DataFrame({
        'movie_id': movies,
        'genre': genres,
    })
    df.to_csv('data/film_3.csv', index=False, encoding='utf-8')
