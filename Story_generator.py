import autogen
from typing import Dict, Optional, List
import random
import google.generativeai as genai
import asyncio

# LLM Configuration
llm_config = {
    "temperature": 0.9,
    "max_tokens": 150,
    "top_p": 0.95,
}

# Convert LLM config to Gemini's format
def get_gemini_config():
    config = genai.types.GenerationConfig(
        temperature=llm_config["temperature"],
        top_k=60,  # Increased for more diverse token selection
        top_p=llm_config["top_p"],
        max_output_tokens=llm_config["max_tokens"],
        candidate_count=1
    )
    return config

# Get AutoGen config with our parameters
def get_autogen_config():
    return {
        "temperature": llm_config["temperature"],
        "max_tokens": llm_config["max_tokens"],
        "top_p": llm_config["top_p"],
        "frequency_penalty": llm_config["frequency_penalty"],
        "presence_penalty": llm_config["presence_penalty"],
        "seed": llm_config["seed"],
        "model": "gemini-pro",
        "config_list": [{"model": "gemini-pro"}]
    }

GENRES = [
    "Shakespearean",
    "Gym Bro",
    "Zen Master",
    "Sci-Fi Futurist",
    "Rap/Hip-Hop",
    "Sarcastic"
]

class StoryAgentBase(autogen.AssistantAgent):
    def __init__(self, name: str, system_message: str):
        super().__init__(
            name=name,
            llm_config=get_autogen_config(),
            system_message=system_message
        )
        
    def generate_response(self, prompt: str) -> str:
        model = genai.GenerativeModel('gemini-pro')
        generation_config = get_gemini_config()
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )
        return response.text

class UserProxyAgent(StoryAgentBase):
    def __init__(self):
        system_message = """
        You are the UserProxy agent responsible for validating and contextualizing user input.
        Your role is to ensure the base prompt is provided and select an appropriate genre if none is specified.
        """
        super().__init__(
            name="UserProxy",
            system_message=system_message
        )
    
    def validate_input(self, base_prompt: str, genre: Optional[str]) -> Dict:
        if not base_prompt:
            raise ValueError("base_prompt is required")
            
        selected_genre = genre if genre in GENRES else random.choice(GENRES)
        contextualized_prompt = (
            f"Context: Someone facing this challenge: '{base_prompt}'\n"
            f"Task: Create a motivational response that addresses their situation."
        )
        
        return {
            "base_prompt": contextualized_prompt,
            "genre": selected_genre
        }

class PromptVariationAgent(StoryAgentBase):
    def __init__(self):
        system_message = """
        You are the PromptVariation agent responsible for generating the initial story draft.
        Use zero-shot and few-shot prompting techniques to create a compelling narrative structure.
        """
        super().__init__(
            name="PromptVariation",
            system_message=system_message
        )
    
    def generate_draft(self, base_prompt: str, genre: str) -> str:
        prompt = f"""
        Write a motivational story based on this situation: {base_prompt}
        
        Here are two example story structures to guide you:
        
        Example 1:
        Challenge → Internal Struggle → Moment of Clarity → Triumph
        
        Example 2:
        Setback → Learning → Adaptation → Success
        
        Generate a unique 100-150 word story following a similar narrative arc.
        """
        
        return self.generate_response(prompt)

class GenreStylingAgent(StoryAgentBase):
    def __init__(self):
        system_message = """
        You are the GenreStyling agent responsible for adapting the story to a specific genre.
        Apply appropriate language, metaphors, and stylistic elements based on the chosen genre.
        """
        super().__init__(
            name="GenreStyling",
            system_message=system_message
        )
    
    def style_story(self, draft: str, genre: str) -> str:
        genre_prompts = {
            "Shakespearean": "Write in eloquent, theatrical Old English style with 'thee', 'thou', and poetic metaphors",
            "Gym Bro": "Use modern gym culture slang, high energy, and fitness metaphors",
            "Zen Master": "Employ calm, mindful language with Eastern philosophical concepts",
            "Sci-Fi Futurist": "Incorporate technological metaphors and futuristic concepts",
            "Rap/Hip-Hop": "Use rhythm, rhyme, and contemporary urban storytelling style",
            "Sarcastic": "Add witty, ironic observations while maintaining motivational impact"
        }
        
        prompt = f"""
        As a master of {genre} storytelling:
        Rewrite this story in {genre} style using these guidelines: {genre_prompts[genre]}
        
        Original story:
        {draft}
        
        Maintain the core message but transform the language and style while keeping it between 100-150 words.
        """
        
        return self.generate_response(prompt)

class FinalComparisonAgent(StoryAgentBase):
    def __init__(self):
        system_message = """
        You are the FinalComparison agent responsible for quality assurance and story finalization.
        Ensure the story meets length requirements, maintains coherence, and delivers a clear message.
        """
        super().__init__(
            name="FinalComparison",
            system_message=system_message
        )
    
    def finalize_story(self, story: str) -> str:
        prompt = f"""
        Review and refine this story using the following steps:
        1. Check if the story is between 100-150 words
        2. Verify the narrative flow is coherent
        3. Ensure the motivational message is clear
        4. Maintain consistent style throughout
        
        Story to review:
        {story}
        
        If needed, adjust the story to meet these criteria while preserving its essence.
        Return only the final story without any additional commentary.
        """
        
        return self.generate_response(prompt)

class StoryGroupChat:
    def __init__(self, config: dict):
        self.config = config
        self.user_proxy = UserProxyAgent()
        self.prompt_variation = PromptVariationAgent()
        self.genre_styling = GenreStylingAgent()
        self.final_comparison = FinalComparisonAgent()
        
        # Create GroupChat
        self.group_chat = autogen.GroupChat(
            agents=[
                self.user_proxy,
                self.prompt_variation,
                self.genre_styling,
                self.final_comparison
            ],
            messages=[],
            max_round=4
        )
        
        # Create GroupChatManager
        self.manager = autogen.GroupChatManager(
            groupchat=self.group_chat,
            llm_config=get_autogen_config()
        )
    
    async def generate_story(self, base_prompt: str, genre: Optional[str] = None) -> Dict:
        # Step 1: Validate input
        validated_input = self.user_proxy.validate_input(base_prompt, genre)
        
        # Step 2: Generate initial draft
        draft = self.prompt_variation.generate_draft(
            validated_input['base_prompt'],
            validated_input['genre']
        )
        
        # Step 3: Apply genre styling
        styled_story = self.genre_styling.style_story(
            draft,
            validated_input['genre']
        )
        
        # Step 4: Finalize story
        final_story = self.final_comparison.finalize_story(styled_story)
        
        return {
            'genre': validated_input['genre'],
            'story': final_story
        }
