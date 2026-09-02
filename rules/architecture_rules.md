# Architecture & Deployment Rules (OnePage Factory)

1. **무서버(Serverless) 원칙**: 백엔드 서버(Node.js, Python 등)나 데이터베이스(MySQL 등)를 절대 사용하지 않습니다.
2. **정적 호스팅**: 모든 서비스는 HTML, CSS, Vanilla JS만으로 구성하여 GitHub Pages로 100% 무료 배포합니다.
3. **로직 독립성**: 타사 유료 API에 의존하지 않는 독립적인 계산기/변환기 기능 위주로 기획합니다.
