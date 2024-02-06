const { spawn } = require('child_process');

document.getElementById('userInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

async function sendMessage() {
    const input = document.getElementById('userInput').value;
    displayMessage(input, 'you');
    showLoading(true);

    const response = await fetch('http://localhost:8000/query/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ text: input })
    })
    const data = await response.json();
    console.log(data);

    displayMessage(data.response, 'mistral');
    if (data.source) {
        displayMessage(data.source, 'source');
    }
}

function openInObsidian(filePath) {
    const { ipcRenderer } = require('electron');
    const filename = filePath.split('/').pop();
    ipcRenderer.send('open-in-obsidian', filename);
}

function showLoading(show) {
    const chatDiv = document.getElementById('chat');
    const loadingBubble = document.getElementById('loading') || createLoadingBubble();
    loadingBubble.style.display = show ? 'block' : 'none';
    if (show) chatDiv.appendChild(loadingBubble);
}

function createLoadingBubble() {
    const loadingBubble = document.createElement('div');
    loadingBubble.id = 'loading';
    loadingBubble.classList.add('message', 'loading');
    loadingBubble.innerHTML = '<div class="loader"></div>'; // use an inner div for the loader animation
    return loadingBubble;
}

function displayMessage(message, sender) {
    const chatDiv = document.getElementById('chat');
    const messageElement = document.createElement('p');
    messageElement.classList.add('message', sender);

    if (sender === 'source') {
        // if sender is 'source' then message is in the form of
        // [filename](filepath)
        // we need to create a link to the file
        const linkElement = document.createElement('a');
        linkElement.href = '#';
        linkElement.textContent = message.split('/').pop();
        linkElement.onclick = () => openInObsidian(message);
        messageElement.appendChild(linkElement);

    } else {
        messageElement.textContent = `${sender} > ${message}`;
    }

    chatDiv.appendChild(messageElement);
    if (sender === 'you') {
        document.getElementById('userInput').value = ''; // Clear input field after sending message
    } else {
        showLoading(false);
    }
    chatDiv.scrollTop = chatDiv.scrollHeight; // Auto-scroll to the latest message
}

function openInObsidian(filePath) {
    // Send a message to the main process via IPC to open the file in Obsidian
    const { ipcRenderer } = require('electron');
    ipcRenderer.send('open-file-in-obsidian', filePath);
}
