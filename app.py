from flask import Flask, request
from collections import defaultdict
from dotenv import load_dotenv
import os
import requests
import random

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

app = Flask(__name__)

scores = defaultdict(lambda: defaultdict(lambda: {"score": 0}))
problems = defaultdict(list)

# 문제 정답을 담는 배열
answers = defaultdict(list)

# 응원 메세지
messages = [
    "오늘도 잘하고 있어요! 조금만 더 힘내요 💪",
    "당신의 노력은 분명 빛을 발할 거예요 ✨",
    "조금 느려도 괜찮아요, 계속 나아가고 있다는 게 중요해요 🚶‍♂️🚶‍♀️",
    "힘들 땐 잠시 쉬어가도 돼요. 당신은 충분히 잘하고 있어요 🌿",
    "당신을 응원하는 사람이 여기 있어요! 파이팅! 🙌"
]


def post_message(channel, text):
    res = requests.post(
        "https://slack.com/api/chat.postMessage",
        headers={
            "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
            "Content-Type": "application/json"
        },
        json={
            "channel": channel,
            "text": text
        }
    )
    print("[슬랙 응답]", res.json())

@app.route('/slack/score', methods=['POST'])
def handle_score():
    channel_id = request.form.get('channel_id')
    text = request.form.get('text', '').strip()
    sender_id = request.form.get('user_id')

    if text == "-h":
        post_message(channel_id, """[사용 가능한 명령어 목록]
/score <@유저> +3 or -2    → 점수 변경
/score 이름 +3 or -2       → 일반 이름도 가능
/score                    → 전체 점수 확인
/score init               → 점수 초기화
/score bye "<@유저>" 또는 "이름" → 사용자 삭제
/score -a [문제 내용]     → 문제 등록
/score -aa [문제 내용] [정답]   → 문제, 정답 등록
/score -c [문제 번호] [정답] → 문제 풀기
/score problem            → 문제 목록 출력
/score -r [번호]          → 문제 삭제
/score -h                 → 이 도움말 보기""")
        return "", 200

    if text == "init":
        scores[channel_id].clear()
        post_message(channel_id, f"<@{sender_id}> 님이 점수를 초기화했습니다.")
        return "", 200

    if text == "problem":
        if not problems[channel_id]:
            post_message(channel_id, "등록된 문제가 없습니다.")
        else:
            result = "\n".join([f"{i+1}. {q}" for i, q in enumerate(problems[channel_id])])
            post_message(channel_id, f"[문제 목록]\n{result}")
        return "", 200

    if text.startswith("-a "):
        question = text[len("-a "):].strip()
        problems[channel_id].append(question)
        post_message(channel_id, f"문제가 등록되었습니다: {question}")
        return "", 200
    
    # 문제와 정답 모두 등록하기
    if text.startsWith("-aa "):
        tokens =  text[len("-aa ")].split()
        if tokens[0] == "-aa" and len(tokens) >= 3:
            problems[channel_id].append(tokens[1])
            answers[channel_id].append(tokens[2])
        else:
            print("형식이 올바르지 않습니다.")
    
    # 정답 확인하기        
    if text.startsWith("-c "):
        tokens =  text[len("-aa ")].split()
        if tokens[0] == "-aa" and len(tokens) >= 3:
            if answers[tokens[1]] == tokens[2]:
                print("정답!")
                # 문제 정답자 점수 자동 증가 로직
            else:
                print("오답!")
        else:
            print("형식이 올바르지 않습니다.")
    
    if text == "cheer":
        print("ChatGPT의 응원")
        print(random.choice(messages))       

    if text.startswith("-r "):
        try:
            index = int(text[len("-r "):].strip()) - 1
            removed = problems[channel_id].pop(index)
            post_message(channel_id, f"문제가 삭제되었습니다: {removed}")
        except:
            post_message(channel_id, "문제 번호가 잘못되었습니다.")
        return "", 200

    if text.startswith("bye "):
        name = text[len("bye "):].strip().strip('"')
        if name in scores[channel_id]:
            del scores[channel_id][name]
            post_message(channel_id, f"{name} 님의 점수가 삭제되었습니다.")
        else:
            post_message(channel_id, f"{name} 님은 등록되어 있지 않습니다.")
        return "", 200

    if text == "":
        if not scores[channel_id]:
            post_message(channel_id, "아직 아무도 점수가 없습니다.")
        else:
            sorted_scores = sorted(scores[channel_id].items(), key=lambda x: -x[1]["score"])
            result = "\n".join([f"{name}: {data['score']}점" for name, data in sorted_scores])
            post_message(channel_id, result)
        return "", 200

    # 점수 조작
    parts = text.split()
    if len(parts) != 2:
        post_message(channel_id, "형식: /score <@유저> +3 또는 /score 이름 -2")
        return "", 200

    target, delta_str = parts
    if not (delta_str.startswith("+") or delta_str.startswith("-")):
        post_message(channel_id, "형식: +숫자 또는 -숫자 만 가능합니다.")
        return "", 200

    try:
        delta = int(delta_str)
    except:
        post_message(channel_id, "숫자 형식이 잘못되었습니다.")
        return "", 200

    if target.startswith("<@") and target.endswith(">"):
        name = target
    else:
        name = target

    scores[channel_id][name]["score"] += delta
    new_score = scores[channel_id][name]["score"]

    post_message(channel_id, f"{name} 님의 점수는 이제 {new_score}점입니다.")
    return "", 200

if __name__ == '__main__':
    app.run(port=3000)
