import mysql.connector
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

# MySQL 연결 정보
DB_CONFIG = {
    "host": "localhost",  
    "user": "root",  
    "password": "admin",  
    "database": "crawling_db"
}

# MySQL 데이터베이스 연결 및 테이블 생성
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS google_trend (
            id INT AUTO_INCREMENT PRIMARY KEY,
            search_term VARCHAR(255) NOT NULL,
            ranking INT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

# 기존 데이터 삭제 및 ID 초기화
def reset_table():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM google_trend")  # 기존 데이터 삭제
    cursor.execute("ALTER TABLE google_trend AUTO_INCREMENT = 1")  # ID 초기화
    
    conn.commit()
    conn.close()

# 데이터 저장 함수
def save_to_db(search_term, ranking):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO google_trend (search_term, ranking) VALUES (%s, %s)", (search_term, ranking))
    conn.commit()
    conn.close()

# Chrome 옵션 설정
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ChromeDriver 실행 (경로 수정 필요)
service = Service("/usr/local/bin/chromedriver")  
driver = webdriver.Chrome(service=service, options=chrome_options)

# Google Trends URL
url = "https://trends.google.com/trends/trendingsearches/daily?geo=KR&hl=ko"
driver.get(url)

# JavaScript 렌더링 대기 (필수)
time.sleep(5)

# 데이터베이스 초기화 및 기존 데이터 삭제
init_db()
reset_table()

# XPath를 사용해 실시간 인기 검색어 찾기
xpath = '//*[@id="trend-table"]/div[1]/table/tbody/tr/td[2]/div[1]'
elements = driver.find_elements(By.XPATH, xpath)

# 데이터 출력 및 저장
print("실시간 인기 검색어 :")
for idx, element in enumerate(elements, start=1):
    search_term = element.text.strip()
    print(f"{idx}. {search_term}")
    save_to_db(search_term, idx)  # 데이터 저장

# 브라우저 종료
driver.quit()

print("데이터 저장 완료!")
