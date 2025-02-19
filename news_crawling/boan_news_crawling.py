from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import mysql.connector

# MySQL 연결 정보
DB_TREND_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "crawling_trends_db"
}

DB_NEWS_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "admin",
    "database": "crawling_news_db"
}

# MySQL에서 키워드 가져오기
def get_keywords():
    conn = mysql.connector.connect(**DB_TREND_CONFIG)
    cursor = conn.cursor()
    
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

# MySQL에 데이터 저장
def save_to_db(title, content, link):
    conn = mysql.connector.connect(**DB_NEWS_CONFIG)
    cursor = conn.cursor()

    # 중복 체크 후 삽입
    cursor.execute("SELECT id FROM boan_news_crawling WHERE link = %s", (link,))
    if cursor.fetchone() is None:  # 중복되지 않는 경우만 저장
        cursor.execute("""
            INSERT INTO boan_news_crawling (title, content, link)
            VALUES (%s, %s, %s)
        """, (title, content, link))
        conn.commit()
        print(f"Saved to DB: {title}")
    else:
        print(f"Skipping (Already in DB): {title}")

    conn.close()

# Selenium WebDriver 초기화
def initialize_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")  # GPU 사용 방지 (메모리 절약)
    chrome_options.add_argument("--window-size=1920,1080")  # 브라우저 크기 지정
    # chrome_options.add_argument("--headless")  # 필요하면 활성화

    service = Service("/usr/local/bin/chromedriver")
    driver = webdriver.Chrome(service=service, options=chrome_options)

    return driver

# 보안뉴스 검색 후 뉴스 본문 크롤링
def search_boannews_and_scrape_results(search_query):
    driver = initialize_driver()
    search_url = "https://www.boannews.com/search/list.asp"

    # 보안뉴스 검색 페이지 이동
    driver.get(search_url)
    time.sleep(3)

    try:
        # 검색창 요소 찾기
        search_input = driver.find_element(By.NAME, "find")
        search_input.clear()
        search_input.send_keys(search_query)  # 검색어 입력
        search_input.send_keys(Keys.RETURN)  # 엔터키 입력으로 검색 실행
        time.sleep(3)

        # '전체뉴스 검색결과 더보기' 버튼 클릭
        try:
            more_results_button = driver.find_element(By.XPATH, "//span[contains(text(),'전체뉴스 검색결과 더보기')]")
            more_results_button.click()
            time.sleep(3)
        except Exception as e:
            print("No '전체뉴스 검색결과 더보기' button found or failed to click.")

        # 검색 결과 페이지의 원래 창 핸들 저장
        original_window = driver.current_window_handle

        # 검색 결과에서 뉴스 기사 링크들 가져오기
        news_elements = driver.find_elements(By.CSS_SELECTOR, "div.news_list a")
        news_links = []
        
        for news in news_elements:
            news_link = news.get_attribute("href")
            if news_link and not news_link.startswith("http"):
                news_link = "https://www.boannews.com" + news_link  # 상대경로 처리
            if news_link not in news_links:
                news_links.append(news_link)
        
        for index, news_link in enumerate(news_links):
            try:
                print(f"\n[{index+1}] Opening News Link: {news_link}")

                # 새 창에서 기사 열기
                driver.execute_script(f"window.open('{news_link}', '_blank');")
                time.sleep(3)

                # 새 창으로 전환
                driver.switch_to.window(driver.window_handles[-1])
                time.sleep(3)

                # 기사 본문 크롤링
                try:
                    title = driver.find_element(By.TAG_NAME, "h1").text
                    article_body = driver.find_element(By.XPATH, "//*[@id='news_content']").text

                    print("Article Title:", title)
                    print("Article Content:")
                    print(article_body[:500] + "...")  # 긴 본문은 앞부분 500자만 출력

                    # 데이터베이스에 저장
                    save_to_db(title, article_body, news_link)

                except Exception as e:
                    print("Failed to retrieve article content.")

                # 현재 창 닫기
                driver.close()

                # 검색 결과 페이지로 복귀
                driver.switch_to.window(original_window)
                time.sleep(3)

            except Exception as e:
                print(f"Error processing news link {index+1}: {e}")

        print("Crawling completed.")

    except Exception as e:
        print(f"Error during search: {e}")

    driver.quit()

# 실행 메인 코드
if __name__ == "__main__":
    keywords = get_keywords()  # 트렌드 키워드 가져오기
    for keyword in keywords:
        print(f"Searching news for keyword: {keyword}")
        search_boannews_and_scrape_results(keyword)
