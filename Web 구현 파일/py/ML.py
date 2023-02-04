import sys
import pandas as pd
import numpy as np
import time
import sqlite3
import chardet
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

crawling = pd.read_csv('vsfile.txt')
# print("First name: " + sys.argv[1])
# print("Last name: " + sys.argv[2])

x_data = crawling['blogReviewText']
x_data = pd.DataFrame(x_data)
vectorizer=TfidfVectorizer(ngram_range=(1, 3),
    min_df=2,   
    max_features=10000,
    sublinear_tf=True,
    lowercase=False,
    use_idf=True)

# blogReviewText 대해서 tf-idf 수행
x_data_vec = vectorizer.fit_transform(x_data['blogReviewText'])

cosine = cosine_similarity(x_data_vec, x_data_vec)
cosine_sorted = cosine.argsort()[:, ::-1]

restaurant = pd.DataFrame()
score = (
    +cosine*1
    +np.repeat([crawling['star'].values], len(crawling['star']) , axis=0) * 0.001
)

score_sorted = score.argsort()[:, ::-1]

def find_simi_place(crawling, sorted_ind, place_name, top_n):
    
    compare = 0
    index = 0
    
    contains_name = crawling[crawling['Name'].str.contains(place_name)]
    contains_name = contains_name.iloc[0:1]
    
    if contains_name.empty:
        contains_name = crawling[crawling['blogReviewText'].str.contains(place_name)]
        
        for i in range(len(contains_name['blogReviewText'])):
            if contains_name['blogReviewText'].iloc[i].count(place_name) > compare:
                compare = contains_name['blogReviewText'].iloc[i].count(place_name)
                index = i
        contains_name = contains_name.iloc[index:index+1]
            
    place_index = contains_name.index.values
    similar_indexes = sorted_ind[place_index, :(top_n)]
    similar_indexes = similar_indexes.reshape(-1)
    
    return crawling.iloc[similar_indexes]

food = sys.argv[1]
# food = "국밥"


restaurant = find_simi_place(crawling, score_sorted,food,5)
restaurant = restaurant.reset_index()
restaurant = restaurant.drop(['blogReviewText','index','Unnamed: 0'],axis =1 )
# restaurant.to_html("output.html")
# dbpath = "restaurant.db" 

# conn = sqlite3.connect(dbpath) # 데이터베이스 파일에 연결(connect)
# cur = conn.cursor() # 연결된 데이터베이스를 돌아다닐 커서(cursor) 생성
# restaurant.to_sql('restaurant', conn,if_exists="replace")
# print(chardet.detect(restaurant.encode()))
restaurant = restaurant.to_string()
restaurant = restaurant.split()
print(restaurant)

