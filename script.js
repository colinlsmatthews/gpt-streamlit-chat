let apiKey = '';

function setAPIKey() {
    apiKey = document.getElementById('api-key').value;
}

let username = '';

function setUsername() {
    username = document.getElementById('username').value;
    document.getElementById('user').innerHTML = username;
}

async function sendMessage() {
    if (!apiKey) {
        alert("API Key is required.");
        return;
    }
    if (!username) {
        alert("Username is required.");
        return;
    }
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input').value;
    
    // Append user's message to chat-box
    chatBox.innerHTML += `<div>${username}: ${userInput}</div>`;
    
    const response = await fetch('http://127.0.0.1:5000/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ "user_input": userInput, "api_key": apiKey }),
    });
    const data = await response.json();
    
    // Append chatbot's message to chat-box
    chatBox.innerHTML += `<div>EAGPT: ${data.ai_response}</div>`;
}
