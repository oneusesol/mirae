import mysql.connector
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

# MySQL 연결 정보
DB_CONFIG = {
    "host": "localhost",  
    "user": "root",  
    "password": "admin",  
    "database": "crawling_db"
}

# MySQL 테이블 생성
def init_db():
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS twitter_trend (
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
    
    cursor.execute("DELETE FROM twitter_trend")  
    cursor.execute("ALTER TABLE twitter_trend AUTO_INCREMENT = 1")  
    
    conn.commit()
    conn.close()

# 데이터 저장 함수 (빈 값 필터링 추가)
def save_to_db(search_term, ranking):
    conn = mysql.connector.connect(**DB_CONFIG)
    cursor = conn.cursor()

    # 빈 검색어 또는 None 값 확인
    if not search_term.strip():  
        print(f"빈 검색어 감지 (순위 {ranking}), 저장하지 않음")
        return  # 저장하지 않고 종료
    
    if ranking is None or not isinstance(ranking, int):  
        print(f"순위 값이 비어 있음, 기본값 999 적용: {search_term}")
        ranking = 999  

    cursor.execute("INSERT INTO twitter_trend (search_term, ranking) VALUES (%s, %s)", (search_term, ranking))
    conn.commit()
    conn.close()

# Selenium WebDriver 초기화
def initialize_driver():
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # 헤드리스 모드 (디버깅 시 주석 처리)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver

# 로그인 함수
def login(driver, user_id, user_pw):
    try:
        input_field = driver.find_element(By.NAME, "text")
        input_field.send_keys(user_id)
        
        next_button = driver.find_element(By.XPATH, "//button[@type='button' and contains(., 'Next')]")
        next_button.click()
        
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(user_pw)
        
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="layers"]/div/div/div/div/div/div/div[2]/div[2]/div/div/div[2]/div[2]/div[2]/div/div/div/div/button'))
        )
        login_button.click()
    
    except Exception as e:
        print(f"로그인 과정 중 오류 발생: {e}")

# 크롤링 함수 (빈 값 필터링 추가)
def crawl_trends(driver):
    try:
        driver.get("https://x.com/explore/tabs/trending")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Explore']"))
        )
        
        trends_data = []
        trend_elements = driver.find_element(By.XPATH, "//div[@aria-label='Timeline: Explore']")
        rank_elements = trend_elements.find_elements(By.XPATH, ".//*[@data-testid='trend']")
        
        for rank, rank_element in enumerate(rank_elements, start=1):
            try:
                search_term = rank_element.find_element(By.CSS_SELECTOR, "div.css-146c3p1.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-b88u0q.r-1bymd8e").text.strip()

                # 빈 값 필터링
                if not search_term:
                    print(f"빈 검색어 감지 (순위 {rank}), 저장하지 않음")
                    continue  # 저장하지 않고 건너뛰기
                
                trends_data.append((search_term, rank))
            
            except Exception as e:
                print(f"트렌드 항목 처리 중 오류 발생: {e}")

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
    driver.get("https://x.com/explore")
    time.sleep(3)
    
    init_db()
    reset_table()

    # id/pw 값 입력 후 사용
    user_id = "id"
    user_pw = "pw"
    
    login(driver, user_id, user_pw)
    time.sleep(3)
    
    crawl_trends(driver)
    
    time.sleep(3)
    driver.quit()

    print("데이터 저장 완료!")
