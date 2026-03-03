from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "<h1>Twilio AI Voice Assistant is running!</h1>"

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    gather = Gather(
        input="speech",
        action="/process",
        method="POST",
        timeout=5,
        speech_timeout="auto"
    )
    gather.say("Hello! You are now connected to your AI assistant. Please ask me anything.")
    response.append(gather)
    response.redirect("/voice")  # Repeat if no speech detected
    return str(response)

@app.route("/process", methods=["POST"])
def process():
    response = VoiceResponse()
    user_speech = request.values.get("SpeechResult")

    if not user_speech:
        response.say("Sorry, I did not hear anything.")
        response.redirect("/voice")
        return str(response)

    # Temporary static response without OpenAI
    response.say("Hi there! How can I help you today?")
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)