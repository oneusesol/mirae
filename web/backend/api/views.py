import os
import json
import logging
from django.http import HttpResponse, JsonResponse
from django.conf import settings
from django.db import connections

# 로깅 설정
logger = logging.getLogger(__name__)

# `trends.json`을 읽어오는 API (정적 데이터)
def get_trend_data(request):
    """ `data/trends.json`을 읽어와 반환하는 API """
    json_path = os.path.join(settings.BASE_DIR, "public", "data", "trends.json")

    if not os.path.exists(json_path):
        logger.error("❌ trends.json 파일이 존재하지 않습니다!")
        return JsonResponse({"error": "trends.json not found"}, status=404)

    try:
        with open(json_path, "r", encoding="utf-8") as file:
            data = json.load(file)
        return JsonResponse(data, safe=False)  # JSON 데이터를 반환
    except json.JSONDecodeError as e:
        logger.error(f"⚠ JSON 파일 파싱 오류: {e}")
        return JsonResponse({"error": "Invalid JSON format"}, status=500)


# API 연결 테스트용
def test_api(request):
    return JsonResponse({"message": "Django 연결 테스트"})


# React 빌드된 index.html을 반환하는 API
def frontend(request):
    index_path = os.path.join(settings.BASE_DIR, "build", "index.html")  # React 빌드된 index.html

    if not os.path.exists(index_path):
        return HttpResponse("index.html not found", status=404)

    with open(index_path, "r", encoding="utf-8") as f:
        return HttpResponse(f.read(), content_type="text/html")



# MySQL에서 데이터를 가져오는 API (동적 데이터)
def get_trends(request):
    """ MySQL에서 실시간 트렌드 데이터를 가져오는 API """
    trends = {
        "naver": [],
        "google": [],
        "twitter": [],
    }

    try:
        with connections["crawling_trends_db"].cursor() as cursor:
            cursor.execute("SELECT search_term FROM naver_trend ORDER BY timestamp DESC LIMIT 10")
            trends["naver"] = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT search_term FROM google_trend ORDER BY timestamp DESC LIMIT 10")
            trends["google"] = [row[0] for row in cursor.fetchall()]

            cursor.execute("SELECT search_term FROM twitter_trend ORDER BY timestamp DESC LIMIT 10")
            trends["twitter"] = [row[0] for row in cursor.fetchall()]

        return JsonResponse(trends)
    
    except Exception as e:
        logger.error(f"MySQL 데이터 조회 오류: {e}")
        return JsonResponse({"error": str(e)}, status=500)
