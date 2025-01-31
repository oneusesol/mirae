from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time


def initialize_driver():
    """
    Selenium WebDriver를 초기화하는 함수 (헤드리스 모드)
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # 헤드리스 모드 설정
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    return driver


def login(driver, user_id, user_pw):
    """
    로그인 기능을 수행하는 함수
    """
    try:
        # ID 입력
        input_field = driver.find_element(By.NAME, "text")
        input_field.send_keys(user_id)
        #print("ID 입력 성공!")
        
        # '다음' 버튼 클릭
        next_button = driver.find_element(By.XPATH, "//button[@type='button' and contains(., '다음')]")
        next_button.click()
        
        # Password 입력
        password_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.NAME, "password"))
        )
        password_field.send_keys(user_pw)
        
        # '로그인하기' 버튼 클릭
        login_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@data-testid='LoginForm_Login_Button']"))
        )
        login_button.click()
        #print("로그인 성공!")
    
    except Exception as e:
        print(f"로그인 과정 중 오류 발생: {e}")


def crawl_trends(driver):
    """
    X (트위터)에서 트렌드를 크롤링하는 함수
    """
    try:
        # Trend 페이지로 이동
        driver.get("https://x.com/explore/tabs/trending")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@aria-label='Timeline: Explore']"))
        )
        
        trends_data = []
        trend_elements = driver.find_element(By.XPATH, "//div[@aria-label='Timeline: Explore']")
        rank_elements = trend_elements.find_elements(By.XPATH, ".//*[@data-testid='trend']")
        
        for rank_element in rank_elements:
            try:
                word = rank_element.find_element(By.CSS_SELECTOR, "div.css-146c3p1.r-bcqeeo.r-1ttztb7.r-qvutc0.r-37j5jr.r-a023e6.r-rjixqe.r-b88u0q.r-1bymd8e").text
                trends_data.append(word)
            except Exception as e:
                print(f"트렌드 항목 처리 중 오류 발생: {e}")
        
        for trend in trends_data:
            print(trend)
        
        return trends_data
    
    except Exception as e:
        print(f"크롤링 오류: {e}")
        return []


if __name__ == "__main__":
    driver = initialize_driver()
    driver.get("https://x.com/explore")
    time.sleep(3)
    
    # 로그인 정보 설정 ------- ! ID, PW 입력 필요 !
    user_id = "ID입력"
    user_pw = "PW입력"
    
    # 로그인 수행
    login(driver, user_id, user_pw)
    time.sleep(3)
    
    # 트렌드 크롤링 실행
    crawl_trends(driver)
    
    # 종료 전 대기
    time.sleep(3)
    driver.quit()
