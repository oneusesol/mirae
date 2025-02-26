import os
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path 
from api.views import frontend  

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),  # API 경로 포함
]

# React Router가 관리하는 모든 경로를 Django가 `frontend`로 넘기도록 설정
urlpatterns += [re_path(r"^(?!api/).*", frontend)]

# 정적 파일 서빙 (React 정적 파일)
urlpatterns += static("/static/", document_root=os.path.join(settings.BASE_DIR, "build", "static"))
urlpatterns += static("/public/", document_root=os.path.join(settings.BASE_DIR, "public"))
urlpatterns += static("/data/", document_root=os.path.join(settings.BASE_DIR, "public"))


