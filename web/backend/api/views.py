from django.http import JsonResponse

def test_api(request):
    return JsonResponse({"message": "Django 연결 테스트"})
