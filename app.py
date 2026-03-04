from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

# A simple keyword-response mapping
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
    """Handle incoming call and prompt for speech"""
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

    # Repeat if no speech detected
    response.redirect("/voice")
    return str(response)

@app.route("/process", methods=["POST"])
def process():
    """Process the user's speech and respond dynamically"""
    response = VoiceResponse()
    user_speech = request.values.get("SpeechResult", "").lower().strip()

    if not user_speech:
        response.say("Sorry, I did not hear anything.")
        response.redirect("/voice")
        return str(response)

    # Check if user said 'bye' to end the call
    if "bye" in user_speech or "goodbye" in user_speech:
        response.say("Goodbye! Thanks for calling.")
        response.hangup()
        return str(response)

    # Check for known keywords
    answered = False
    for keyword, reply in KEYWORD_RESPONSES.items():
        if keyword in user_speech:
            response.say(reply)
            answered = True
            break

    if not answered:
        # Default response for unknown input
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

    # If no speech, redirect back
    response.redirect("/voice")
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)