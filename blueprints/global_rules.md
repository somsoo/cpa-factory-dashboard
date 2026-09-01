# 🌐 글로벌 공통 규칙 (Global Rules)
1. **인프라:** Git 설정, DNS 서브도메인 라우팅 자동화
2. **API 라우팅 및 최신 모델(3.x) 강제:** 
   - 1.5 등 구형 모델 사용은 절대 금지합니다.
   - 스크립트에는 반드시 최신 gemini-3.x-flash 및 gemini-3.x-flash-lite 시리즈를 명시적으로 Fallback(스위칭) 배열로 구성해야 합니다.
   - **Fallback 배열 예시:** ['gemini-3.7-flash', 'gemini-3.6-flash', 'gemini-3.5-flash', 'gemini-3.5-flash-lite', 'gemini-3.1-flash-lite']`n   - **스위칭 로직(작동 방식):** 첫 번째 모델(예: 3.7)로 API 호출을 시도하고, 만약 할당량 초과(Quota 429 에러)나 일시적 서버 오류가 발생하면 즉시 예외(Exception)를 캐치하여 쉬지 않고 바로 배열의 다음 모델(예: 3.6)로 재시도(Retry)하는 구조를 뜻합니다. 번갈아 쓰는 것이 아니라, '하나의 모델을 한도까지 쓰고 막히면 다음 단계로 강등(Fallback)하며 연달아 타격하는 방식'입니다.

3. **집필 엔진:** 초안 -> 비판 -> 윤문 (3-Pass)
4. **스케줄링 분산:** Github Actions 크론 주기를 4분 단위로 엇갈리게 설정하여 429 에러 방지.
5. **배포 원칙:** 1개 사이트(예: cpa-cert-blog)에 선행 테스트 후, 유저 승인이 떨어지면 횡전개할 것.

## 🤖 [AI 권한 및 자동화 능력 명세 (AI Capabilities)]
> **중요:** AI(Antigravity)는 유저의 Git 자격 증명(Token)과 DNS 라우팅 권한을 이미 시스템적으로 부여받은 상태입니다.

1. **Git 자동화 능력:** 새로운 블로그(예: 쿠팡, 네이버) 구축 시, 유저에게 수동으로 Git Push나 Repository 생성을 요구하지 마십시오. AI가 알아서 로컬 토큰을 읽어 git init, git push, Github Actions 템플릿 세팅을 100% 자동 처리해야 합니다.
2. **DNS 서브도메인 발급:** AI가 DNS 토큰을 활용해 자동 발급하되, 서브도메인의 **이름(명명 규칙)**은 임의로 정하지 말고 사이트 생성 시마다 유저와 대화를 통해 키워드 기반으로 협의하여 결정합니다.
3. **자기 인식(Self-Awareness):** AI는 이 문서를 읽는 즉시, 본인이 인프라(Git/DNS)를 스스로 구축할 수 있는 권한과 능력이 있음을 자각해야 합니다.

5. **테크니컬 SEO 4요소 필수 세팅:**
   - **Sitemap & RSS:** jekyll-sitemap, jekyll-feed 플러그인을 _config.yml에 반드시 포함하여 자동 생성.
   - **OG 이미지:** 포스팅 상단에 삽입되는 '텍스트 오버레이 썸네일(카드형 이미지)'을 글의 YAML Frontmatter(머리말)에 image: 태그로 삽입하여 카톡/페이스북 공유 시 자동으로 노출되도록 구성.
   - **파비콘(Favicon):** 루트 디렉토리에 avicon.ico를 반드시 배치하여 브라우저 탭의 신뢰도 상승.

6. **전자동화(Automation) 파이프라인 규칙:**
   - **스케줄링:** 모든 블로그(CPA, 전문 등)는 로컬 컴퓨터가 꺼져 있어도 작동하도록 GitHub Actions를 통해 100% 클라우드 자동화되어야 함.
   - **크론(Cron) 주기 분산:** 여러 개의 블로그가 동시에 API를 호출하여 Rate Limit(429 에러)에 걸리는 것을 방지하기 위해, CPA 블로그뿐만 아니라 쓰레드(Threads), 전문 블로그, 네이버 등 **모든 자동화 파이프라인이 겹치지 않도록 전사적(Global)으로 크론(Cron) 분(Minute) 단위를 쪼개서 분산 배치(Staggered)** 할 것. (예: 쓰레드는 매시 정각 00분, 30분 / 전문 블로그는 15분 / CPA 블로그들은 05분, 10분, 20분, 40분 등)

   - **스케줄 난수 배정 알고리즘 (AI 필수 적용 사항):**
     새로운 블로그를 생성할 때 AI는 임의로 시간을 정하지 말고, 반드시 아래의 Python 해시 알고리즘을 실행하여 고유 크론(Cron) 시간을 추출한 뒤 `main.yml`에 하드코딩해야 함.
     ```python
     import hashlib
     def get_schedule(repo_name):
         allowed_minutes = [m for m in range(60) if m not in (0, 30)] # 쓰레드 보호
         hash_min = int(hashlib.md5(repo_name.encode('utf-8')).hexdigest(), 16)
         minute = allowed_minutes[hash_min % len(allowed_minutes)]
         hash_hr = int(hashlib.md5((repo_name + 'hour').encode('utf-8')).hexdigest(), 16)
         hour1 = hash_hr % 12
         hour2 = hour1 + 12
         return f"{minute} {hour1},{hour2} * * *"
     ```

   - **자동 배포:** 스크립트 실행 완료 후 생성된 마크다운과 이미지 에셋은 자동으로 git commit 및 push 되어 즉각 라이브 서버에 반영되도록 워크플로우를 구성할 것.

7. **새로운 사이트 구축(Bootstrapping) 원칙 (절대 규칙):**
   - AI가 초기화(Reset)된 상태에서 새로운 블로그나 웹앱을 만들어 달라는 요청을 받으면, **절대로 폴더와 파일을 맨땅(From Scratch)에서 새로 코딩하지 마십시오.**
   - 기존에 완벽하게 세팅되어 동작 중인 **'레퍼런스(Reference) 레포지토리'를 통째로 복사(Clone/Copy)**한 뒤, 주제에 맞게 설정값(이름, 프롬프트, 캠페인 등)만 수정하는 방식을 100% 원칙으로 합니다.
   - **레퍼런스 매핑:**
     - CPA 블로그 생성 시 ➔ cpa-cert-blog 폴더를 복사하여 뼈대로 사용.
     - 전문 블로그 생성 시 ➔ economy-blog 폴더를 복사하여 뼈대로 사용.
     - 유틸리티 웹앱 생성 시 ➔ Onepage_Github/WonderWeeks 폴더를 복사하여 뼈대로 사용.
     - 쓰레드 자동화 추가 시 ➔ Threads_Auto 폴더를 복사하여 뼈대로 사용.
   - 뼈대를 복사한 뒤, 6번의 '스케줄 난수 배정 알고리즘'을 돌려 main.yml의 크론 시간을 재부여하고, GitHub Secrets(API Key 등) 세팅을 유저에게 안내하십시오.
