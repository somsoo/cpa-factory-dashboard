# 🟢 네이버 블로그 설계도 (Naver Blog Blueprint)

- **페르소나:** (카테고리별 맞춤 정보 제공자)
- **모델 분배 (핵심):** 글쓰기, 검사, 수정 과정에서 Flash-Lite와 Flash 모델을 교차 사용하여 API 한도(Quota) 방어.

## 1. 키워드 발굴 방식 (NCP & Search Ad API)
1. **카테고리별 실시간 뉴스 수집:** NCP News API를 통해 지정된 타겟 카테고리(유연하게 확장 및 변경 가능)의 실시간 뉴스를 수집.
2. **토픽 추출:** 제미나이가 뉴스를 분석하여 카테고리별로 5개의 토픽 추출.
3. **황금 키워드 발굴:** 추출된 토픽을 '네이버 검색광고 API'에 던져, 경쟁도는 낮고 검색량은 높은 황금 키워드 추출.
4. **중복 검증:** posted_history.txt를 대조하여 중복 방지.

## 2. 배포 인프라 (수동 업로드 전처리)
- **자동 배포 안 함:** 네이버는 API 자동 배포나 깃허브 페이지 자동 연동을 사용하지 않습니다.
- **폴더 자동 생성:** Git 레포지토리 내에 [날짜]/[키워드] 형식으로 폴더를 자동 생성합니다.
- **이미지 소싱 및 결과물 저장:** 픽사베이(Pixabay) API를 통해 키워드에 맞는 무료 스톡 이미지를 다운로드하고, 해당 폴더 안에 **HTML 원고**와 **이미지 파일**들을 함께 저장해 둡니다.
- **최종 업로드:** 유저가 해당 폴더의 HTML과 이미지를 복사하여 네이버 블로그에 **수동으로 직접 업로드**합니다.

## 4. 수익화 방식
- **애드센스 불가:** 네이버 블로그는 애드센스 삽입이 불가능하므로, 플랫폼 자체 광고(애드포스트) 또는 별도 제휴 링크 삽입으로 대체.

## 5. 2-Track Hybrid Framework (Concept + Fact)
- **Objective:** Fulfill both the 'concept search intent' and 'latest news search intent' to maximize dwell time (SEO) and prevent hallucinations.
- **[Chapter 1] Basic Concept Dictionary:** Use Gemini's inherent knowledge to easily explain the keyword's basic meaning and definition for beginners (e.g., What is FAR?).
- **[Chapter 2] Latest Issue Fact-Check:** Inject (RAG) the scraped 'raw news article (Context)' into Gemini to summarize the latest trends and outlook based ONLY on news facts, without forcibly injecting unrelated high-CPC keywords (e.g., loans).
- **Persona Control:** Do not use personas (e.g., '30s office worker') to distort news facts. Separate the persona and apply it only at the very end of the post as a 'personal review or thought'.

## 6. 에버그린(Evergreen) 키워드 3중 필터링 시스템
- **목적:** 퀴즈, 운세 등 수명이 짧고 블로그 지수를 갉아먹는 일회용 키워드를 원천 차단하고 장기 트래픽을 유발하는 고품질 명사만 추출.
- **[1단계] 표본 확대:** NCP 뉴스 API 호출 시 헤드라인을 15개에서 100개로 대폭 늘려 단기 어그로 기사의 비중을 희석시킴.
- **[2단계] 네거티브 프롬프팅:** 제미나이 추출 시, 퀴즈, 캐시워크 같은 단발성 키워드를 강제로 배제하고 에버그린 명사만 뽑도록 지시.
- **[3단계] 파이썬 하드 블랙리스트:** 코드 내 배열(퀴즈, 정답, 비트버니 등)을 통해 스팸 단어가 포함되면 강제로 폐기함.
