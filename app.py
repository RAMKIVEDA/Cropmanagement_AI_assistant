import os
import openai
import requests
import uuid
import json
from flask import Flask, render_template, request, jsonify, send_file

app = Flask(__name__)
openai.api_key = "provide openai api key"

# Set up Azure translator
subscription_key = 'provide translator key'
endpoint = 'https://api.cognitive.microsofttranslator.com/'
location = 'provide region'


def translate(input_text, target_language):
    path = '/translate'
    constructed_url = endpoint + path

    params = {
        'api-version': '3.0',
        'from': 'en',
        'to': [target_language]
    }

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': location,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{'text': input_text}]

    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()
    return response[0]['translations'][0]['text']

def translate_to_english(input_text):
    return translate(input_text, 'en')

def translate_to_hindi(input_text):
    return translate(input_text, 'hi')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question = request.form.get('question')

    # Translate question to English
    question_in_english = translate_to_english(question)

    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=f"Farmer question: {question_in_english}\nAnswer:",
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.5,
    )

    answer = response.choices[0].text.strip()

    # Translate answer to Hindi
    answer_in_hindi = translate_to_hindi(answer)

    return jsonify({'answer': answer_in_hindi})

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
