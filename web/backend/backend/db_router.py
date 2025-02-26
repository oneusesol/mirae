class DatabaseRouter:
    """
    ´ÙÁß µ¥ÀÌÅÍº£ÀÌ½º ¶ó¿ìÆÃÀ» °ü¸®ÇÏ´Â Å¬·¡½º
    """

    def db_for_read(self, model, **hints):
        """¸ðµ¨º° ÀÐ±â Àü¿ë µ¥ÀÌÅÍº£ÀÌ½º ÁöÁ¤"""
        if model._meta.db_table in ["naver_trend", "google_trend", "twitter_trend"]:
            return "crawling_trends_db"
        elif model._meta.db_table in ["boan_news_crawling", "naver_news_crawling", "google_news_crawling"]:
            return "crawling_news_db"
        return None

    def db_for_write(self, model, **hints):
        """¸ðµ¨º° ¾²±â Àü¿ë µ¥ÀÌÅÍº£ÀÌ½º ÁöÁ¤"""
        if model._meta.db_table in ["naver_trend", "google_trend", "twitter_trend"]:
            return "crawling_trends_db"
        elif model._meta.db_table in ["boan_news_crawling", "naver_news_crawling", "google_news_crawling"]:
            return "crawling_news_db"
        return None

    def allow_relation(self, obj1, obj2, **hints):
        """°°Àº µ¥ÀÌÅÍº£ÀÌ½º ³»¿¡¼­¸¸ °ü°è¸¦ Çã¿ë"""
        db_set = {"crawling_trends_db", "crawling_news_db"}
        if obj1._state.db in db_set and obj2._state.db in db_set:
            return obj1._state.db == obj2._state.db  # °°Àº DB ³»¿¡¼­¸¸ Çã¿ë
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """¸¶ÀÌ±×·¹ÀÌ¼ÇÀ» Çã¿ëÇÒ µ¥ÀÌÅÍº£ÀÌ½º ÁöÁ¤"""
        if db == "crawling_trends_db":
            return model_name.lower() in ["navertrend", "googletrend", "twittertrend"]
        elif db == "crawling_news_db":
            return model_name.lower() in ["boannewscrawling", "navernewscrawling", "googlenewscrawling"]
        return None
