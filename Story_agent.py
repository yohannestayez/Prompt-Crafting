import random
import google.generativeai as genai

GENRES = ["Shakespearean", "Gym Bro", "Zen Master", "Sci-Fi Futurist", "Rap/Hip-Hop", "Sarcastic"]

class StoryGenerator:
    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')

    def generate_story(self, base_prompt: str, genre: str = None) -> str:
        genre = genre or random.choice(GENRES)
        genre_style = {
            "Shakespearean": "Old English style with 'thee', 'thou', and poetic metaphors.",
            "Gym Bro": "High-energy gym slang and fitness metaphors.",
            "Zen Master": "Calm, mindful language with Eastern philosophy.",
            "Sci-Fi Futurist": "Technological metaphors and futuristic concepts.",
            "Rap/Hip-Hop": "Rhythm, rhyme, and urban storytelling.",
            "Sarcastic": "Witty, ironic tone while staying motivational."
        }[genre]

        prompt = f"""
        Write a motivational story in {genre} style ({genre_style}) for this situation: {base_prompt}.
        Follow this structure: Challenge → Struggle → Clarity → Triumph. Keep it 100-150 words.
        """
        response = self.model.generate_content(prompt, generation_config=llm_config)
        return {"genre": genre, "story": response.text}

# Example usage
if __name__ == "__main__":
    API_KEY = "your_api_key_here"  # Replace with your actual API key
    generator = StoryGenerator(api_key=API_KEY)
    
    base_prompt = "I'm struggling to stay motivated at work."
    result = generator.generate_story(base_prompt)
    print(f"Genre: {result['genre']}")
    print(f"Story:\n{result['story']}")