from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "Alexa Flask server running."

@app.route("/alexa", methods=["POST"])
def alexa_webhook():

    data = request.get_json()
    print("=== Alexa Request ===")
    print(data)

    req_type = data["request"]["type"]

    # LaunchRequest
    if req_type == "LaunchRequest":
        return jsonify(build_response("でんすけせんせいを起動しました。何をしますか？"))

    # IntentRequest
    if req_type == "IntentRequest":
        intent = data["request"]["intent"]["name"]

        if intent == "HelloIntent":
            return jsonify(build_response("こんにちは、私はでんすけせんせいです。"))

        return jsonify(build_response("その意図にはまだ対応していません。"))

    return jsonify(build_response("リクエストを処理できませんでした。"))

def build_response(text):
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

if __name__ == "__main__":
    app.run()
