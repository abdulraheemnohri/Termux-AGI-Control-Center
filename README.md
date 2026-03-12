# Termux AGI Control Center 📱🤖

A local AI operating environment running inside Termux that provides autonomous internet research, automatic knowledge learning, code generation, and a cyberpunk control dashboard.

## 🚀 Concept
Termux AGI is a mobile AI research lab that runs completely on your device. It utilizes the **Qwen3-0.6B** LLM and **ChromaDB** to create a self-improving, autonomous knowledge network.

## ✨ Features
- **Autonomous Research:** AI searches and analyzes the internet to build its own knowledge.
- **Auto Learning:** Detects knowledge gaps and triggers research agents.
- **Agent Swarm:** Specialized agents for Planning, Research, Coding, Knowledge, and Tool Improvement.
- **Self-Improving Tools:** AI analyzes its own tool performance and suggests/applies code optimizations.
- **Cyberpunk Dashboard:** A modern, mobile-responsive web interface with glassmorphism and neon aesthetics.
- **Knowledge Manager:** Upload PDF, TXT, MD, or HTML files to expand the AI's brain.
- **System Monitor:** Real-time tracking of CPU, RAM, and Model status.

## 🛠️ Prerequisites
- **Android Device:** 8GB RAM recommended (6GB minimum).
- **Termux:** Installed from F-Droid (preferred).
- **Python 3.11+**

## 📥 Installation

1. **Update Termux:**
   ```bash
   pkg update && pkg upgrade
   ```

2. **Install Dependencies:**
   ```bash
   pkg install python git clang make libjpeg-turbo
   ```

3. **Clone the Repository:**
   ```bash
   git clone <repository-url>
   cd termux-agi
   ```

4. **Install Python Libraries:**
   ```bash
   pip install -r requirements.txt
   ```
   *Note: This may take a while as it installs torch and transformers.*

## 🏃 Running the System

1. **Start the Backend:**
   ```bash
   python app.py
   ```

2. **Access the Dashboard:**
   Open your mobile browser and navigate to:
   `http://localhost:5000`

## 📂 Folder Structure
```text
termux-agi/
├── app.py              # Flask Backend
├── config.py           # Configuration
├── requirements.txt    # Python Dependencies
├── ai/                 # Model & Chat logic
├── agents/             # Specialized AI Agents
├── tools/              # Research & Code Tools
├── knowledge/          # Vector Database & Docs
├── monitor/            # System metrics
├── templates/          # HTML Interface
└── static/             # CSS & JavaScript
```

## 🛡️ Self-Improvement Safety
The **Tool Improvement Agent** creates backups (`.bak`) before applying any code changes to existing tools. If a tool fails after an improvement, you can find the previous versions in the `tools/` directory.

## ⚠️ Notes
- The first time you run a chat command or start research, the system will download the **Qwen3-0.6B** model (~1.2GB) and embedding models.
- Ensure your device has enough storage (8GB+ recommended).
- Keep Termux running in the background for continuous autonomous research.
