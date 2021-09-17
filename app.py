from flask import Flask, request, jsonify
from datetime import datetime
import os
import json
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

class TrainedModel:
    def __init__(self):
        tokenizer = RegexTokenizer()
        self.model = FastTextSocialNetworkModel(tokenizer=tokenizer)
        # pass

        
    def get_mood_coefficient(self, input_text):
        return self.model.predict([input_text], k=5)[0]
        # return {"neutral": 0.5}

class DecisionLadder:
    def get_text_by_mood(mood):
        return mood
    
    def get_options_by_mood_history(mood):
        return []



app = Flask(__name__)
moodModel = TrainedModel()


@app.route('/', methods=['POST'])
def index():
    # print(request.json)
    user = request.form.get('username')
    message = request.form.get('message')
    print("request", user, message)

    mood = max(moodModel.get_mood_coefficient(message).items(),
              key=lambda x: x[1])

    if mood[0] in ['speech', 'skip']:
        mood = ('neutral', mood[1])

    return json.dumps({
        'Mood': mood[0],
        'Current action': DecisionLadder.get_text_by_mood(mood),
        'Potential actions':
            DecisionLadder.get_options_by_mood_history(mood)
    })


if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5001))
  app.run(host = '0.0.0.0', port = port)