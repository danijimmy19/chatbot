# Chatbot with OpenAI
In this project, I built a chatbot using Python web framework (Flask) and OpenAI's API. 

## Required Packages
```shell
pip install openai
pip install Flask
```

## Configuration
You will need OpenAI API key for accessing the GPT model. You can set key using:
```shell
export OPENAI_API_KEY='api-key'
```

OR 

You can directly set it in the program in line. This approach is not recommended as it is not secure.
```Python
# initialize openai client
API_KEY = ''
```

## Running the Code
1. Set up the API key
2. Start the Flask server
```Shell
python main.py
```
3. Open the browser and navigate to `http://localhost:3000`. This will load the chat interface in the web browser.
