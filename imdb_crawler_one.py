from typing import Container
from bs4 import BeautifulSoup
from requests.api import request
import regex as re
import requests
import string
import numpy as np
import pandas as pd
import csv

title_ids = list()
genres = list()

for i in range(1, 50, 50):
    url = "http://www.imdb.com/search/title?at=0&genres=action&sort=moviemeter,asc&start=" + \
        str(i)+"&title_type=feature"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    genre_tags = soup.find_all("span", class_="genre")
    for genre_tag in genre_tags:
        genre = genre_tag.text.strip()
        genres.append(genre)

    a_tags = soup.find_all(href=re.compile('/title/tt'))
    for a_tag in a_tags:
        tmp = a_tag.text.strip()
        if not tmp:
            continue
        else:
            tmp = a_tag['href'].strip()
            # print(tmp[17:21])
            if tmp[17:21] == "vote":
                continue
            title_ids.append(a_tag['href'])

genre_names = list()
ratings = list()
user_names = list()
movie_names = list()
index = 0

for title_id in title_ids:
    url = "https://www.imdb.com"+title_id+"reviews?ref_=tt_ov_rt"
    
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    try:
        curr_genre = genres[index]
    except:
        # print(len(genres))
        # print(index)
        print("out of index")

    curr_movie = soup.find('a', itemprop="url")
    if curr_movie == None:
        continue
    curr_movie = curr_movie.text
    
    num_of_review = soup.find('div',class_='header')
    num_of_review = num_of_review.find('span')
    if num_of_review == None:
        continue
    num_of_review = num_of_review.text
    num_of_review = num_of_review.replace(",","")
    
    num_of_review = [int(s) for s in num_of_review.split() if s.isdigit()]
    
    print(num_of_review)
    a_range = int(num_of_review[0]/25)
    for i in range(a_range):
        data_ajaxurl = title_id + 'reviews/_ajax?paginationKey='
        data_key_tag = soup.find('div',class_='load-more-data')
        data_key = data_key_tag['data-key']
        load_more_url = "https://www.imdb.com"+str(data_ajaxurl)+str(data_key)
        
        containers = soup.findAll('div', class_="review-container")
        for container in containers:
            # print(container)
            # print('------------------------------------------------\n--------------------------------------------------')
            point_scale = container.find("span", class_="point-scale")
            if point_scale == None:
                continue
            rating_tag = point_scale.find_previous_sibling("span")
            rating = rating_tag.text
            ratings.append(rating)
            display_name_link = container.find("span", class_="display-name-link")
            name = display_name_link.text.strip()
            user_names.append(name)
            genre_names.append(curr_genre)
            movie_names.append(curr_movie)
        
            print(len(movie_names))
            print(len(genre_names))
            print(len(user_names))
            print(len(ratings))
            print('---------------')
    index += 1


df = pd.DataFrame({
    'movie_name': movie_names,
    'user_name': user_names,
    'rating': ratings,
    'genre': genre_names, })
