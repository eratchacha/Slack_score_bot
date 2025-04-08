import os
import requests
from flask import Flask, request
from collections import defaultdict
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
scores = defaultdict(lambda: defaultdict(int))
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")

def send_channel_message(channel_id, text):
    headers = {
        "Authorization": f"Bearer {SLACK_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    data = {
        "channel": channel_id,
        "text": text
    }
    response = requests.post("https://slack.com/api/chat.postMessage", json=data, headers=headers)
    print("[Slack 응답]", response.status_code, response.json())  # 👉 이거 추가


@app.route('/slack/score', methods=['POST'])
def handle_score():
    channel_id = request.form.get('channel_id')
    text = request.form.get('text', '').strip()
    sender_id = request.form.get('user_id')

    print(f"[DEBUG] text: {text}")

    if text == "init":
        scores[channel_id].clear()
        send_channel_message(channel_id, f"<@{sender_id}> 님이 점수를 초기화했습니다.")
        return "", 200

    elif text == "":
        if not scores[channel_id]:
            send_channel_message(channel_id, "아직 아무도 점수가 없습니다.")
            return "", 200
        sorted_scores = sorted(scores[channel_id].items(), key=lambda x: -x[1])
        result = "\n".join([f"{name}: {score}점" for name, score in sorted_scores])
        send_channel_message(channel_id, result)
        return "", 200

    else:
        parts = text.split()
        if len(parts) != 2:
            send_channel_message(channel_id, "형식: /score 이름 +1 또는 /score 이름 -1")
            return "", 200

        name, delta_str = parts
        if delta_str not in ("+1", "-1"):
            send_channel_message(channel_id, "잘못된 형식입니다. 이름과 +1/-1을 사용하세요.")
            return "", 200

        delta = int(delta_str)
        scores[channel_id][name] += delta
        new_score = scores[channel_id][name]
        send_channel_message(channel_id, f"{name}의 점수는 이제 {new_score}점입니다.")
        return "", 200

if __name__ == '__main__':
    app.run(port=3000)
