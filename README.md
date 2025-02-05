## Motivational Story Generator API
This is a Flask-based API that generates motivational stories based on a given prompt and an optional genre. It uses Google's Generative AI (Gemini) to create unique, styled stories.

### Select the Image below to see the demo video


### Folder Structure
```
├── static/
│   ├── scripts.js        -- JavaScript file
│   └── styles.css        -- CSS stylesheet
├── templates/
│   └── Index.html        -- HTML template
├── .env                 
├── .gitignore           
├── app.py               -- Main flask application script 
├── README.md            -- Project description and information
├── requirements.txt     -- dependencies
└── Story_generator.py   -- Python script for generating stories
```

### Features
- Customizable Genres : Choose from predefined genres like "Shakespearean", "Gym Bro", "Realistic", etc., or let the system pick one randomly.
- Simple API Endpoint : Send a POST request with a base prompt, and get a motivational story in response.
- Flexible Input : Only a base prompt is required; the genre is optional.

### Prompting Techniques 
Some of the prompting techniques used are:
- 



### Dependencies
- `flask`
- `python-dotenv`
- `requests`
- `google-generativeai`
- `pyautogen`

