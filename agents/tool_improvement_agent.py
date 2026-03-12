import os
import shutil
import datetime
from ai.model_loader import model_loader
from agents.agent_logs import log_action

class ToolImprovementAgent:
    def __init__(self):
        pass

    def analyze_tool(self, tool_file):
        log_action("ToolImprovementAgent", "Analyzing tool", tool_file)
        if not os.path.exists(tool_file):
            return "Tool file not found."

        with open(tool_file, "r") as f:
            code = f.read()

        prompt = f"### System: You are a senior software engineer. Analyze the following Python tool code for performance bottlenecks, bugs, and potential improvements.\n\n### Tool Code:\n{code}\n\n### Analysis:\n"

        analysis = model_loader.generate(prompt)
        log_action("ToolImprovementAgent", "Analysis complete", tool_file)
        return analysis

    def improve_tool(self, tool_file):
        log_action("ToolImprovementAgent", "Improving tool", tool_file)
        if not os.path.exists(tool_file):
            return "Tool file not found."

        with open(tool_file, "r") as f:
            code = f.read()

        prompt = f"### System: You are a senior software engineer. Rewrite the following Python tool code to be more efficient, robust, and follow best practices while maintaining the same functionality.\n\n### Original Code:\n{code}\n\n### Improved Code:\n"

        improved_code = model_loader.generate(prompt)

        # In a real scenario, we might want to test this before replacing
        # For now, we'll just return it
        log_action("ToolImprovementAgent", "Improvement suggested", tool_file)
        return improved_code

    def apply_improvement(self, tool_file, improved_code):
        log_action("ToolImprovementAgent", "Applying improvement", tool_file)
        try:
            # 1. Backup
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = f"{tool_file}.{timestamp}.bak"
            shutil.copy2(tool_file, backup_file)
            log_action("ToolImprovementAgent", "Backup created", backup_file)

            # 2. Write improved code
            with open(tool_file, "w") as f:
                f.write(improved_code)

            log_action("ToolImprovementAgent", "Improvement applied", tool_file)
            return True, f"Applied successfully. Backup: {backup_file}"
        except Exception as e:
            log_action("ToolImprovementAgent", "Error applying", str(e))
            return False, str(e)

tool_improvement_agent = ToolImprovementAgent()
