from bs4 import BeautifulSoup
import requests
import pandas as pd
from tqdm.auto import tqdm
import lxml

# 보안뉴스 페이지 URL 템플릿
URL_TEMPLATE = 'http://boannews.com/media/t_list.asp?Page={}&kind='

# 결과를 저장할 리스트 초기화
all_titles = []
all_contents = []
all_links = []

# 크롤링할 페이지 범위 설정 (예: 1페이지부터 5페이지까지)
start_page = 1
end_page = 5

# 각 페이지를 순회하며 크롤링
for page in range(start_page, end_page + 1):
    # URL 요청
    URL = URL_TEMPLATE.format(page)
    site = requests.get(URL)
    print(f"크롤링 중: {URL}")  # 현재 크롤링 중인 페이지 URL 출력

    # BeautifulSoup을 사용하여 HTML 파싱
    site_soup = BeautifulSoup(site.text, 'lxml')

    # 뉴스 리스트 추출
    news_list = site_soup.select('div.news_list')

    # 뉴스 리스트를 순회하며 데이터프레임에 추가
    for news in tqdm(news_list):
        news_title = news.select('span.news_txt')[0].text  # 뉴스 제목 추출
        news_url = news.find('a').get('href')  # 뉴스 URL 추출
        news_url = 'http://boannews.com' + news_url  # 절대 URL로 변환
        news_writer = news.select('span.news_writer')[0].text  # 뉴스 작성자 추출

        # 새로운 데이터 리스트 생성
        new_data = [news_title, news_url, news_writer]
        
        # 리스트에 추가
        all_titles.append(news_title)
        all_links.append(news_url)
        all_contents.append(news_writer)

# 데이터프레임 생성
data = pd.DataFrame({'title': all_titles, 'url': all_links, 'writer': all_contents})

# 데이터프레임을 CSV 파일로 저장
data.to_csv('boannews.csv', encoding='utf-8-sig', index=False)
