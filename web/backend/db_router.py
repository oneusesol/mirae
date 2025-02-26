class DatabaseRouter:
   
    def db_for_read(self, model, **hints):

        if model._meta.db_table in ["naver_trend", "google_trend", "twitter_trend"]:
            return "crawling_trends_db"
        elif model._meta.db_table in ["boan_news_crawling", "naver_news_crawling", "google_news_crawling"]:
            return "crawling_news_db"
        return None

    def db_for_write(self, model, **hints):
        if model._meta.db_table in ["naver_trend", "google_trend", "twitter_trend"]:
            return "crawling_trends_db"
        elif model._meta.db_table in ["boan_news_crawling", "naver_news_crawling", "google_news_crawling"]:
            return "crawling_news_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if db == "crawling_trends_db":
            return model_name in ["navertrend", "googletrend", "twittertrend"]
        elif db == "crawling_news_db":
            return model_name in ["boannewscrawling", "navernewscrawling", "googlenewscrawling"]
        return None
