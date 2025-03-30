from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
import logging
from .models import Resume
from .groq_service import generate_resume
from crawlers.Job_Post_Crawler import fetch_job_description
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import CsrfViewMiddleware
from django.views.decorators.csrf import ensure_csrf_cookie
import json
from django.http import JsonResponse
from crawlers.Target_Company_Crawler import fetch_company_info
from django.views.decorators.csrf import csrf_protect
# from django.utils.decorators import method_decorator

# 로깅 설정
logger = logging.getLogger("api")

@csrf_protect
def fetch_company_info_api(request):
    """
    회사 정보를 크롤링하는 API 엔드포인트
    """
    logger.debug("===== fetch_company_info_api 요청 시작 =====")
    if request.method == "POST":
        try:
            # 요청 정보를 확인
            logger.info(f"요청 헤더: {request.headers}")
            logger.info(f"요청 쿠키: {request.COOKIES}")
            logger.debug(f"요청 본문: {request.body}")    

            # CSRF 토큰 확인
            csrf_cookie = request.COOKIES.get("csrftoken")
            csrf_header = request.headers.get("X-CSRFToken")
            logger.debug(f"서버에서 받은 CSRF 쿠키: {csrf_cookie}")
            logger.debug(f"서버에서 받은 CSRF 헤더: {csrf_header}")
            
            if not csrf_cookie or not csrf_header or csrf_cookie != csrf_header:
                logger.error("CSRF 토큰 검증 실패")
                return JsonResponse({"error": "CSRF 토큰이 일치하지 않습니다."}, status=403)
                                
            data = json.loads(request.body)
            company_url = data.get("company_url")
            logger.debug(f"파싱된 JSON 데이터: {data}")

            if not company_url:
                logger.error("회사 URL 누락")
                return JsonResponse({"error": "회사 URL이 제공되지 않았습니다."}, status=400)

            # 크롤링 시작 로그
            logger.info(f"Fetching company info for URL: {company_url}")

            try:
                # 회사 정보 크롤링 함수 호출
                logger.debug("크롤링 함수 fetch_company_info 호출 시작")
                company_info = fetch_company_info(company_url)
                logger.debug("크롤링 함수 fetch_company_info 호출 완료")
                logger.info(f"Fetched company info: {company_info[:200]}")  # 크롤링 결과 앞 200자 출력
            except Exception as e:
                logger.error(f"Error while fetching company info: {str(e)}", exc_info=True)
                return JsonResponse({"error": "회사 정보를 가져오는 중 오류 발생"}, status=500)

            logger.debug("회사 정보 API 응답 반환")
            response = JsonResponse({"company_info": company_info}, status=200)
            logger.debug(f"응답 데이터: {company_info[:100]}...")
            logger.debug("===== fetch_company_info_api 요청 완료 =====")
            return response

        except json.JSONDecodeError as e:
            logger.error(f"JSON 파싱 오류: {str(e)}", exc_info=True)
            return JsonResponse({"error": "올바른 JSON 형식이 아닙니다."}, status=400)
        except Exception as e:
            logger.error(f"예상치 못한 오류: {str(e)}", exc_info=True)
            return JsonResponse({"error": f"서버 오류: {str(e)}"}, status=500)

    logger.error(f"허용되지 않은 HTTP 메서드: {request.method}")
    return JsonResponse({"error": "허용되지 않은 요청 방식입니다."}, status=405)


