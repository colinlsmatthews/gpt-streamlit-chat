from flask import Flask, request, jsonify
# from EAGPT import your_chat_function  # Replace 'your_chat_function' with the actual function name

app = Flask(__name__)


@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json['user_input']
    ai_response = your_chat_function(user_input)
    return jsonify({"ai_response": ai_response})


if __name__ == "__main__":
    app.run(port=5000)
