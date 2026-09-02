# 원페이지 앱 무인 공장 (One-Page Autonomous Factory SOP)

이 문서는 '원페이지 사이트(유틸리티 앱)'를 서브에이전트(Subagents) 멀티 시스템을 활용하여 100% 무인화로 기획, 개발, SEO 세팅, 배포, 마케팅하는 표준 작업 지침(SOP)입니다.

## 1. 핵심 원칙 (Context Injection)
서브에이전트가 백지상태에서 임의로 코딩(React 사용, 광고 누락 등 환각 현상)하는 것을 방지하기 위해, 총괄 디렉터(메인 에이전트)는 **반드시 각 에이전트를 호출(Invoke)할 때 `utility_app_blueprint.md`의 절대 규칙을 프롬프트에 강제로 주입**하여 통제해야 합니다.

## 2. 9-Agent 어벤져스 파이프라인
원페이지 제작 지시가 떨어지면, 다음 9명의 에이전트를 순차적/병렬적으로 투입하여 프로젝트를 완수합니다.

### Step 1: 💡 프로덕트 오너 (Product Owner)
- 역할: 돈 되는 아이디어 발굴 및 방향 설정(Tool vs Info).
- 검증: **백엔드 서버나 DB 없이, 깃허브 정적 페이지(HTML/JS)만으로 100% 구현 가능한지** 엄격하게 타당성 검토.

### Step 2: 🕵️ 경쟁사 분석가 (Competitor Analyst)
- 역할: 타겟 키워드 검색 후 상위 노출 중인 1~3위 사이트 벤치마킹.
- 검증: 경쟁사의 UI/UX 약점과 유저가 원하지만 빠져있는 정보(Content Gap) 리포트 작성.

### Step 3: 📊 SEO 기획자 (SEO PM)
- 역할: 분석 리포트를 바탕으로 경쟁사를 압살할 사이트 구조 설계.
- 검증: 롱테일 키워드를 겨냥한 서브 메뉴(Content Silo)와 내부 링크(Internal Linking) 구조 완벽 기획.

### Step 4: ✍️ SEO 카피라이터 (SEO Copywriter)
- 역할: 사람 냄새나는 텍스트 및 마이크로카피 작성.
- 검증: 서브 페이지에 들어갈 상세 가이드 문서 및 유저의 클릭을 유도하는 매력적인 버튼 문구(CTA) 작성.

### Step 5: 💻 프론트엔드 개발자 (Frontend Developer)
- 역할: 바닐라 JS 코딩 및 UI/UX 구현.
- 검증: 무거운 프레임워크 배제, 모바일 최적화, **애드센스/쿠팡 파트너스 명당 위치 절대 사수**. **[중요]** 카카오 API 키 발급이 필요한 외부 SDK 대신, 키 없이 100% 동작하는 표준 **Web Share API (`navigator.share`)**를 무조건 사용하여 무인화 흐름을 유지할 것.

### Step 6: 🎨 SEO & 에셋 디자이너 (Asset Manager)
- 역할: 시각 및 기술적 SEO 자산 생성.
- 검증: 파비콘 및 OG 이미지 생성. **`sitemap.xml`, RSS 피드(`feed.xml`), `robots.txt`** 자동 생성 및 연결. 구글 검색 상위 노출을 위한 **JSON-LD 구조화 데이터(Schema.org)** HTML 헤더 주입.

### Step 7: 🧐 QA 리뷰어 (QA Reviewer)
- 역할: 최종 산출물 품질 관리.
- 검증: 모바일 환경 레이아웃 깨짐 테스트, 규칙 준수 여부 신랄하게 비판 후 반려 또는 승인.

### Step 8: 🛠️ 데브옵스 / 배포 담당자 (DevOps Engineer)
- 역할: 깃허브 인프라 관리 및 최종 배포.
- 검증: 
  1. `gh` CLI를 통한 깃허브 저장소 자동 생성 및 Git Push.
  2. **[Pages 활성화]** 깃허브 페이지 호스팅은 기본이 Off 상태이므로, 반드시 `gh api`를 호출하여 Pages 호스팅 스위치를 원격으로 강제 On 시킬 것.
  3. **[Cloudflare 자동화]** 시스템 환경 변수의 `CLOUDFLARE_API_TOKEN`을 조회하여 회장님의 커스텀 도메인(예: `enjoy-onepage.com`)의 Zone ID를 파악하고, Cloudflare API로 CNAME(프록시 ON)을 자동 등록할 것.
  4. **[GitHub CNAME 연동]** 깃허브 저장소 루트에 `CNAME` 파일을 커밋하고, `gh api repos/{owner}/{repo}/pages`를 통해 cname 속성을 덮어씌울 것.

### Step 9: 📢 그로스 해커 (Growth Hacker)
- 역할: 배포 직후 초기 트래픽 폭발 유도.
- 검증: 네이버 지식인, 카페, Threads 등 타겟 커뮤니티에 '사람이 직접 추천하는 듯한' 자연스러운 바이럴 홍보 원고 3종 세트 작성 (네이버는 수동 업로드, 스레드는 봇 API 활용).
