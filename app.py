from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/', methods=['POST'])
def alexa_webhook():
    """ Alexa からのリクエストを受け取って返答する """

    data = request.get_json()

    # LaunchRequest（「開いて」で起動）
    if data["request"]["type"] == "LaunchRequest":
        return jsonify(build_response("でんすけせんせいを起動しました。何をしますか？"))

    # IntentRequest
    if data["request"]["type"] == "IntentRequest":
        intent = data["request"]["intent"]["name"]
        
        if intent == "HelloIntent":
            return jsonify(build_response("こんにちは、私はでんすけせんせいです。"))

        return jsonify(build_response("その機能にはまだ対応していません。"))

    return jsonify(build_response("リクエストを理解できませんでした。"))

def build_response(text):
    """ Alexa の JSON レスポンスを作成 """
    return {
        "version": "1.0",
        "response": {
            "outputSpeech": {
                "type": "PlainText",
                "text": text
            },
            "shouldEndSession": False
        }
    }

@app.route('/', methods=['GET'])
def root():
    return "Alexa Flask server is running."

