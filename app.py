from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
import config
from monitor.system_monitor import get_system_metrics
from agents.agent_logs import get_logs, log_action
from ai.chat_engine import chat_engine
from tools.auto_learn import auto_learn

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/monitor')
def monitor():
    return jsonify(get_system_metrics())

@app.route('/api/logs')
def logs():
    return jsonify({"logs": get_logs()})

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_input = data.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    response = chat_engine.get_response(user_input)
    return jsonify({"response": response})

@app.route('/api/knowledge/search')
def knowledge_search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "No query provided"}), 400
    results = auto_learn.search_knowledge(query)
    return jsonify({"results": results})

@app.route('/api/knowledge/learn', methods=['POST'])
def knowledge_learn():
    data = request.json
    topic = data.get('topic')
    if not topic:
        return jsonify({"error": "No topic provided"}), 400

    # Run in background ideally, but for now simple
    learned_count = auto_learn.learn_topic(topic)
    return jsonify({"status": "Success", "learned_from": learned_count})

@app.route('/api/model/status')
def model_status():
    installed = os.path.exists(os.path.join(config.MODEL_DIR, "config.json"))
    return jsonify({"installed": installed, "model_name": config.MODEL_NAME})

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.DEBUG_MODE)
