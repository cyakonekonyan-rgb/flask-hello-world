# -*- coding: utf-8 -*-

from flask import Flask, request, Response
import json

app = Flask(__name__)

# ============================================================
# Alexa からの POST リクエストを受け取り、正しい JSON 形式で返す
# ============================================================

@app.route('/', methods=['POST'])
def alexa_webhook():
    try:
        data = request.get_json(force=True)
    except:
        return alexa_response("JSON を取得できませんでした。")

    # デバッグ用
    print("=== Alexa Request ===")
    print(json.dumps(data, indent=2, ensure_ascii=False))

    # スキル起動（LaunchRequest）
    if data["request"]["type"] == "LaunchRequest":
        return alexa_response("でんすけせんせいを起動しました。何をしますか？")

    # IntentRequest
    if data["request"]["type"] == "IntentRequest":
        intent = data["request"]["intent"]["name"]

        if intent == "HelloIntent":
            return alexa_response("こんにちは、私はでんすけせんせいです。")

        # 未対応のインテント
        return alexa_response("その機能にはまだ対応していません。")

    # その他
    return alexa_response("リクエストを理解できませんでした。")


# ============================================================
# Alexa が要求する形式でレスポンスを返す関数
# Flask の jsonify は Alexa に不向きなので Response を使用
# ============================================================

def alexa_response(text):
    body = {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": text
            },
            "shouldEndSession": False
        }
    }

    json_text = json.dumps(body, ensure_ascii=False)

    return Response(
        json_text,
        status=200,
        mimetype='application/json'
    )


# ============================================================
# 動作確認用 GET
# ============================================================

@app.route('/', methods=['GET'])
def root():
    return "Alexa Flask server is running."

# ============================================================

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
