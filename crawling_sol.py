from bs4 import BeautifulSoup
import requests
from tqdm import tqdm

import pandas as pd
import datetime

# trend API -> Keyword Filter -> url 합치기
# 키워드 api 연동하기 
keywords = ['트럼프', '코인', '명절', '택배']

# 네이버 뉴스의 URL
url = 'https://search.naver.com/search.naver?&where=news&query=' + keywords[0]

# ConnectionError방지
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

# keywords에 걸린 기사들 (10개) 주소 크롤링
original_html = requests.get(url,headers=headers)
html = BeautifulSoup(original_html.text, "html.parser")

url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")

# 걸린 주소 중 언론사 홈페이지 주소를 제외한 기사주소만 정렬
url = []
for i in url_naver:
    if "news.naver.com" in str(i):
        #print(i.attrs['href'])
        url.append(i.attrs['href'])


titles = []
contents = []
links = []

# 뉴스 제목, 링크, 내용 가져오기
for i in url:
    news = requests.get(i, headers=headers)
    news_html = BeautifulSoup(news.text, "html.parser")
    
    articles_content = news_html.select_one('#dic_area')
    articles_content = articles_content.get_text()
    contents.append(articles_content)
    
    articles_title = news_html.select_one('#title_area > span')
    articles_title = articles_title.get_text()
    titles.append(articles_title)
    
    articles_link = i
    links.append(articles_link)
   
# print("articles nums : ", end="")
# print( len(articles_link))

#데이터 프레임 만들기
news_df = pd.DataFrame({'title':titles,'link':links,'content':contents})

#cvs 저장
now = datetime.datetime.now() 
news_df.to_csv('{}_{}.csv'.format(keywords[0],now.strftime('%Y%m%d_%H시%M분%S초')),encoding='utf-8-sig',index=False)    # 이름 keyword 배열 구현해야함