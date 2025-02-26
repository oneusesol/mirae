from django.db import models

# ���̹� Ʈ���� ������ (crawling_trends_db)
class NaverTrend(models.Model):
    search_term = models.CharField(max_length=255)  # �˻���
    ranking = models.IntegerField()  # ����
    timestamp = models.DateTimeField(auto_now_add=True)  # ���� �ð� (�ڵ�)

    class Meta:
        db_table = "naver_trend"
        app_label = "api"

# ���� Ʈ���� ������ (crawling_trends_db)
class GoogleTrend(models.Model):
    search_term = models.CharField(max_length=255)
    ranking = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "google_trend"
        app_label = "api"

# Ʈ���� Ʈ���� ������ (crawling_trends_db)
class TwitterTrend(models.Model):
    search_term = models.CharField(max_length=255)
    ranking = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "twitter_trend"
        app_label = "api"

# ���� ���� ũ�Ѹ� ������ (crawling_news_db)
class BoanNewsCrawling(models.Model):
    title = models.CharField(max_length=255)  # ���� ����
    content = models.TextField()  # ���� ���� (MEDIUMTEXT �� Django������ TextField ���)
    link = models.URLField(max_length=2083)  # ���� ��ũ
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "boan_news_crawling"
        app_label = "api"

# ���̹� ���� ũ�Ѹ� ������ (crawling_news_db)
class NaverNewsCrawling(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField(max_length=2083)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "naver_news_crawling"
        app_label = "api"

# ���� ���� ũ�Ѹ� ������ (crawling_news_db)
class GoogleNewsCrawling(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    link = models.URLField(max_length=2083)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "google_news_crawling"
        app_label = "api"
