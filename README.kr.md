# CV Factory - 전문 이력서 빌더

<div align="center">
  <img src="logo.png" alt="CV Factory Logo" style="width:200px; height:auto;"/>
  <br>

  [![English](https://img.shields.io/badge/language-English-blue.svg)](README.md)
  [![코드 품질](https://img.shields.io/badge/SonarQube-A%20등급-brightgreen.svg)](http://localhost:9000/dashboard?id=frontend)
</div>

## 📖 개요
CV Factory는 AI 기반 지원으로 전문적인 이력서를 작성할 수 있도록 돕는 현대적인 풀스택 웹 애플리케이션입니다. Django 백엔드와 Svelte 프론트엔드로 구축되어 다국어 지원과 함께 직관적인 이력서 작성 인터페이스를 제공합니다.

## ✨ 주요 기능
- **현대적 프론트엔드**: TypeScript와 SvelteKit을 사용한 Svelte 5
- **견고한 백엔드**: REST API 기능을 갖춘 Django
- **다국어 지원**: svelte-i18n을 통한 한국어 및 영어 지원
- **반응형 디자인**: 현대적인 UI/UX를 갖춘 모바일 우선 접근법
- **코드 품질**: 버그 제로의 A등급 SonarQube 분석
- **Docker 지원**: 컨테이너화된 개발 및 배포
- **CI/CD 준비**: Northflank 배포 구성 완료

## 🛠 기술 스택

### 프론트엔드 (Svelte)
| 분류 | 기술 요소 |
|----------|--------------|
| 프레임워크 | Svelte 5, SvelteKit |
| 언어 | TypeScript |
| 빌드 도구 | Vite |
| 스타일링 | CSS3, 현대적 디자인 |
| 국제화 | svelte-i18n |
| 코드 품질 | ESLint, Prettier, TypeScript |

### 백엔드 (Django)
| 분류 | 기술 요소 |
|----------|--------------|
| 프레임워크 | Django |
| 데이터베이스 | SQLite (개발), PostgreSQL (프로덕션) |
| API | Django REST 기능 |
| 정적 파일 | Whitenoise |
| 보안 | Django CSP, CORS 헤더 |
| 배포 | Gunicorn, Docker |

### DevOps 및 품질
| 분류 | 기술 요소 |
|----------|--------------|
| 컨테이너화 | Docker, Docker Compose |
| 코드 분석 | SonarQube (A등급 품질) |
| 배포 | Northflank, Cloudflare |
| 환경 설정 | python-dotenv |

## 🚀 시작하기

### 필수 요구사항
- **Python 3.11+**
- **Node.js 18+** 및 npm
- **Docker** (선택사항, 컨테이너화된 개발용)
- **Git**

### 빠른 시작

1. **리포지토리 클론:**
   ```bash
   git clone https://github.com/CV-Factory/Frontend.git
   cd Frontend
   ```

2. **백엔드 설정 (Django):**
   ```bash
   # 가상 환경 생성
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   
   # 의존성 설치
   pip install -r requirements.txt
   
   # 마이그레이션 실행
   python manage.py migrate
   
   # Django 서버 시작
   python manage.py runserver
   ```

3. **프론트엔드 설정 (Svelte):**
   ```bash
   # client 디렉토리로 이동
   cd client
   
   # 의존성 설치
   npm install
   
   # 개발 서버 시작
   npm run dev
   ```

4. **애플리케이션 접속:**
   - 프론트엔드: `http://localhost:5173` (Vite 개발 서버)
   - 백엔드 API: `http://localhost:8000` (Django 서버)

### Docker 개발

완전한 컨테이너화된 설정을 위해:

```bash
# 모든 서비스 시작
docker compose up -d

# 로그 확인
docker compose logs -f

# 서비스 중지
docker compose down
```

## 📁 프로젝트 구조

```
Frontend/
├── client/                    # Svelte 프론트엔드
│   ├── src/
│   │   ├── routes/           # SvelteKit 라우트
│   │   ├── lib/              # 공유 컴포넌트 및 유틸리티
│   │   │   └── i18n/         # 국제화
│   │   └── app.html          # 메인 HTML 템플릿
│   ├── static/               # 정적 자산
│   ├── package.json          # 프론트엔드 의존성 및 스크립트
│   └── vite.config.ts        # Vite 구성
├── config/                   # Django 프로젝트 설정
│   ├── settings.py           # 메인 Django 설정
│   ├── urls.py               # URL 라우팅
│   └── wsgi.py               # WSGI 구성
├── core/                     # Django 핵심 애플리케이션
│   └── views.py              # API 뷰 및 로직
├── locale/                   # Django 번역
├── favicon_io/               # 파비콘 자산
├── docker-compose.yml        # 멀티 서비스 컨테이너 설정
├── Dockerfile                # 컨테이너 이미지 정의
├── requirements.txt          # Python 의존성
├── manage.py                 # Django 관리 스크립트
└── sonar-project.properties  # 코드 품질 구성
```

## 🔧 개발 명령어

### 프론트엔드 (`/client` 디렉토리에서)
```bash
npm run dev          # 개발 서버 시작
npm run build        # 프로덕션 빌드
npm run preview      # 프로덕션 빌드 미리보기
npm run check        # 타입 검사
npm run lint         # ESLint 분석
npm run lint:fix     # ESLint 문제 수정
npm run format       # Prettier로 코드 포맷팅
```

### 백엔드 (루트 디렉토리에서)
```bash
python manage.py runserver    # Django 서버 시작
python manage.py migrate      # 데이터베이스 마이그레이션 적용
python manage.py collectstatic # 정적 파일 수집
python manage.py test         # 테스트 실행
```

### 코드 품질
```bash
# SonarQube 분석 (SonarQube 서버 실행 필요)
docker compose up -d sonarqube  # SonarQube 시작
# 그 다음 프로젝트 루트에서 sonar-scanner 실행
```

## 🌐 다국어 지원

애플리케이션은 다음을 지원합니다:
- **영어** (기본값): `/`를 통해 접속
- **한국어**: `/ko/`를 통해 접속

언어 전환은 URL 라우팅과 사용자 기본 설정에 따라 자동으로 처리됩니다.

## 🐳 배포

### Northflank 배포
프로젝트는 다음과 함께 Northflank 배포용으로 구성되어 있습니다:
- `northflank.json` 구성
- Docker 기반 빌드
- 환경 변수 관리
- Cloudflare CDN 통합

### 수동 배포
```bash
# 프론트엔드 빌드
cd client && npm run build

# Django 정적 파일 수집
python manage.py collectstatic --noinput

# Gunicorn으로 실행
gunicorn config.wsgi:application
```

## 📊 코드 품질

이 프로젝트는 **A등급 코드 품질**을 유지합니다:
- ✅ **버그 0개**
- ✅ **취약점 0��** 
- ✅ **코드 스멜 0개**
- ✅ **A등급 신뢰성**
- ✅ **A등급 보안**
- ✅ **A등급 유지보수성**

품질은 다음을 통해 보장됩니다:
- SonarQube 정적 분석
- 프론트엔드용 ESLint 및 Prettier
- 타입 안전성을 위한 TypeScript
- 포괄적인 테스트 설정

## 🤝 기여하기

1. 리포지토리 포크
2. 기능 브랜치 생성 (`git checkout -b feature/amazing-feature`)
3. 변경사항 커밋 (`git commit -m 'Add amazing feature'`)
4. 브랜치에 푸시 (`git push origin feature/amazing-feature`)
5. Pull Request 열기

## 📄 라이선스
독점 소프트웨어 – 모든 권리 보유
(자세한 내용은 [LICENSE](LICENSE) 파일 참조)

## 📬 연락처
- **이메일**: wintrover@gmail.com
- **GitHub**: [CV-Factory/Frontend](https://github.com/CV-Factory/Frontend)

---
*Django + Svelte로 ❤️를 담아 제작*