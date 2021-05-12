## 프로젝트 소개
React를 사용한 '여기어때' 웹사이트를 모티브로 한 프로젝트
## 프로젝트 기간
- 2021.04.26~2021.05.07
## FrontEnd
- 김효진, 박단비, 박성은
## BackEnd
- 백승찬, 신지원, 황수민
## 기술 스택
- FrontEnd
  ![HTML/CSS](https://img.shields.io/badge/-HTML/CSS-E44D26)
  ![JavaScript(ES6+)](<https://img.shields.io/badge/-JavaScript(ES6%2B)-F0DB4D>)
  ![React](https://img.shields.io/badge/-React-blue)<br>
  React Router<br>
  Styled-component
- BackEnd
- Python, Django, bcrypt, pyjwt, unittest, MySQL, AqueryTool, AWS EC2, AWS RDS, AWS S3, Docker
## 협업 도구
- ![Slack](https://img.shields.io/badge/-Slack-D91D57)
- ![Git](https://img.shields.io/badge/-Git-black)
- ![Trello](https://img.shields.io/badge/-Trello-036AA7)
## 구현 내용 
## FrontEnd
**김효진** <br>
### 로그인 & 회원가입
- 반복되는 input에 component를 사용하여 회원가입 페이지 구현.
- useState와 validator 조건문 선언을 사용한 회원가입 경고문 표시.
- 쿼리스트링을 사용하여 서버에 인증번호 주소 전송
- 로그인 & 회원가입 access_token 을 이용한 유효성 검사
- 회원가입 완료 시 환영 메세지 모달 창 등장.
- 카카오API를 이용한 소셜 로그인 연동
- 레이아웃/소셜 로그인 시(토큰 유무에 따른) nav bar 카카오톡 이름(닉네임), 예약내역 표시
**박단비** <br>
### 메인 페이지
- 메인페이지, 리스트페이지/에어비앤비 캘린더Library 활용 및 레이아웃 구현
- 메인 페이지, 리스트 페이지/ Query String을 사용한 통신 (숙박유형, 지역, 날짜, 인원수 선택) 에 따른 filtering
### 숙박 리스트 페이지
- 필터링된 호텔 리스트 추천순, 평점순, 가격순, 성급별 sorting
- 리스트 페이지 호텔별 성급, 리뷰에 따른 코멘트 라벨 컴포넌트화
- 날짜, 인원 재검색에 따른 결과 표시

**박성은** <br>
### 숙박 상세 페이지
- 호텔 상세페이지 레이아웃/카카오지도 API에 활용 및 숙박지도표시
- 필터링된 룸 타입에 따른 숙박예약
- S3를 이용한 사용자 예약여부에 따른 리뷰쓰기/리뷰등록
### 숙박 예약 페이지, 예약 확인 페이지
- Query Parameter로 숙박 정보 받기/숙박 예약하기
- 예약내역 확인/ 리뷰등록 후 예약완료에서 숙박완료로 라벨 변화
## BackEnd
**백승찬**

'users'
- 일반 로그인 기능 구현
-일반 회원가입 기능 구현
-회원가입 시 핸드폰 인증(네이버 클라우드) 기능 구현
-unittest 완료
'reviews'
- AWS(S3) 이용한 사진 업로드, 댓글, 별점 등록 기능 구현
-호텔 별 등록된 리뷰 보여주기 기능 구현
- 사용자가 등록한 리뷰 삭제 기능 구현
-unittest 완료

**신지원**

'users'
- 카카오 소셜 로그인 기능 구현
-  mock 과 patch 사용해서 unittest 완료

'reservations'
- 호텔 예약하면 status 바꿔주고, 예약 테이블에서 해당 날짜의 방의 잔여 갯수 1씩 빼주도록 구현
- 예약하거나 취소한 호텔들 리스트 데이터 전달
- 예약 취소하면 status 바꿔주고, 예약 테이블에서 해당 날짜의 방의 잔여 갯수 1씩 더해주도록 구현
- unittest 완료

**황수민**

'hotels'
- CategoryLocationView: 메인 페이지 Category, Location, image 데이터 전달
- HotelView: 리스트 페이지 Query parameter 사용하여 필터링된 호텔 데이터 전달, 검색기능 구현
- HotelDetailView: 디테일 페이지 Path parameter, Query parameter 사용하여 필터링된 호텔 룸 데이터 전달
- unittest 완료

## 프로젝트 후기
김효진 : https://velog.io/@jinjinhyojin<br>
박단비 : https://velog.io/@itssweetrain<br>
박성은 : https://velog.io/@elena_park<br>
백승찬 : https://velog.io/@chan_baek<br>
신지원 : https://velog.io/@jxxwon<br>
황수민 : https://velog.io/@z132305


-------------------
## ✔︎ References
이 프로젝트는 여기어때를 참고하여 학습용으로 작업 되었습니다.
이 프로젝트에서 사용된 모든 이미지는 Unsplash 에서 가져왔습니다.
