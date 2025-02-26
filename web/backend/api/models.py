from django.db import models

# 네이버 트렌드 데이터 (crawling_trends_db)
class NaverTrend(models.Model):
    search_term = models.CharField(max_length=255)  # 검색어
    ranking = models.IntegerField()  # 순위
    timestamp = models.DateTimeField(auto_now_add=True)  # 생성 시간 (자동)

    class Meta:
        db_table = "naver_trend"
        app_label = "api"

# 구글 트렌드 데이터 (crawling_trends_db)
class GoogleTrend(models.Model):
    search_term = models.CharField(max_length=255)
    ranking = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "google_trend"
        app_label = "api"

# 트위터 트렌드 데이터 (crawling_trends_db)
class TwitterTrend(models.Model):
    search_term = models.CharField(max_length=255)
    ranking = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "twitter_trend"
        app_label = "api"

# 보안 뉴스 크롤링 데이터 (crawling_news_db)
class BoanNewsCrawling(models.Model):
    title = models.CharField(max_length=255)  # 뉴스 제목
    content = models.TextField()  # 뉴스 내용 (MEDIUMTEXT → Django에서는 TextField 사용)
    link = models.URLField(max_length=2083)  # 뉴스 링크
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "boan_news_crawling"
        app_label = "api"

# 네이버 뉴스 크롤링 데이터 (crawling_news_db)
class NaverNewsCrawling(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField(max_length=2083)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "naver_news_crawling"
        app_label = "api"

# 구글 뉴스 크롤링 데이터 (crawling_news_db)
class GoogleNewsCrawling(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField(max_length=2083)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "google_news_crawling"
        app_label = "api"
