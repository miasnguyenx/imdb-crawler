from collections import Counter
from sklearn import metrics
import sklearn
from sklearn.metrics import davies_bouldin_score
import pandas as pd  # reading all required header files
import numpy as np
import random
import operator
import math
import matplotlib.pyplot as plt
from scipy.spatial import distance
from scipy.stats import multivariate_normal  # for generating pdf

df_full = pd.read_csv("data/imdb_full_4.csv")  # iris data
df_full.info()
print(len(list(df_full['user_id'])))
print(len(Counter(list(df_full['movie_id']))))
print(len(Counter(list(df_full['user_id']))))

