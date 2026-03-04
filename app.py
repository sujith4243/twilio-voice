from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# Simple keyword-response mapping
KEYWORD_RESPONSES = {
    "hello": "Hi there! How can I help you today?",
    "time": "I am not able to tell time yet, but I hope you have a great day!",
    "help": "You can say hello, ask for time, or say goodbye to end the call.",
    "bye": "Goodbye! Have a great day!"
}

@app.route("/", methods=["GET"])
def home():
    return "<h1>Twilio AI Voice Assistant is running!</h1>"

@app.route("/voice", methods=["POST"])
def voice():
    """Handle incoming or outgoing call and prompt for speech"""
    response = VoiceResponse()

    gather = Gather(
        input="speech",
        action="/process",
        method="POST",
        timeout=5,
        speech_timeout="auto"
    )
    gather.say("Hello! You are now connected to your AI assistant. Please ask me anything or say help.")
    response.append(gather)
    response.redirect("/voice")
    return str(response)

@app.route("/process", methods=["POST"])
def process():
    """Process user's speech and respond dynamically"""
    response = VoiceResponse()
    user_speech = request.values.get("SpeechResult", "").lower().strip()

    if not user_speech:
        response.say("Sorry, I did not hear anything.")
        response.redirect("/voice")
        return str(response)

    if "bye" in user_speech or "goodbye" in user_speech:
        response.say("Goodbye! Thanks for calling.")
        response.hangup()
        return str(response)

    answered = False
    for keyword, reply in KEYWORD_RESPONSES.items():
        if keyword in user_speech:
            response.say(reply)
            answered = True
            break

    if not answered:
        response.say("I'm not sure how to respond to that. Please try again or say help.")

    # Ask for more input after responding
    gather = Gather(
        input="speech",
        action="/process",
        method="POST",
        timeout=5,
        speech_timeout="auto"
    )
    gather.say("What else would you like to do?")
    response.append(gather)
    response.redirect("/voice")
    return str(response)

if __name__ == "__main__":
    # Use port=5000 for local, but on Render it uses $PORT
    import os
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))