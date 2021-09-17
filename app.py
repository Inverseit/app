from flask import Flask, request, jsonify
from datetime import datetime

import json
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel

class TrainedModel:
    def __init__(self):
        tokenizer = RegexTokenizer()
        self.model = FastTextSocialNetworkModel(tokenizer=tokenizer)
        pass

        
    def get_mood_coefficient(self, input_text):
        return self.model.predict([input_text], k=5)[0]

class DecisionLadder:
    def get_text_by_mood(mood):
        return mood
    
    def get_options_by_mood_history(mood):
        return []



app = Flask(__name__)
moodModel = TrainedModel()


@app.route('/', methods=['POST'])
async def index():
    object = json.loads(request.get_json())
    user = object['username']
    message = object['message']

    mood = max(moodModel.get_mood_coefficient(message).items(),
              key=lambda x: x[1])

    if mood[0] in ['speech', 'skip']:
        mood = ('neutral', mood[1])

    return json.dumps({
        'Mood': mood[0],
        'Current action': DecisionLadder.get_text_by_mood(mood),
        'Potential actions':
            DecisionLadder.get_options_by_mood_history(total_mood_list)
    })


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)