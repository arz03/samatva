
function showLoader() {
    const chatBox = document.getElementById('chat-box');
    const loader = document.createElement('div');
    loader.classList.add('chat-message', 'loader', 'system');
    chatBox.appendChild(loader);
    chatBox.scrollTop = chatBox.scrollHeight;
    return loader;
}

async function sendMessage() {
    const inputField = document.getElementById('user-message');
    const userMessage = inputField.value;

    if (userMessage.trim() === '') {
        return;  
    }

    const chatBox = document.getElementById('chat-box');
    const userMessageElement = `<div class="chat-message user-message">
                                    <div>${userMessage}</div>
                                </div>`;
    chatBox.innerHTML += userMessageElement;

    chatBox.scrollTop = chatBox.scrollHeight;

    inputField.value = '';

    const loader = showLoader();

    const response = await fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: userMessage }),
    });

    const data = await response.json();
    const systemReply = data.reply;
    loader.remove();

    const systemMessageElement = `<div class="chat-message system-message">
                                    <div>${systemReply}</div>
                                  </div>`;
    chatBox.innerHTML += systemMessageElement;
    chatBox.scrollTop = chatBox.scrollHeight;
}
