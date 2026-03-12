import psutil
import os
import config

def get_system_metrics():
    cpu_usage = psutil.cpu_percent(interval=1)
    ram = psutil.virtual_memory()

    # Check model status (basic check if MODEL_DIR exists and has config.json)
    model_installed = os.path.exists(os.path.join(config.MODEL_DIR, "config.json"))

    return {
        "cpu": cpu_usage,
        "ram_used": ram.percent,
        "ram_available": ram.available / (1024 * 1024), # MB
        "model_status": "Installed" if model_installed else "Not Installed",
        "active_agents": ["PlannerAgent", "ResearchAgent", "CoderAgent"] # Simplified
    }

if __name__ == "__main__":
    metrics = get_system_metrics()
    print(f"CPU: {metrics['cpu']}%")
    print(f"RAM: {metrics['ram_used']}%")
    print(f"Model: {metrics['model_status']}")
