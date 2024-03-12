from flask import Flask, request, jsonify, render_template, send_from_directory
from openai import OpenAI
import os
from dotenv import load_dotenv

# Access the OpenAI API key
openai_api_key = os.getenv('API_KEY')

client = OpenAI(api_key=openai_api_key)
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from flask_cors import CORS

app = Flask(__name__)
CORS(app)


@app.route('/ask', methods=['POST'])
def ask():
    user_message = request.json['message']
    response = client.chat.completions.create(model="gpt-4",
        messages=[
            # {"role": "system", "content": "you always answer with a joke"},
            # {"role": "system", "content": "you always answer with high energy, as if you're Tony Robbins"},
            {"role": "system", "content": "you always answer with opportunism and enthusiasm, pushing me to achieve a ten times better version of myself. You don't answer with practicalities, but focus on my mindset and energy level"},


            {"role": "user", "content": user_message}
            ])
    print(response)
    return jsonify({'response': response.choices[0].message.content})

if __name__ == '__main__':
    app.run(debug=True)


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)
