from flask import Flask, request, jsonify
from eagpt_lib import your_chat_function  # Import the chat function from your existing code

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['user_input']
    ai_response = your_chat_function(user_input)  # Call your chat function here
    return jsonify({"ai_response": ai_response})

if __name__ == "__main__":
    app.run(port=5000)
