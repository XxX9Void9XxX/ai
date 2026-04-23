from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return "My Custom Groq AI is running on Render!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # We moved the client inside the chat function! 
        # This prevents the server from crashing on startup if the key is missing.
        # Groq() automatically looks for the GROQ_API_KEY environment variable.
        client = Groq()
        
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a highly intelligent and helpful AI assistant."
                },
                {
                    "role": "user",
                    "content": user_message,
                }
            ],
            model="llama-3.3-70b-versatile",
        )
        
        return jsonify({"response": chat_completion.choices[0].message.content})
        
    except Exception as e:
        # If there is an API key error, it will now safely tell you here instead of crashing the server!
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
