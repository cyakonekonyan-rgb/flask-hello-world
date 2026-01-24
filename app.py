from flask import Flask, request, jsonify
from ask_sdk_webservice_support.webservice_handler import WebserviceSkillHandler
from ask_sdk_core.skill_builder import SkillBuilder

sb = SkillBuilder()
app = Flask(__name__)

# LaunchRequest
@sb.request_handler(can_handle_func=lambda handler_input:
                    handler_input.request_envelope.request.object_type == "LaunchRequest")
def launch_request_handler(handler_input):
    speech = "でんすけせんせいを起動しました。何をしますか？"
    return handler_input.response_builder.speak(speech).ask(speech).response

# HelloIntent
@sb.request_handler(can_handle_func=lambda handler_input:
                    handler_input.request_envelope.request.intent.name == "HelloIntent")
def hello_handler(handler_input):
    speech = "こんにちは、私はでんすけせんせいです。"
    return handler_input.response_builder.speak(speech).ask(speech).response

# Fallback
@sb.request_handler(can_handle_func=lambda handler_input: True)
def fallback_handler(handler_input):
    return handler_input.response_builder.speak(
        "その機能にはまだ対応していません。").ask(
        "何をしますか？").response

skill_handler = WebserviceSkillHandler(skill=sb.create())

@app.post("/")
def invoke_skill():
    return skill_handler.verify_and_dispatch(request.data, request.headers)

@app.get("/")
def health():
    return "Alexa Flask server is running."
