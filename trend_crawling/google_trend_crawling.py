import os
import django
import sys
import time
import re
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from django.db import connections  # 특정 데이터베이스 강제 지정

# Django 환경 설정
sys.path.append("/home/ubuntu/mirae/web/backend")  # Django 루트 경로 추가
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # Django 설정 로드
django.setup()  # Django 환경 초기화

from api.models import GoogleTrend  # Django ORM 모델 import

# 기존 데이터 삭제 및 ID 초기화
def reset_table():
    """기존 데이터 삭제 및 ID 초기화"""
    with connections["crawling_trends_db"].cursor() as cursor:  # MySQL 강제 지정
        cursor.execute("DELETE FROM google_trend;")  # 기존 데이터 삭제
        cursor.execute("ALTER TABLE google_trend AUTO_INCREMENT = 1;")  # ID 값 초기화
    print("테이블 초기화 완료 (데이터 삭제 + ID 리셋)")

# 데이터 저장 함수
def save_to_db(search_term, ranking):
    """Django ORM을 사용하여 데이터 저장"""
    if not search_term.strip():  # 빈 검색어 필터링
        print(f"빈 검색어 감지 (순위 {ranking}), 저장하지 않음")
        return  

    print(f"저장 시도: 검색어 = {search_term}, 순위 = {ranking}")
    GoogleTrend.objects.using("crawling_trends_db").create(search_term=search_term, ranking=ranking)
    print(f"저장 완료: 검색어 = {search_term}, 순위 = {ranking}")

# Selenium WebDriver 초기화
def initialize_driver():
    """크롬 드라이버 초기화 및 자동화 탐지 방지"""
    chrome_profile_dir = f"/tmp/chrome-profile-{os.getpid()}"

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument(f"--user-data-dir={chrome_profile_dir}")
    chrome_options.add_argument(f"--remote-debugging-port={random.randint(5000, 9000)}")
    chrome_options.add_argument("--lang=ko-KR")  # 한국어 설정

    # 자동화 탐지 방지
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # User-Agent 변경 (랜덤 적용 가능)
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36"
    chrome_options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(options=chrome_options)

    # DevTools 실행을 통한 자동화 탐지 방지
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver

# 크롤링 함수
def crawl_trends(driver):
    """Google Trends에서 실시간 검색어 크롤링"""
    try:
        driver.get("https://trends.google.com/trends/trendingsearches/daily?geo=KR&hl=ko")

        # 페이지가 완전히 로드될 때까지 대기 (최대 20초)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="trend-table"]/div[1]/table'))
        )
        print("Google Trends 페이지 로딩 완료!")

        trends_data = []
        xpath = '//*[@id="trend-table"]/div[1]/table/tbody/tr/td[2]/div[1]'

        # 최대 3번 재시도
        for attempt in range(3):
            elements = driver.find_elements(By.XPATH, xpath)
            if elements:
                break  # 찾으면 바로 탈출
            print(f"데이터 로딩 재시도 {attempt + 1}/3")
            time.sleep(5)  # 5초 대기 후 재시도

        if not elements:
            print("크롤링 실패! XPath가 데이터를 찾지 못함.")
            return []

        for idx, element in enumerate(elements, start=1):
            search_term = element.text.strip()

            if not search_term:
                print(f"빈 검색어 감지 (순위 {idx}), 저장하지 않음")
                continue  

            trends_data.append((search_term, idx))

            # 크롤링 간 랜덤한 지연 시간 추가
            time.sleep(random.uniform(1, 3))

        for search_term, ranking in trends_data:
            print(f"{ranking}. {search_term}")
            save_to_db(search_term, ranking)  

        return trends_data

    except Exception as e:
        print(f"크롤링 오류: {e}")
        return []

# 실행 메인 코드
if __name__ == "__main__":
    print(f"현재 프로세스 PID: {os.getpid()}")
    driver = initialize_driver()
    print(f"Chrome 디버깅 포트: {driver.capabilities.get('goog:chromeOptions', {}).get('debuggerAddress', 'Unknown')}")

    driver.get("https://trends.google.com/trends/trendingsearches/daily?geo=KR&hl=ko")
    time.sleep(3)
    
    reset_table()  # 기존 데이터 삭제 + ID 초기화
    
    results = crawl_trends(driver)
    
    if not results:
        print("크롤링된 데이터가 없습니다! XPath를 확인해주세요.")
    
    time.sleep(3)
    driver.quit()

    print("데이터 저장 완료!")
