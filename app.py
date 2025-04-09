from flask import Flask, request
from collections import defaultdict
from dotenv import load_dotenv
import os
import requests

load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

app = Flask(__name__)

scores = defaultdict(lambda: defaultdict(lambda: {"score": 0}))
problems = defaultdict(list)

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
