from datetime import timedelta
from flask import render_template, request, jsonify
import requests
from app import app
from app.get_api_key import get_iam_token

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/chat', methods=['POST', 'GET'])
def chat():
    bear = get_iam_token()["iamToken"]

    headers = {
        'x-node-id': 'bt1nrcqlo7781a84n0l6',
        'Authorization': f'Bearer {bear}',
        'x-folder-id': 'b1gvmo70ll74cvokevfk',
    }

    if request.method == 'POST':
        data = request.get_json()
        user_message = data.get('message')
        print(user_message)
        response = requests.post('https://node-api.datasphere.yandexcloud.net/generate', headers=headers, json={'prompt': user_message})
        print(response.text)
        return jsonify({"response": response.json()['answer: ']})

    return render_template('chat.html')
