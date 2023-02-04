import numpy as np
from bs4 import BeautifulSoup 
import time
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote

def iframe(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser") 

    src_url = "https://blog.naver.com/" + soup.iframe["src"]
    
    return src_url

def crawling(url):
    headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    soup = BeautifulSoup(res.text, "html.parser") 

    if soup.find("div", {"class":"se-main-container"}):
        print('se-main-container')
        text = soup.find("div", {"class":"se-main-container"}).get_text()
        text = text.replace("\n","")
        text = re.sub('&nbsp; | &nbsp;| \n|\t|\r|\u200b','',text)
        print("성공")
        return text

    else:
        print("실패")
        return "실패"
    
blog_review_text =[]
index_count = 0
food = input('음식 : ')
blog_text_result = ""
url = "https://search.naver.com/search.naver?where=post&sm=tab_viw.blog&query=서면" + quote(food)

headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}
res = requests.get(url, headers=headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "html.parser") 

posts = soup.find_all("li",{"class":"bx"})
del posts[0:4]
    
index_count += 1
for post,i in zip(posts,range(5)):
    try:
        post_title = post.find("a",{"class":"api_txt_lines total_tit"}).get_text()
        print("제목 :",post_title)
        post_link = post.find("a",{"class":"api_txt_lines total_tit"})['href']
        blog_text = crawling(iframe(post_link))

        blog_text_result = blog_text_result + blog_text
        blog_text_result = blog_text_result.replace(" ","")
        print("-"*50)
    except:
        print("404에러")
        break
blog_review_text.append(blog_text_result)
blog_review_text = pd.DataFrame(blog_review_text)

from collections import Counter
from konlpy.tag import Twitter

articles = blog_review_text[0].tolist()
articles = ''.join(articles)

twitter = Twitter()
raw_pos_tagged = twitter.pos(articles, norm=True, stem=True)

del_list = ['하다', '있다', '되다', '이다', '돼다', '않다', '그렇다', '아니다', '이렇다', '그렇다', '어떻다'] 
word_cleaned = []
for word in raw_pos_tagged:
    if not word[1] in ["Josa", "Eomi", "Punctuation", "Foreign"]: # Foreign == ”, “ 와 같이 제외되어야할 항목들
        if (len(word[0]) != 1) & (word[0] not in del_list): # 한 글자로 이뤄진 단어들을 제외 & 원치 않는 단어들을 제외
            word_cleaned.append(word[0])

word_counted = Counter(word_cleaned)
word_dic = dict(word_counted)
        
sorted_word_dic = sorted(word_dic.items(), key=lambda x:x[1], reverse=True)

from wordcloud import WordCloud
from wordcloud import ImageColorGenerator # Image 로부터 Color 를 생성(Generate)해내는 객체입니다.
import matplotlib.pyplot as plt
# 아래 옵션들을 원하시는대로 지정하셔서 가장 마음에 드는 워드클라우드를 활용하시면 됩니다.

word_cloud = WordCloud(font_path="C:/Windows/Fonts/malgun.ttf", # 한글 폰트 변경
                       width=2000, height=1000, # 실제 워드클라우드 크기 변경 (해상도 변경)
                       max_words=100, # 최대로 보여질 단어 수 제한
                       background_color='white', # 바탕색 지정 (주석처리할 경우 검정으로 변경됨)
#                        max_font_size=100, # 최대 단어 크기 제한
                      ).generate_from_frequencies(word_dic)

plt.figure(figsize=(15,15)) # Jupyter notebook 상에서 보여지는 워드클라우드 크기 지정 
plt.imshow(word_cloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()

# word_cloud.to_file("word_cloud_7 (white, squared, max100).png")