@api_view(["OPTIONS", "POST", "GET"])  #  OPTIONS 요청 허용 (CORS 문제 해결)
@permission_classes([AllowAny])  #  로그인 없이도 API 호출 가능하도록 설정
@csrf_exempt
@ensure_csrf_cookie  
def create_resume(request):
    logger.debug("===== create_resume 요청 시작 =====")
    logger.debug(f"요청 메서드: {request.method}")
    
    if request.method == "GET":
        logger.debug("GET 요청 처리: CSRF 쿠키 설정")
        return Response({"message": "CSRF 쿠키 설정됨"}, status=200)
    
    logger.info(" API create_resume 요청 수신됨.")
    logger.debug(f" 요청 헤더: {request.headers}")
    logger.debug(f" 요청 본문: {request.data}")
    logger.info(f" 현재 사용자: {request.user} (인증됨 여부: {request.user.is_authenticated})")

    #  CSRF 정보 확인
    logger.debug(f" CSRF 쿠키: {request.COOKIES.get('csrftoken')}")
    logger.debug(f" CSRF 세션 토큰: {request.session.get('csrftoken')}")

    #  403 Forbidden 발생 원인 추적
    if request.user.is_authenticated is False:
        logger.warning(" 로그인되지 않은 사용자 요청 (403 가능성 높음)")

    if "csrftoken" not in request.COOKIES:
        logger.warning(" CSRF 토큰 없음 (403 가능성 높음)")

    #  Django 내부에서 CSRF 보호로 인해 403이 발생하는지 확인
    try:
        reason = CsrfViewMiddleware().process_view(request, None, (), {})
        if reason:
            logger.error(f" CSRF 보호로 인해 403 발생: {reason}")
    except Exception as e:
        logger.error(f" CSRF 검사 중 오류 발생: {str(e)}")

    try:
        # 요청 데이터 가져오기
        logger.debug("클라이언트 요청 데이터 파싱 시작")
        job_url = request.data.get("recruitment_notice_url")
        company_url = request.data.get("target_company_url", "")  # 선택값 (기본값: 빈 문자열)
        user_story = request.data.get("user_story")

        logger.info(f"받은 recruitment_notice_url: {job_url}")
        logger.info(f"받은 target_company_url: {company_url}")
        logger.debug(f"받은 user_story: {user_story[:100]}...")

        # 필수 값 체크
        if not job_url or not user_story:
            logger.error(" 필수 입력값 누락")
            return Response({"error": "공고 URL과 자기소개 내용은 필수 입력 사항입니다."}, status=400)

        # 🔹 크롤링 실행 (채용 공고 데이터 가져오기)
        logger.debug("채용 공고 크롤링 시작")
        try:
            job_description = fetch_job_description(job_url)
            logger.info(f"채용 공고 크롤링 성공: {job_description[:100]}...")
            logger.debug(f"채용 공고 전체 내용: {job_description}")
        except Exception as e:
            logger.error(f"채용 공고 크롤링 실패: {str(e)}", exc_info=True)
            job_description = "(채용 공고 크롤링 실패)"

        # 🔹 회사 정보 크롤링 (company_url이 있을 경우)
        company_info = ""
        if company_url:
            logger.debug("회사 정보 크롤링 시작")
            try:
                company_info = fetch_company_info(company_url)
                logger.info(f"회사 정보 크롤링 성공: {company_info[:100]}...")
                logger.debug(f"회사 정보 전체 내용: {company_info}")
            except Exception as e:
                logger.error(f" 회사 정보 크롤링 실패: {str(e)}", exc_info=True)
                company_info = "(회사 정보 크롤링 실패)"

        # 🔹 크롤링 데이터 검증 (빈 데이터 체크)
        logger.debug("크롤링 데이터 검증")
        if not job_description or job_description == "(채용 공고 크롤링 실패)":
            logger.error("채용 공고 데이터가 없습니다. GPT 호출을 중단합니다.")
            return Response({"error": "채용 공고 데이터를 가져오는 데 실패했습니다."}, status=500)

        if not company_info or company_info == "(회사 정보 크롤링 실패)":
            logger.warning("회사 정보 데이터가 없습니다. GPT는 채용 공고와 사용자 입력만으로 실행됩니다.")


        # 🔹 GPT API 호출하여 자기소개서 생성
        logger.debug("GPT API 호출 준비")
        try:
            logger.info("GPT 호출 직전 데이터:")
            logger.debug(f"🔹 job_description: {job_description}")
            logger.debug(f"🔹 user_story: {user_story}")
            logger.debug(f"🔹 company_info: {company_info}")
            
            logger.debug("GPT API 호출 시작")
            generated_resume = generate_resume(job_description, user_story, company_info)
            logger.debug("GPT API 호출 완료")
            logger.info(f"GPT 자기소개서 생성 성공: {generated_resume[:100]}...")
            logger.debug(f"생성된 자기소개서 전체: {generated_resume}")
        except Exception as e:
            logger.error(f"GPT API 호출 실패: {str(e)}", exc_info=True)
            return Response({"error": "GPT API 호출 중 문제가 발생했습니다."}, status=500)

        # 🔹 DB 저장
        logger.debug("데이터베이스 저장 시작")
        try:
            resume = Resume.objects.create(
                recruitment_notice_url=job_url,
                target_company_url=company_url,
                job_description=job_description,
                company_info=company_info,
                user_story=user_story,
                generated_resume=generated_resume
            )
            logger.info(f" DB 저장 성공: Resume ID {resume.id}")
        except Exception as e:
            logger.error(f" 데이터베이스 저장 실패: {str(e)}", exc_info=True)
            return Response({"error": "데이터 저장 중 문제가 발생했습니다."}, status=500)

        # 🔹 응답 데이터 반환
        logger.debug("응답 데이터 구성")
        response_data = {
            "resume_id": resume.id,
            "recruitment_notice_url": resume.recruitment_notice_url,
            "target_company_url": resume.target_company_url,
            "user_story": resume.user_story,
            "company_info": resume.company_info,  # 응답에 회사 정보 포함
            "generated_resume": resume.generated_resume,
            "created_at": resume.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

        logger.info(f" 자기소개서 생성 완료: ID {resume.id}")
        logger.debug(f" 응답 데이터: {response_data}")
        logger.debug("===== create_resume 요청 완료 =====")
        return Response(response_data)

    except Exception as e:
        logger.critical(f" 서버 내부 오류 발생: {str(e)}", exc_info=True)
        logger.debug("===== create_resume 요청 실패 =====")
        return Response({"error": "서버에서 오류가 발생했습니다."}, status=500)
