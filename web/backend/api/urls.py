from django.urls import path
from api.views import test_api, get_trends, get_trend_data

urlpatterns = [
    path("test/", test_api, name="test-api"),  # API �׽�Ʈ ��������Ʈ
    path("trends-live/", get_trends, name="trends-live"),  # MySQL �ǽð� ������
    path("trends-static/", get_trend_data, name="trends-static"),  # JSON ������
]
