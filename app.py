from flask import Flask, request, jsonify
import os
from transformers import pipeline

app = Flask(__name__)

# This downloads and loads a small open-source AI model directly into memory.
# Note: 'distilgpt2' is a lightweight model. It's not as smart as GPT-4, but it runs locally!
print("Loading AI model... (This might take a minute on startup)")
generator = pipeline('text-generation', model='distilgpt2')

@app.route('/', methods=['GET'])
def home():
    return "My Self-Hosted AI is running!"

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # Generate text based on the user's input
        # max_length controls how long the response is
        output = generator(user_message, max_length=50, num_return_sequences=1)
        
        # Extract the text from the model's output
        ai_response = output[0]['generated_text']
        
        return jsonify({"response": ai_response})
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # We use threaded=False to save memory on Render's free tier
    app.run(host='0.0.0.0', port=port, threaded=False)
