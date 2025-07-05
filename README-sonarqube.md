# SonarQube 로컬 분석 가이드

## 사전 준비
1. SonarQube 서버 실행
   ```bash
   docker compose up -d sonarqube
   ```

2. SonarScanner CLI 설치
   ```bash
   # Windows (Chocolatey)
   choco install sonarscanner
   
   # macOS (Homebrew)
   brew install sonar-scanner
   
   # Linux (수동 설치)
   wget https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-5.0.1.3006-linux.zip
   unzip sonar-scanner-cli-5.0.1.3006-linux.zip
   export PATH=$PATH:/path/to/sonar-scanner/bin
   ```

## 분석 실행
프로젝트 루트에서 다음 명령어 실행:

```bash
sonar-scanner \
  -Dsonar.projectKey=CV-Factory_Frontend_7d986e4d-207a-4b0f-bf7f-ec8e725723c5 \
  -Dsonar.sources=client,core \
  -Dsonar.host.url=http://localhost:9000 \
  -Dsonar.login=<YOUR_SONAR_TOKEN>
```

## 토큰 생성
1. SonarQube UI (http://localhost:9000) 접속
2. 우상단 프로필 → My Account → Security
3. "Generate Tokens" → 이름 입력 → Generate
4. 생성된 토큰을 위 명령어의 `<YOUR_SONAR_TOKEN>` 부분에 입력

## 분석 결과 확인
- SonarQube UI → Projects → Frontend 프로젝트에서 결과 확인
- 코드 품질, 버그, 보안 취약점, 중복 코드 등 분석 리포트 제공