import pymysql
import textrank_keyword_import


# MySQL 연결 정보
DB_CONFIG_NEWS = {
    "host": "localhost",
    "user": "root",
    "password": "password",
    "database": "crawling_news_db"
}

# MYSQL 연결
# conn = pymysql.connect(**DB_CONFIG_NEWS)
# cursor = conn.cursor()


# news 가져오기
def get_news():
    conn = pymysql.connect(**DB_CONFIG_NEWS)
    cursor = conn.cursor()
    
    # sql_query = """SELECT content FROM boan_news_crawling
    #                 UNION ALL
    #                 SELECT content FROM naver_news_crawling
    #                 UNION ALL
    #                 SELECT content FROM google_news_crawling
    #             """
    
    sql_query = """SELECT id, content FROM naver_news_crawling"""
    cursor.execute(sql_query)

    news = [row for row in cursor.fetchall()]

    conn.close()
    
    return news


# def save_to_db(keyword, id):
#     conn = pymysql.connect(**DB_CONFIG_NEWS)
#     cursor = conn.cursor()

#     cursor.execute("UPDATE naver_news_crawling SET content = (%s) WHERE id = (%s)", (keyword, id))

#     conn.commit()
#     conn.close()

def save_to_db(save_data):
    conn = pymysql.connect(**DB_CONFIG_NEWS)
    cursor = conn.cursor()

    sql_query = """UPDATE naver_news_crawling SET content = %s WHERE id = %s"""
    cursor.executemany(sql_query, save_data)

    conn.commit()
    conn.close()
    
if __name__ == "__main__":
    
    # news 가져오기
    news = get_news()

    # news 핵심 키워드 추출
    save_data = []
    
    for new in news:
        keywords = textrank_keyword.textrank_keyword_main(new[1])
        keyword = ", ".join(keywords)
        data = (keyword, new[0])
        save_data.append(data)
    
    # DB 재저장 하기
    save_to_db(save_data)
        
    