# 🐈 우리 집 고양이의 입맛 분석을 통한 사료 추천 웹사이트, 마이펫푸드

🔗 www.mypetfood.kr

![image](https://img.shields.io/badge/python-3.8.10-blue) ![image](https://img.shields.io/badge/-pymongo-lightgrey) ![image](https://img.shields.io/badge/-mongodb-brightgreen) ![image](https://img.shields.io/badge/heroku-purple)

## 기획 의도
1년 2개월차 초보 집사인 저는 "고양이가 어릴 때 다양하게 먹여봐야 앞으로 평생 이것저것 잘 먹는다" 라는 조언을 듣고, 지난 1년간 다양한 사료를 사보았습니다. 하지만 고양이의 입맛은... 까다로웠습니다. 좋다는 사료는 왜 안먹는건지, 싼 사료는 잘 먹는데 이게 몸에 좋은 건지 안 좋은건지 알쏭달쏭한 집사는 일단 고양이의 입맛을 기록하기 시작했습니다. (A 참치캔 : 잘 먹음, B 칠면조 파우치 : 먹다 남김, C 치즈무스캔 : 입에도 안 댐)

## 사료 추천
마이펫푸드는 그렇게 쌓인 저희 고양이의 입맛 데이터와, 테스터로 참여해준 총 5마리 고양이의 입맛 데이터와 320여개의 고양이 사료 데이터를 바탕으로, 개별 고양이의 입맛을 ( 선호도 * 사료의 성분, 제조사, 이름 등에 들어가는 단어의 빈도수) 행렬로 만들어 전체 사료에 대한 dtm과의 코사인 유사도 기반으로, 가장 입맛과 유사한 사료를 추천해줍니다. 

## 사용 스택
Fastapi 기반을 웹앱을 구축하고, jinja2와 boostrap으로 사이트를 꾸몄습니다. mongodb를 사용하여 데이터를 불러오고 저장합니다. 배포는 heroku로 진행하고 미리 구매해둔 도메인을 연결했습니다. 
Fastapi를 사용한 이유는
- 성능이 뛰어나고 빠르다
- 배우기 쉽다
- 코드작업이 빠르다
- 에러가 적다
는 장점이 있었기 때문입니다. 

하지만 성능과 시간 면에서는 flask와 큰 차이를 느끼지 못했으며, 오히려 db와 쿼리 시 문법에 for문이 들어가 시간복잡도가 증가하는 경향이 있었습니다.
찾을 수 있는 샘플 코드도 flsk보다 덜 RESTful한 경우가 있고, 에러가 적은지도 체감상 크게 느끼지 못하였습니다. 최근 핫한 최신의 스택이라고 무조건 답이 아니라는 것도 알게 되었습니다. 
하지만 직접 부딪히며 오류와 문제를 해결해본 좋은 경험이 되었습니다.

## 화면

### 메인
<image src="https://user-images.githubusercontent.com/61692777/121760070-c4452a00-cb63-11eb-97e2-285908be6941.png" width="850">
- 고양이의 정보를 입력받습니다. (로그인과 유사)

### 사료 평가
<image src="https://blog.kakaocdn.net/dn/ds6bWa/btq7pfvRQtG/0ozmuzKYK0kIwvHp8kZ5Ak/img.png" width="850">
- 데이터베이스에 있는 사료들의 정보를 보고 고양이의 선호도를 입력할 수 있습니다.
- "선호도 입력" 버튼을 누르면 각각의 사료에 대한 고양이의 선호도를 입력할 수 있습니다. 이렇게 입력한 데이터는 "rating" 콜렉션에 저장됩닙다.
- "평가 후 추천받기" 버튼을 누르면 평가한 사료들을 기반으로 고양이의 입맛에 따른 추천 사료를 볼 수 있습니다. 

### 사료 추천
<image src="https://user-images.githubusercontent.com/61692777/121759894-e7230e80-cb62-11eb-9e7a-612bb4a01381.png" width="850">
- 이미 사료를 평가한 고양이들의 평가 정보 갯수와, 고양이별로 추천된 사료들을 확인할 수 있습니다.
<image src="https://user-images.githubusercontent.com/61692777/121759940-1cc7f780-cb63-11eb-8881-c70489f39c92.png" width="850">
- 개별 고양이의 입맛을 바탕으로 10개 사료를 추천합니다.

### 검색
정규식을 사용하여, 키워드로 검색이 가능하게 구현하였습니다.
<image src="https://user-images.githubusercontent.com/61692777/121759982-4f71f000-cb63-11eb-848e-4f1fa57e6303.png" width="850">

