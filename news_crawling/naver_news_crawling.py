# DB 2차 적용 (최종_1)

from bs4 import BeautifulSoup
import requests
from tqdm import tqdm
import mysql.connector

# MySQL 연결 정보
DB_CONFIG_NEWS = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "crawling_news_db"
}

DB_CONFIG_KEYWORDS = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "crawling_db"
}

# MySQL 데이터베이스 및 테이블 생성
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG_NEWS)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS naver_news_crawling (
            id INT AUTO_INCREMENT PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            content MEDIUMTEXT NOT NULL,
            link VARCHAR(2083) NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# MySQL에서 키워드 가져오기 (crawling_trend_db에서 가져오기)
def get_keywords():
    conn = mysql.connector.connect(**DB_CONFIG_KEYWORDS)
    cursor = conn.cursor()
    
    # `naver_trend`, `google_trend`, `twitter_trend` 테이블에서 검색어 가져오기
    cursor.execute("""
        SELECT search_term FROM naver_trend 
        UNION 
        SELECT search_term FROM google_trend 
        UNION 
        SELECT search_term FROM twitter_trend
    """)
    
    keywords = [row[0] for row in cursor.fetchall()]
    conn.close()
    return keywords


# 데이터 저장 함수
def save_to_db(title, content, link):
    conn = mysql.connector.connect(**DB_CONFIG_NEWS)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO naver_news_crawling (title, content, link) VALUES (%s, %s, %s)", (title, content, link))
    conn.commit()
    conn.close()

# 데이터베이스 초기화
init_db()

# 데이터베이스에서 키워드 가져오기
keywords = get_keywords()
if not keywords:
    print("No keywords found in the database.")
    exit()

# ConnectionError 방지
headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102"}

# 모든 키워드에 대해 크롤링 수행
for keyword in keywords:
    url = f'https://search.naver.com/search.naver?&where=news&query={keyword}'
    original_html = requests.get(url, headers=headers)
    html = BeautifulSoup(original_html.text, "html.parser")
    
    url_naver = html.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
    
    news_urls = [i.attrs['href'] for i in url_naver if "news.naver.com" in str(i)]
    
    for news_url in news_urls:
        news = requests.get(news_url, headers=headers)
        news_html = BeautifulSoup(news.text, "html.parser")
        
        articles_content = news_html.select_one('#dic_area')
        if articles_content:
            content = articles_content.get_text()
        else:
            content = "No content found"
        
        articles_title = news_html.select_one('#title_area > span')
        if articles_title:
            title = articles_title.get_text()
        else:
            title = "No title found"
        
        link = news_url
        
        # 데이터 저장
        save_to_db(title, content, link)

# 데이터 저장 완료
print("News data has been successfully stored in the database.")
