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

#### 점수 등록(+1, -1)

> /score 이소연 +1
> 

> /score 이소연 -1
> 

**<결과>**


<img width="273" alt="image" src="https://github.com/user-attachments/assets/4cf249c1-dee4-4f95-ac90-e6af49d58e2c" />



#### 점수 초기화

> /score init
> 


**<결과>**


<img width="380" alt="image" src="https://github.com/user-attachments/assets/d1774a78-80e6-4ed5-99f5-54085dbefc28" />


#### 총점 조회

> /score
> 

**<결과>**

<img width="195" alt="image" src="https://github.com/user-attachments/assets/f6f15866-ba84-4791-8b79-e1954cbd18e5" />

#### 명령어를 잘못 입력했을 때

**<결과>**

<img width="387" alt="image" src="https://github.com/user-attachments/assets/ad7f37b5-5ed8-4127-a26f-97f986d4ff7e" />

## 3. v2 기능
- 문제도 등록하거나 취소할수 있도록 구현
- 잘못 입력한 사람 이름 날릴수있게 구현
