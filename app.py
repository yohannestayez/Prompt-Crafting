from flask import Flask, request, jsonify
from Story_generator import StoryGenerator  

app = Flask(__name__)

story_generator = StoryGenerator(api_key=API_KEY)

@app.route('/generate-story', methods=['POST'])
def generate_story():
    try:
        # Parse JSON input
        data = request.get_json()
        base_prompt = data.get("base_prompt")
        genre = data.get("genre", None)  # Optional genre

        if not base_prompt:
            return jsonify({"error": "base_prompt is required"}), 400

        # Generate the story
        result = story_generator.generate_story(base_prompt, genre)

        # Return the response
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)