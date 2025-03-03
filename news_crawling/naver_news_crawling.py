import os
import django
from datetime import datetime
import sys
import time
import random
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from django.db import connections  # 특정 데이터베이스 강제 지정

# Django 환경 설정
sys.path.append("/home/ubuntu/mirae/web/backend")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from api.models import NaverNewsCrawling
from api.models import NaverTrend, GoogleTrend, TwitterTrend  # 키워드 테이블 import

# User-Agent 리스트 (자동화 탐지 우회)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36"
]

# 기존 데이터 삭제 및 ID 초기화
def reset_table():
    with connections["crawling_news_db"].cursor() as cursor:
        cursor.execute("DELETE FROM naver_news_crawling;")
        cursor.execute("ALTER TABLE naver_news_crawling AUTO_INCREMENT = 1;")
    print("테이블 초기화 완료 (데이터 삭제 + ID 리셋)")

# DB에서 키워드 가져오기
def get_keywords():
    keywords = list(NaverTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True))
    keywords += list(GoogleTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True))
    keywords += list(TwitterTrend.objects.using("crawling_trends_db").values_list("search_term", flat=True))
    return list(set(keywords))  # 중복 제거 후 반환

# 데이터 저장 함수
def save_to_db(title, content, link):
    """Django ORM을 사용하여 뉴스 데이터 저장"""
    if not title or not content or not link:
        print("빈 데이터 발견, 저장하지 않음")
        return  

    NaverNewsCrawling.objects.using("crawling_news_db").create(
        title=title.strip(),
        content=content.strip(),
        link=link.strip()
    )

# Selenium WebDriver 초기화
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    
    # 자동화 탐지 방지 옵션
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)
    
    # User-Agent 설정
    chrome_options.add_argument(f"user-agent={random.choice(USER_AGENTS)}")

    driver = webdriver.Chrome(options=chrome_options)
    
    # navigator.webdriver 속성 제거 (자동화 감지 방지)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    return driver


# 날짜 확인 함수
def get_news_date(driver, news_url):
    """ 뉴스 페이지에서 날짜를 가져오고, 시각을 제거하여 반환 """
    driver.get(news_url)
    try:
        date_element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="ct"]/div[1]/div[3]/div[1]/div[1]/span'))
        )
        full_date_text = date_element.text.strip()

        # 날짜에서 시각 제거 (YYYY.MM.DD. HH:MM 형식일 경우)
        clean_date = full_date_text.split()[0]  # 첫 번째 단어만 (날짜 부분만) 추출
        return clean_date

    except Exception as e:
        print(f"Failed getting news date ({news_url}): {e}")
        return None
    
    
# 네이버 뉴스 크롤링 함수
def crawl_naver_news():
    keywords = get_keywords()
    if not keywords:
        print("데이터베이스에 검색어가 없습니다.")
        return

    headers = {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://www.naver.com/",
    }
    
    driver = initialize_driver()  # Selenium WebDriver 초기화
    today_str = datetime.today().strftime("%Y.%m.%d.")  # 오늘 날짜 (네이버 뉴스 형식)

    for i, keyword in enumerate(keywords, 1):
        print(f"[{i}/{len(keyword)}] '{keyword}' 검색 중...")
        url = f"https://search.naver.com/search.naver?where=news&query={keyword}"

        try:
            response = requests.get(url, headers=headers, timeout=5)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f"요청 오류 ({keyword}): {e}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        news_links = [
            a.attrs['href'] for a in soup.select("div.group_news > ul.list_news > li div.news_area > div.news_info > div.info_group > a.info")
            if "news.naver.com" in a.attrs['href']
        ]

        for news_url in news_links:
            try:
                news_date = get_news_date(driver, news_url)  # 뉴스 날짜 가져오기
                
                if news_date != today_str:
                    print(f"* {news_date} (오늘 날짜 아님): {news_url}")
                    continue  # 오늘 날짜가 아니면 크롤링 건너뜀
                
                news_response = requests.get(news_url, headers=headers, timeout=5)
                news_response.raise_for_status()
                news_soup = BeautifulSoup(news_response.text, "html.parser")

                title = news_soup.select_one("#title_area > span")
                content = news_soup.select_one("#dic_area")

                if title and content:
                    save_to_db(title.get_text(), content.get_text(), news_url)

                # 랜덤 딜레이 추가 (트래픽 제한 회피)
                time.sleep(random.uniform(2, 5))

            except requests.exceptions.RequestException as e:
                print(f"뉴스 요청 오류 ({news_url}): {e}")

# 실행 메인 코드
if __name__ == "__main__":
    reset_table()  # 기존 데이터 삭제 + ID 초기화
    crawl_naver_news()
    print("네이버 뉴스 크롤링 완료 및 데이터 저장 완료!")
