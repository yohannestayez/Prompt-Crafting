from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import os
from dotenv import load_dotenv
from Story_generator import StoryGroupChat, llm_config
import asyncio

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv('GOOGLE_API_KEY'))

app = Flask(__name__)

# Initialize StoryGroupChat with our LLM configuration
story_chat = StoryGroupChat(llm_config)

def run_async(coro):
    return asyncio.run(coro)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_story():
    data = request.get_json()
    base_prompt = data.get('base_prompt')
    genre = data.get('genre')
    
    if not base_prompt:
        return jsonify({'error': 'base_prompt is required'}), 400
        
    result = run_async(story_chat.generate_story(base_prompt, genre))
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)