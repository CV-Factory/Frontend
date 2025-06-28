"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from core import views # core.views 모듈을 임포트합니다.

# 언어 코드가 포함되지 않은 공통 URL
urlpatterns = [
    path("admin/", admin.site.urls),
    path('health/', views.health_check, name='health_check'),
    # Django 기본 set_language view (POST) 활성화 – 선택사항
    path('i18n/', include('django.conf.urls.i18n')),
]

# 언어 코드 접두사가 붙는 URL들
urlpatterns += i18n_patterns(
    path('', views.index, name='index'),
    prefix_default_language=False,
)

# 개발 환경에서만 정적 파일을 제공합니다.
# if settings.DEBUG:
#     urlpatterns += staticfiles_urlpatterns() # 이 줄은 삭제됩니다.
