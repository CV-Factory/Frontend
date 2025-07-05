from django.shortcuts import render
from django.http import HttpResponse
from django.utils import translation
from django.conf import settings
from django.shortcuts import redirect

def index(request):
    return render(request, 'index.html')

def health_check(_request):
    return HttpResponse("OK", status=200)

def language_switch(request):
    """프리픽스 없는 / 로 들어오면 Accept-Language 등에 따라 처리
    - 선택된 언어가 기본 언어(en) → 그대로 index 렌더링
    - 그 외 언어 → 해당 프리픽스 URL로 302 리다이렉트
    """
    lang = translation.get_language_from_request(request, check_path=False)
    if lang not in dict(settings.LANGUAGES):
        lang = settings.LANGUAGE_CODE

    if lang == settings.LANGUAGE_CODE:
        # 기본 언어면 슬러그 없이 바로 렌더링
        return index(request)

    return redirect(f"/{lang}/", permanent=False) 