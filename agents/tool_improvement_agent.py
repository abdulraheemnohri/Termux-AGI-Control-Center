import os
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

tool_improvement_agent = ToolImprovementAgent()
