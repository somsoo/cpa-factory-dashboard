# 🌐 One-Page Factory 커스텀 도메인 정책

1. **루트 도메인 (Root Domain)**: enjoy-onepage.com
2. **서브도메인 명명 규칙**: 각 웹앱의 깃허브 리포지토리 이름(repo_name)을 서브도메인으로 사용.
   - 예시: 리포지토리가 esume-text-counter인 경우 -> esume-text-counter.enjoy-onepage.com
3. **CNAME 자동화 필수**: 모든 신규 리포지토리 생성 시, 반드시 루트 폴더에 위 서브도메인 주소가 적힌 CNAME 파일을 1순위로 생성 및 커밋할 것.
4. **목적**: 구글 애드센스(Google AdSense) 신규 사이트 승인 및 광고 송출을 위한 필수 조건.
