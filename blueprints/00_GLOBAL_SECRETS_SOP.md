# 🔐 Global Secrets Management (전사 공통 보안 설정)

본 관제 리포지토리(total-system-dashboard)는 자동화 공장 전체에서 공통으로 사용되는 핵심 API 키와 민감 정보를 중앙에서 관리합니다.

## 📍 중앙 관리 파일 위치
- 파일명: \global_secrets.env\ (루트 디렉토리 위치)
- **보안 주의**: 이 파일은 절대 깃허브에 Push되어서는 안 되며, \.gitignore\에 의해 로컬에만 안전하게 보관됩니다.

## 🔑 등록된 공통 키 목록
\global_secrets.env\ 파일 안에는 다음의 공통 변수들이 저장되어 있습니다:

1. **GEMINI_GLOBAL_KEY** 
   - 용도: AI 원고 작성, 로직 생성 등 모든 Gemini AI 호출 공통 키
   - (참고: 모델 호출 시 허용된 3.X Flash 및 Lite 모델만 사용할 것)
2. **CLOUDFLARE_GLOBAL_TOKEN**
   - 용도: 원페이지 사이트 및 블로그의 서브도메인 DNS 레코드 자동 등록
3. **ADSENSE_PUB_ID**
   - 용도: 공장(Factory)에서 생성되는 모든 사이트/블로그에 부착할 공통 애드센스 ID (pub-xxxx)

## 🤖 에이전트 행동 지침 (Agent Rules)
1. 새로운 자동화 봇이나 스크립트를 생성할 때, API 키를 스크립트 안에 하드코딩(Hardcoding)하지 마십시오.
2. 스크립트 실행 시 \	otal-system-dashboard/global_secrets.env\ 경로를 참조하여 키를 동적으로 불러오도록(Load) 설계하십시오.
3. 작업 내역을 마크다운이나 로그로 사용자(회장님)에게 보고할 때, **실제 키 값(Plain text)이 노출되지 않도록 마스킹 처리(예: \AIzaSy...\)**를 철저히 하십시오.
