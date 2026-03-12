import os

# System Paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
AI_DIR = os.path.join(BASE_DIR, "ai")
AGENTS_DIR = os.path.join(BASE_DIR, "agents")
TOOLS_DIR = os.path.join(BASE_DIR, "tools")
KNOWLEDGE_DIR = os.path.join(BASE_DIR, "knowledge")
DOCS_DIR = os.path.join(KNOWLEDGE_DIR, "docs")
VECTOR_DB_DIR = os.path.join(KNOWLEDGE_DIR, "vector_db")
LOGS_DIR = os.path.join(AGENTS_DIR, "logs")

# Ensure directories exist
for d in [DOCS_DIR, VECTOR_DB_DIR, LOGS_DIR]:
    os.makedirs(d, exist_ok=True)

# AI Model Configuration
# Primary LLM
MODEL_NAME = "Qwen/Qwen3-0.6B"
MODEL_DIR = os.path.join(BASE_DIR, "models", "qwen3")
EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

# Backend Configuration
FLASK_HOST = "0.0.0.0"
FLASK_PORT = 5000
DEBUG_MODE = True

# Agent Logs
AGENT_LOG_FILE = os.path.join(LOGS_DIR, "agent.log")
