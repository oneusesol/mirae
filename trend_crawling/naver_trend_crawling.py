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

from api.models import NaverTrend  # Django ORM 모델 import

# 기존 데이터 삭제 및 ID 초기화
def reset_table():
    """기존 데이터 삭제 및 ID 초기화"""
    with connections["crawling_trends_db"].cursor() as cursor:
        cursor.execute("DELETE FROM naver_trend;")
        cursor.execute("ALTER TABLE naver_trend AUTO_INCREMENT = 1;")
    print("테이블 초기화 완료 (데이터 삭제 + ID 리셋)")

# 특수문자 처리 함수
def clean_text(text):
    """특수문자(#, - 제거, _는 공백으로 변경)"""
    text = re.sub(r'[_]+', ' ', text)  # _를 공백으로 변환
    text = re.sub(r'[#-]', '', text)   # #, - 제거
    return text.strip()

# 데이터 저장 함수
def save_to_db(search_term, ranking):
    """Django ORM을 사용하여 데이터 저장"""
    if not search_term.strip():
        print(f"빈 검색어 감지 (순위 {ranking}), 저장하지 않음")
        return  

    print(f"저장 시도: 검색어 = {search_term}, 순위 = {ranking}")
    NaverTrend.objects.using("crawling_trends_db").create(search_term=search_term, ranking=ranking)
    print(f"저장 완료: 검색어 = {search_term}, 순위 = {ranking}")

# User-Agent 리스트 (자동화 탐지 우회)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.85 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.150 Safari/537.36"
]

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
    chrome_options.add_argument("--lang=ko-KR")

    # 자동화 탐지 방지
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option("useAutomationExtension", False)

    # 랜덤 User-Agent 적용
    user_agent = random.choice(USER_AGENTS)
    chrome_options.add_argument(f"user-agent={user_agent}")

    driver = webdriver.Chrome(options=chrome_options)

    # navigator.webdriver 속성 제거 (자동화 탐지 방지)
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    return driver

# 크롤링 함수
def crawl_trends(driver):
    """실시간 검색어 크롤링"""
    try:
        driver.get("https://www.signal.bz/")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="app"]/div/main/div/section/div/section/section[1]/div[2]/div'))
        )
        print("페이지 로딩 완료!")

        trends_data = []
        index = 1  

        for section in range(1, 3):  
            for n in range(1, 6):  
                xpath = f'//*[@id="app"]/div/main/div/section/div/section/section[1]/div[2]/div/div[{section}]/div[{n}]/div/span[2]'
                try:
                    element = driver.find_element(By.XPATH, xpath)
                    search_term = element.text.strip()

                    if not search_term:
                        print(f"빈 검색어 감지 (순위 {index}), 저장하지 않음")
                        continue  

                    search_term = clean_text(search_term)
                    trends_data.append((search_term, index))
                    index += 1

                except Exception as e:
                    print(f"{index}. 데이터 없음 (에러): {e}")

        for search_term, ranking in trends_data:
            print(f"{ranking}. {search_term}")
            save_to_db(search_term, ranking)  

        return trends_data
    
    except Exception as e:
        print(f"크롤링 오류: {e}")
        return []

# 실행 메인 코드
if __name__ == "__main__":
    driver = initialize_driver()
    print(f"현재 프로세스 PID: {os.getpid()}")
    print(f"Chrome 디버깅 포트: {driver.service.process.pid}")

    reset_table()  # 기존 데이터 삭제 + ID 초기화

    results = crawl_trends(driver)

    if not results:
        print("크롤링된 데이터가 없습니다! XPath를 확인해주세요.")

    time.sleep(3)
    driver.quit()

    print("데이터 저장 완료!")
