news-comment analysis
=====================
website for auto crawling, data analysis project


## Crawler
- Naver / The New York Times news & comment data

- crawling 원칙에 따라 요청 횟수를 최소한으로 줄이기 위해 selenium 방식 -> 직접받아오는 방식으로 변경

## docker-compose
- version 3
- Flask, Nginx, Postgres

## 모듈관리
- Flask(blueprint)

## 설정값(Configuratrion) 관리
env_file 로 관리하다가

server(environment variable) -> Config -> docker-compose -> application(module)
방식으로 변경
