# Motivational Story Generator API
This is a Flask-based API that generates motivational stories based on a given prompt and an optional genre. It uses Google's Generative AI (Gemini) to create unique, styled stories.


## Folder Structure
```
├── static/
│   ├── scripts.js        -- Frontend JavaScript file
│   └── styles.css        -- Frontend CSS stylesheet
├── templates/
│   └── Index.html        -- Frontend HTML template
├── .env                 
├── .gitignore           
├── app.py               -- Main flask application script 
├── README.md            -- Project description and information
├── requirements.txt     -- dependencies
└── Story_generator.py   -- Python script for generating stories
```


## Features
- Multi-agent architecture for story generation
- Genre-specific story styling
- Customizable Genres : Choose from predefined genres like "Shakespearean", "Gym Bro", "Realistic", etc., or let the system pick one randomly.
- Simple API Endpoint : Send a POST request with a base prompt, and get a motivational story in response.
- Flexible Input : Only a base prompt is required; the genre is optional.

### Select the Image below to see the demo video

[![Project Demo Video](https://img.youtube.com/vi/hpUGSBewAU8/0.jpg)](https://www.youtube.com/watch?v=hpUGSBewAU8)

## Prompting Techniques 
Some of the prompting techniques used are:
- Role-Based Prompting
- Few-Shot Prompting
- Chain-of-Thought Prompting
- Constrained Prompting
- Multi-Turn Prompting

## Dependencies
- `flask`
- `python-dotenv`
- `requests`
- `google-generativeai`
- `pyautogen`