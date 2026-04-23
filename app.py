from flask import Flask, request, jsonify, render_template_string
import os
from groq import Groq

app = Flask(__name__)

# This is a simple HTML interface so you can actually type to your AI
HTML_UI = """
<!DOCTYPE html>
<html>
<head>
    <title>My Custom AI</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 50px auto; padding: 20px; }
        #chatbox { height: 300px; border: 1px solid #ccc; overflow-y: scroll; padding: 10px; margin-bottom: 10px; background: #f9f9f9; }
        #input-area { display: flex; }
        input { flex-grow: 1; padding: 10px; }
        button { padding: 10px; background: #007bff; color: white; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <h2>Chat with my AI</h2>
    <div id="chatbox"></div>
    <div id="input-area">
        <input type="text" id="user-input" placeholder="Type a message...">
        <button onclick="sendMessage()">Send</button>
    </div>

    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const chatbox = document.getElementById('chatbox');
            const message = input.value;
            if (!message) return;

            chatbox.innerHTML += `<div><b>You:</b> ${message}</div>`;
            input.value = '';

            const response = await fetch('/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            const data = await response.json();
            chatbox.innerHTML += `<div><b>AI:</b> ${data.response || data.error}</div>`;
            chatbox.scrollTop = chatbox.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET'])
def home():
    return render_template_string(HTML_UI)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    
    try:
        # This uses the GROQ_API_KEY you set in Render's Environment tab
        client = Groq()
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}],
            model="llama-3.3-70b-versatile",
        )
        return jsonify({"response": completion.choices[0].message.content})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
