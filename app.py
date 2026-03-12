from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import os
import config
from monitor.system_monitor import get_system_metrics
from agents.agent_logs import get_logs, log_action
from ai.chat_engine import chat_engine
from tools.auto_learn import auto_learn
from agents.knowledge_agent import knowledge_agent
from tools.article_reader import extract_from_file
from tools.autonomous_loop import autonomous_mode
from werkzeug.utils import secure_filename

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

@app.route('/api/knowledge/upload', methods=['POST'])
def knowledge_upload():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    filename = secure_filename(file.filename)
    filepath = os.path.join(config.DOCS_DIR, filename)
    file.save(filepath)

    doc_data = extract_from_file(filepath)
    if doc_data:
        knowledge_agent.add_document(doc_data['content'], {"source": filename, "title": doc_data['title']})
        return jsonify({"status": "Success", "message": f"Stored {filename}"})
    return jsonify({"error": "Failed to process file"}), 500

@app.route('/api/knowledge/browse')
def knowledge_browse():
    metadatas = knowledge_agent.list_knowledge()
    return jsonify({"knowledge": metadatas})

@app.route('/api/knowledge/delete', methods=['DELETE'])
def knowledge_delete():
    source = request.args.get('source')
    if not source:
        return jsonify({"error": "No source provided"}), 400
    res = knowledge_agent.delete_document(source)
    return jsonify({"status": "Success", "message": res})

@app.route('/api/autonomous/start', methods=['POST'])
def autonomous_start():
    autonomous_mode.start()
    return jsonify({"status": "Started"})

@app.route('/api/autonomous/stop', methods=['POST'])
def autonomous_stop():
    autonomous_mode.stop()
    return jsonify({"status": "Stopped"})

@app.route('/api/autonomous/status')
def autonomous_status():
    return jsonify({"running": autonomous_mode.running})

@app.route('/api/model/status')
def model_status():
    installed = os.path.exists(os.path.join(config.MODEL_DIR, "config.json"))
    return jsonify({"installed": installed, "model_name": config.MODEL_NAME})

if __name__ == '__main__':
    app.run(host=config.FLASK_HOST, port=config.FLASK_PORT, debug=config.DEBUG_MODE)
