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

# MySQL 데이터베이스 연결 (테이블 생성만 수행, 삭제는 하지 않음)
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS naver_trend (
            id INT AUTO_INCREMENT PRIMARY KEY,
            search_term VARCHAR(255) NOT NULL,
            ranking INT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

# 기존 데이터 삭제 및 ID 초기화 (테이블 삭제 없이)
def reset_table():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    
    cursor.execute("DELETE FROM naver_trend")  # 데이터만 삭제
    cursor.execute("ALTER TABLE naver_trend AUTO_INCREMENT = 1")  # ID 초기화
    
    conn.commit()
    conn.close()

# 데이터 저장 함수
def save_to_db(search_term, ranking):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO naver_trend (search_term, ranking) VALUES (%s, %s)", (search_term, ranking))
    conn.commit()
    conn.close()

# Chrome 옵션 설정 (Headless 모드)
chrome_options = Options()
chrome_options.add_argument("--headless")  
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# ChromeDriver 실행 (경로 수정 필요)
service = Service("/usr/local/bin/chromedriver")  
driver = webdriver.Chrome(service=service, options=chrome_options)

# Signal.bz 사이트 접속
url = "https://www.signal.bz/"
driver.get(url)

# 데이터베이스 초기화 (데이터만 삭제하고 테이블 유지)
init_db()
reset_table()

# 데이터 크롤링
print("실시간 인기 검색어 목록:")
index = 1  # 순위 초기화

for section in range(1, 3):  
    for n in range(1, 6):  
        xpath = f'//*[@id="app"]/div/main/div/section/div/section/section[1]/div[2]/div/div[{section}]/div[{n}]/div/span[2]'
        try:
            element = driver.find_element(By.XPATH, xpath)
            search_term = element.text.strip()
            print(f"{index}. {search_term}")
            save_to_db(search_term, index)  
            index += 1  
        except Exception as e:
            print(f"{index}. 데이터 없음 (에러): {e}")  

# 브라우저 종료
driver.quit()

print("데이터 저장 완료!")
