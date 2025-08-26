from flask import Flask, request, jsonify
import google.generativeai as genai
import os
from config import *

# Load Ame-chan prompt

def load_amechan_prompt():
    prompt_path = os.path.join(os.path.dirname(__file__), 'amechan_prompt.txt')
    with open(prompt_path, 'r', encoding='utf-8') as f:
        return f.read().strip()

app = Flask(__name__)
genai.configure(api_key=GOOGLE_AI_KEY)

# Prepare the initial chat template with Ame-chan's prompt as user message
amechan_prompt = load_amechan_prompt()
bot_template = [
    {"role": "user", "parts": [amechan_prompt]}
]

model = genai.GenerativeModel(model_name="gemini-2.5-flash", generation_config=text_generation_config, safety_settings=safety_settings)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    # Start a new chat session for each request (stateless)
    chat_session = model.start_chat(history=bot_template)
    response = chat_session.send_message(user_message)
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
