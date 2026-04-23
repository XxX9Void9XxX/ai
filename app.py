from flask import Flask, request, jsonify
import os
from groq import Groq

app = Flask(__name__)

# Initialize the Groq client. It will pull your key securely from Render.
client = Groq(api_key=os.environ.get("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"))

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
        # We are using Meta's incredibly smart Llama 3.3 (70 billion parameters)
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    # Customize your AI's brain/personality right here!
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
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
