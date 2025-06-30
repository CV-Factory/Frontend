from django.shortcuts import render
from django.http import HttpResponse
from django.utils import translation
from django.conf import settings
from django.shortcuts import redirect

def index(request):
    return render(request, 'index.html')

def health_check(request):
    return HttpResponse("OK", status=200)

def language_switch(request):
    """프리픽스 없는 / 로 들어오면 Accept-Language 등을 참고해 언어 프리픽스로 리다이렉트"""
    # URL 경로가 비어 있으므로 check_path=False 로 헤더·쿠키만 사용
    lang = translation.get_language_from_request(request, check_path=False)
    # 지원하지 않는 언어라면 기본 언어로 대체
    if lang not in dict(settings.LANGUAGES):
        lang = settings.LANGUAGE_CODE

    # 선택된 언어로 프리픽스 리다이렉트 (302)
    return redirect(f"/{lang}/", permanent=False) 