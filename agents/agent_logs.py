import os
import datetime
import config

def log_action(agent_name, action, details=""):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {agent_name}: {action} | {details}\n"

    os.makedirs(os.path.dirname(config.AGENT_LOG_FILE), exist_ok=True)
    with open(config.AGENT_LOG_FILE, "a") as f:
        f.write(log_entry)
    print(log_entry.strip())

def get_logs(limit=50):
    if not os.path.exists(config.AGENT_LOG_FILE):
        return []
    with open(config.AGENT_LOG_FILE, "r") as f:
        lines = f.readlines()
    return lines[-limit:]
