# Slack Score Bot
## 1. 슬랙 앱 생성

- slack api 사이트 접속
- create new app → from scratch
- 앱이름 + 워크스페이스 지정
- 앱 생성 후 “slash commands” 기능 추가
    - 명령어 : (예) /score
    - request URL :  (예)(ngrok주소)/slack/score
 

### 📡 외부 요청 처리를 위한 ngrok
슬랙에서 Flask 서버로 요청을 보려면 public URL이 있어야 하니, ngrok을 아래처럼 켜두면 됩니다:


ngrok http 3000
슬랙 Slash Command에 https://abcd1234.ngrok.io/slack/score 이렇게 등록하면 OK.

### flask 실행
python app.py


## 2. v1 기능

### 점수 등록(+1, -1)

> /score 이소연 +1
> 

> /score 이소연 -1
> 

**<결과>**


<img width="273" alt="image" src="https://github.com/user-attachments/assets/4cf249c1-dee4-4f95-ac90-e6af49d58e2c" />



### 점수 초기화

> /score init
> 


**<결과>**


<img width="380" alt="image" src="https://github.com/user-attachments/assets/d1774a78-80e6-4ed5-99f5-54085dbefc28" />


### 총점 조회

> /score
> 


<img width="195" alt="image" src="https://github.com/user-attachments/assets/f6f15866-ba84-4791-8b79-e1954cbd18e5" />

### 명령어를 잘못 입력했을 때

<img width="1029" alt="image" src="https://github.com/user-attachments/assets/da193ab0-7319-41f1-b8df-5edefb1dddc8" />


## 3. v2 기능
- 문제도 등록하거나 취소할수 있도록 구현
- 잘못 입력한 사람 이름 날릴수있게 구현

### 도움말 기능

<img width="607" alt="image" src="https://github.com/user-attachments/assets/1131f617-d0f9-44b8-8699-34cc0bd3cf1b" />

### 문제 등록

<img width="254" alt="image" src="https://github.com/user-attachments/assets/bccd6500-48cb-488d-91a5-5c3a403d2efd" />

### 문제 삭제

<img width="411" alt="image" src="https://github.com/user-attachments/assets/e7d7dffe-ea19-4b43-875d-f5d0c4b64682" />

### 문제 조회

<img width="490" alt="image" src="https://github.com/user-attachments/assets/2f6820a9-9406-4ecb-bed5-3941d234b5f4" />

### 잘못 입력한 사람 이름 삭제

<img width="389" alt="image" src="https://github.com/user-attachments/assets/0643e29c-ea48-41b9-a2aa-aa17c3f8a209" />

### 기타 변경점
- +1, -1 이 아닌 자유롭게 올리고 내릴수 있음
- 아무 이름이 아닌 @닉네임으로 점수를 등록해서 중복 방지

## 4. v3 기능
- 문제가 두줄이상 일 경우 처리안됨. 
