from django.urls import path
from api.views import test_api, get_trends, get_trend_data

urlpatterns = [
    path("test/", test_api, name="test-api"),  # API 테스트 엔드포인트
    path("trends-live/", get_trends, name="trends-live"),  # MySQL 실시간 데이터
    path("trends-static/", get_trend_data, name="trends-static"),  # JSON 데이터
]
