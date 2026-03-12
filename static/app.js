document.addEventListener('DOMContentLoaded', () => {
    // Elements
    const cpuBar = document.getElementById('cpu-bar');
    const cpuVal = document.getElementById('cpu-val');
    const ramBar = document.getElementById('ram-bar');
    const ramVal = document.getElementById('ram-val');
    const modelIndicator = document.getElementById('model-indicator');
    const modelName = document.getElementById('model-name');
    const downloadModelBtn = document.getElementById('download-model-btn');
    const chatBox = document.getElementById('chat-box');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');
    const logContainer = document.getElementById('log-container');
    const topicInput = document.getElementById('topic-input');
    const learnBtn = document.getElementById('learn-btn');
    const knowledgeList = document.getElementById('knowledge-list');
    const fileInput = document.getElementById('file-input');
    const uploadBtn = document.getElementById('upload-btn');
    const autoStatus = document.getElementById('auto-status');
    const autoToggle = document.getElementById('auto-toggle');
    const settingsModal = document.getElementById('settings-modal');
    const topicsList = document.getElementById('topics-list');
    const saveSettings = document.getElementById('save-settings');
    const closeSettings = document.getElementById('close-settings');

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
                downloadModelBtn.style.display = data.installed ? 'none' : 'inline-block';
            });
    }

    downloadModelBtn.addEventListener('click', () => {
        downloadModelBtn.disabled = true;
        downloadModelBtn.innerText = 'DOWNLOADING...';
        fetch('/api/model/download', { method: 'POST' })
            .then(res => res.json())
            .then(data => {
                logContainer.innerHTML += `<br>[UI] ${data.message}`;
            });
    });

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
    function updateKnowledge() {
        fetch('/api/knowledge/browse')
            .then(res => res.json())
            .then(data => {
                knowledgeList.innerHTML = '';
                data.knowledge.forEach(item => {
                    const div = document.createElement('div');
                    div.className = 'knowledge-item';
                    div.innerHTML = `
                        <span class="title" title="${item.title}">${item.title}</span>
                        <span class="delete-btn" onclick="deleteKnowledge('${item.source}')">×</span>
                    `;
                    knowledgeList.appendChild(div);
                });
            });
    }

    window.deleteKnowledge = (source) => {
        if (!confirm(`Delete knowledge from ${source}?`)) return;
        fetch(`/api/knowledge/delete?source=${encodeURIComponent(source)}`, { method: 'DELETE' })
            .then(() => updateKnowledge());
    };

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
            updateKnowledge();
        });
    });

    uploadBtn.addEventListener('click', () => fileInput.click());
    fileInput.addEventListener('change', () => {
        if (!fileInput.files.length) return;
        const formData = new FormData();
        formData.append('file', fileInput.files[0]);

        logContainer.innerHTML += `<br>[UI] Uploading ${fileInput.files[0].name}...`;

        fetch('/api/knowledge/upload', {
            method: 'POST',
            body: formData
        })
        .then(res => res.json())
        .then(data => {
            logContainer.innerHTML += `<br>[UI] ${data.status || 'Error'}: ${data.message || data.error}`;
            updateKnowledge();
        });
    });

    // Autonomous Mode
    function updateAutoStatus() {
        fetch('/api/autonomous/status')
            .then(res => res.json())
            .then(data => {
                autoStatus.innerText = data.running ? 'RUNNING' : 'OFF';
                autoStatus.style.color = data.running ? 'var(--neon-cyan)' : '#888';
                autoToggle.innerText = data.running ? 'STOP' : 'START';
            });
    }

    autoToggle.addEventListener('click', () => {
        const action = autoToggle.innerText === 'START' ? 'start' : 'stop';
        fetch(`/api/autonomous/${action}`, { method: 'POST' })
            .then(() => updateAutoStatus());
    });

    // Tools
    window.triggerTool = (tool) => {
        const prompt = promptUserForTool(tool);
        if (!prompt) return;

        addMessage('system', `Executing ${tool.toUpperCase()} tool...`);

        fetch('/api/tools/execute', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ tool, params: prompt })
        })
        .then(res => res.json())
        .then(data => {
            if (tool === 'search') {
                const summary = data.results.map(r => r.title).join('\n');
                addMessage('assistant', `Search results:\n${summary}`);
            } else if (tool === 'code') {
                addMessage('assistant', `Generated code:\n\`\`\`\n${data.code}\n\`\`\``);
            } else if (tool === 'improve') {
                addMessage('assistant', `Improvement Analysis:\n${data.analysis}\n\nImproved Code generated and available in logs.`);
            }
        });
    };

    function promptUserForTool(tool) {
        if (tool === 'search') {
            const query = prompt("Enter search query:");
            return query ? { query } : null;
        }
        if (tool === 'code') {
            const promptStr = prompt("Describe the script to generate:");
            return promptStr ? { prompt: promptStr } : null;
        }
        if (tool === 'improve') {
            const target = prompt("Target tool file (e.g., tools/web_search.py):", "tools/web_search.py");
            return target ? { target } : null;
        }
        return null;
    }

    // Settings
    window.openSettings = () => {
        fetch('/api/autonomous/status')
            .then(res => res.json())
            .then(data => {
                topicsList.value = data.topics.join(', ');
                settingsModal.classList.add('active');
            });
    };

    saveSettings.addEventListener('click', () => {
        const topics = topicsList.value.split(',').map(t => t.trim());
        fetch('/api/autonomous/topics', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topics })
        })
        .then(() => {
            settingsModal.classList.remove('active');
        });
    });

    closeSettings.addEventListener('click', () => {
        settingsModal.classList.remove('active');
    });

    // Intervals
    setInterval(updateMonitor, 2000);
    setInterval(updateLogs, 3000);
    setInterval(updateAutoStatus, 5000);
    updateModelStatus();
    updateKnowledge();
    updateAutoStatus();
});
