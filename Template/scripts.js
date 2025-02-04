async function generateStory() {
    const prompt = document.getElementById('prompt').value.trim();
    const genre = document.getElementById('genre').value;
    const generateBtn = document.getElementById('generate');
    const loading = document.getElementById('loading');
    const storyOutput = document.getElementById('story-output');
    const genreDisplay = document.getElementById('genre-display');
    const storyText = document.getElementById('story-text');
    const error = document.getElementById('error');
    
    if (!prompt) {
        error.textContent = 'Please describe your challenge first!';
        return;
    }
    
    error.textContent = '';
    generateBtn.disabled = true;
    loading.style.display = 'block';
    storyOutput.style.display = 'none';
    
    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                base_prompt: prompt,
                genre: genre || undefined
            })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            genreDisplay.textContent = `Style: ${data.genre}`;
            storyText.textContent = data.story;
            storyOutput.style.display = 'block';
        } else {
            throw new Error(data.error || 'Failed to generate story');
        }
    } catch (err) {
        error.textContent = err.message || 'Something went wrong. Please try again.';
    } finally {
        generateBtn.disabled = false;
        loading.style.display = 'none';
    }
}