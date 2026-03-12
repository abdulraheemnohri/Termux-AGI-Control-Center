document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const cpuBar = document.getElementById('cpu-bar');
    const cpuVal = document.getElementById('cpu-val');
    const ramBar = document.getElementById('ram-bar');
    const ramVal = document.getElementById('ram-val');
    const modelIndicator = document.getElementById('model-indicator');
    const modelName = document.getElementById('model-name');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const logContainer = document.getElementById('log-container');
    const topicInput = document.getElementById('topic-input');
    const learnBtn = document.getElementById('learn-btn');
    const knowledgeResults = document.getElementById('knowledge-results');

    // Monitoring
    function updateMonitor() {
        fetch('/api/monitor')
            .then(res => res.json())
            .then(data => {
                cpuBar.style.width = data.cpu + '%';
                cpuVal.innerText = data.cpu + '%';
                ramBar.style.width = data.ram_used + '%';
                ramVal.innerText = data.ram_used + '%';

                if (data.model_status === "Installed") {
                    modelIndicator.className = 'status-dot green';
                } else {
                    modelIndicator.className = 'status-dot red';
                }
            });
    }

    function updateModelStatus() {
        fetch('/api/model/status')
            .then(res => res.json())
            .then(data => {
                modelName.innerText = data.model_name + (data.installed ? ' (Ready)' : ' (Not Installed)');
            });
    }

    // Chat
    function addMessage(role, text) {
        const msgDiv = document.createElement('div');
        msgDiv.className = `message ${role}`;
        msgDiv.innerHTML = `<strong>${role.toUpperCase()}:</strong> ${text}`;
        chatBox.appendChild(msgDiv);
        chatBox.scrollTop = chatBox.scrollHeight;
    }

    sendBtn.addEventListener('click', () => {
        const message = userInput.value.trim();
        if (!message) return;

        addMessage('user', message);
        userInput.value = '';

        fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        })
        .then(res => res.json())
        .then(data => {
            addMessage('assistant', data.response);
        })
        .catch(err => {
            addMessage('system', 'Error connecting to AI engine.');
        });
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') sendBtn.click();
    });

    // Logs
    function updateLogs() {
        fetch('/api/logs')
            .then(res => res.json())
            .then(data => {
                logContainer.innerHTML = data.logs.join('<br>');
                logContainer.scrollTop = logContainer.scrollHeight;
            });
    }

    // Knowledge
    learnBtn.addEventListener('click', () => {
        const topic = topicInput.value.trim();
        if (!topic) return;

        logContainer.innerHTML += `<br>[UI] Triggering learning for: ${topic}`;
        topicInput.value = '';

        fetch('/api/knowledge/learn', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic })
        })
        .then(res => res.json())
        .then(data => {
            logContainer.innerHTML += `<br>[UI] Learning completed for ${topic}`;
        });
    });

    // Intervals
    setInterval(updateMonitor, 2000);
    setInterval(updateLogs, 3000);
    updateModelStatus();
});