df.to_csv('data/imdb_full.csv', index=False, encoding='utf-8')
# <div class="lister-item mode-advanced">
# <div class="lister-top-right">
# <div class="ribbonize" data-caller="filmosearch" data-tconst="tt7991608"></div>
# </div>
# <div class="lister-item-image float-left">
# <a href="/title/tt7991608/"> <img alt="Lệnh Truy Nã Đỏ" class="loadlate" data-tconst="tt7991608" height="98" loadlate="https://m.media-amazon.com/images/M/MV5BZmRjODgyMzEtMzIxYS00OWY2LTk4YjUtMGMzZjMzMTZiN2Q0XkEyXkFqcGdeQXVyMTkxNjUyNQ@@._V1_UX67_CR0,0,67,98_AL_.jpg" src="https://m.media-amazon.com/images/S/sash/4FyxwxECzL-U1J8.png" width="67"/>
# </a> </div>
# <div class="lister-item-content">
# <h3 class="lister-item-header">
# <span class="lister-item-index unbold text-primary">1.</span>
# <a href="/title/tt7991608/">Lệnh Truy Nã Đỏ</a>
# <span class="lister-item-year text-muted unbold">(2021)</span>
# </h3>
# <p class="text-muted">
# <span class="certificate">C13</span>
# <span class="ghost">|</span>
# <span class="runtime">118 min</span>
# <span class="ghost">|</span>
# <span class="genre">
# Action, Comedy, Crime            </span>
# </p>
# <div class="ratings-bar">
# <div class="inline-block ratings-imdb-rating" data-value="6.4" name="ir">
# <span class="global-sprite rating-star imdb-rating"></span>
# <strong>6.4</strong>
# </div>
# <div class="inline-block ratings-user-rating">
# <span class="userRatingValue" data-tconst="tt7991608" id="urv_tt7991608">
# <span class="global-sprite rating-star no-rating"></span>
# <span class="rate" data-no-rating="Rate this" data-value="0" name="ur">Rate this</span>
# </span>
# <div class="starBarWidget" id="sb_tt7991608">
# <div class="rating rating-list" data-csrf-token="" data-ga-identifier="" data-starbar-class="rating-list" data-user="" id="tt7991608|imdb|6.4|6.4|adv_li_tt||advsearch|title" itemprop="aggregateRating" itemscope="" itemtype="http://schema.org/AggregateRating" title="Users rated this 6.4/10 (124,375 votes) - click stars to rate">
# <meta content="6.4" itemprop="ratingValue"/>
# <meta content="10" itemprop="bestRating"/>
# <meta content="124375" itemprop="ratingCount"/>
# <span class="rating-bg"> </span>
# <span class="rating-imdb" style="width: 89.6px"> </span>
# <span class="rating-stars">
# <a href="/register/login?why=vote" rel="nofollow" title="Register or login to rate this title"><span>1</span></a>
# <a href="/register/login?why=vote" rel="nofollow" title="Register or login to rate this title"><span>2</span></a>
# <a href="/register/login?why=vote" rel="nofollow" title="Register or login to rate this title"><span>3</span></a>
# <a href="/register/login?why=vote" rel="nofollow" title="Register or login to rate this title"><span>4</span></a>
# <a href="/register/login?why=vote" rel="nofollow" title="Register or login to rate this title"><span>5</span></a>
# <a href="/register/login?why=vote" rel="nofollow" title="Register or login to rate this title"><span>6</span></a>
# <a href="/register/login?why=vote" rel="nofollow" title="Register or login to rate this title"><span>7</span></a>
# <a href="/register/login?why=vote" rel="nofollow" title="Register or login to rate this title"><span>8</span></a>
# <a href="/register/login?why=vote" rel="nofollow" title="Register or login to rate this title"><span>9</span></a>
# <a href="/register/login?why=vote" rel="nofollow" title="Register or login to rate this title"><span>10</span></a>
# </span>
# <span class="rating-rating"><span class="value">6.4</span><span class="grey">/</span><span class="grey">10</span></span>
# <span class="rating-cancel"><a href="/title/tt7991608/vote" rel="nofollow" title="Delete"><span>X</span></a></span>
#  </div>
# </div>
# </div>
# <div class="inline-block ratings-metascore">
# <span class="metascore unfavorable">39        </span>
#         Metascore
#             </div>
# </div>
# <p class="text-muted">
# An Interpol agent tracks the world's most wanted art thief.</p>
# <p class="">
#     Director:
# <a href="/name/nm1098493/">Rawson Marshall Thurber</a>
# <span class="ghost">|</span>
#     Stars:
# <a href="/name/nm0425005/">Dwayne Johnson</a>,
# <a href="/name/nm0005351/">Ryan Reynolds</a>,
# <a href="/name/nm2933757/">Gal Gadot</a>,
# <a href="/name/nm5709125/">Ritu Arya</a>
# </p>
# <p class="sort-num_votes-visible">
# <span class="text-muted">Votes:</span>
# <span data-value="124375" name="nv">124,375</span>
# </p>
# </div>
# </div>
