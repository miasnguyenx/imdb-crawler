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
ratings = list()
user_ids = list()
movie_ids = list()

df = pd.read_csv('data/film_5.csv')
title_ids_with_tt = list(dict.fromkeys(df['movie_id']))
for title_id_with_tt in title_ids_with_tt:
    title_id = re.findall('[0-9]+', title_id_with_tt)
    title_id = title_id[0]
    title_ids.append(title_id)

for title_id in title_ids[0:5000]:
    try:
        url = "https://www.imdb.com/title/tt" + \
            str(title_id)+"/reviews?ref_=tt_ov_rt"
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
    except:
        print('Cannot request url: ', url)
        print('++++++++++++++++++++++++')

    num_of_review = soup.find('div', class_='header')
    if not num_of_review:
        print("This film has no review: ")
        print("Film id: ", title_id)
        print('Continue ... ')
        print('++++++++++++++++++++++++')
        continue
    num_of_review = num_of_review.find('span')
    num_of_review = num_of_review.text
    num_of_review = num_of_review.replace(",", "")

    num_of_review = [int(s) for s in num_of_review.split() if s.isdigit()]
    num_of_review = num_of_review[0]
    if num_of_review > 1000:
        a_range = 40
    elif num_of_review <= 25:
        a_range = 1
    else:
        a_range = int(num_of_review/25)
    print('----------------------')
    print("Url: ", url)

    for i in range(a_range):
        containers = soup.findAll('div', class_="review-container")
        for container in containers:
            point_scale = container.find("span", class_="point-scale")
            if point_scale == None:
                # print('one review has no rating: ')
                # print("Film id: ", title_id)
                # print('Continue ... ')
                # print('++++++++++++++++++++++++')
                continue
            rating_tag = point_scale.find_previous_sibling("span")
            rating = rating_tag.text
            display_name_link = container.find(
                "span", class_="display-name-link")
            name = display_name_link.text.strip()
            display_name_link = display_name_link.find('a')
            user_id = display_name_link['href']
            user_id = re.findall('[0-9]+', user_id)
            user_id = 'ur'+str(user_id[0])
            
            a_title_id = 'tt'+str(title_id)
            
            ratings.append(rating)
            movie_ids.append(a_title_id)
            user_ids.append(user_id)

            print("Review No: ", len(ratings))

        data_ajaxurl = str(title_id) + '/reviews/_ajax?paginationKey='
        try:
            data_key_tag = soup.find('div', class_='load-more-data')

            data_key = data_key_tag['data-key']
        except:
            print("Load more end")
            print('Continue .......')
            break
        try:
            load_more_url = "https://www.imdb.com/title/tt" + \
                str(data_ajaxurl)+str(data_key)
            page = requests.get(load_more_url)
            soup = BeautifulSoup(page.content, 'html.parser')
        except:
            print('Cannot request url: ', load_more_url)
            print('++++++++++++++++++++++++')

    df = pd.DataFrame({
        'movie_id': movie_ids,
        'user_id': user_ids,
        'rating': ratings,
    })
    df.to_csv('data/imdb_full_8.csv', index=False, encoding='utf-8')
