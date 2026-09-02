# Total System Dashboard

원페이지 팩토리 시스템 전체를 통합 관리하고 모니터링하는 메인 관제 저장소입니다.

## 📂 폴더 구조 (Directory Structure)

- **/monitoring/**
  - onepage_office.html : 2D 가상 오피스 기반 실시간 모니터링 웹 대시보드
  - onepage_status.json : 에이전트 작업 상태가 기록되는 데이터 파일 (60초 단위 갱신)
  - sync_office_monitor.py : 로컬 로그를 분석하여 상태를 업데이트하고 GitHub에 Push하는 데몬 스크립트

- **/rules/**
  - rchitecture_rules.md : 시스템 구조 및 배포 원칙 (무서버, GitHub Pages 등)
  - seo_guidelines.md : 검색엔진 최적화 및 법적 필수 페이지(약관 등) 가이드라인
  - ui_ux_standards.md : Tailwind CSS 및 UI 레이아웃 표준 규칙

