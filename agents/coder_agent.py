import os
import datetime
from tools.code_ai import generate_code, debug_code
from agents.agent_logs import log_action

class CoderAgent:
    def __init__(self):
        self.output_dir = "generated_scripts"
        os.makedirs(self.output_dir, exist_ok=True)

    def create_script(self, requirement, language="Python"):
        log_action("CoderAgent", "Creating script", f"{language}: {requirement}")
        code = generate_code(requirement, language)

        # Save script locally
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        ext = ".py" if language.lower() == "python" else ".txt"
        filename = f"script_{timestamp}{ext}"
        filepath = os.path.join(self.output_dir, filename)

        with open(filepath, "w") as f:
            f.write(code)

        log_action("CoderAgent", "Script created and saved", f"Path: {filepath}")
        return code

    def fix_code(self, code, error):
        log_action("CoderAgent", "Fixing code", f"Error: {error}")
        fixed_code = debug_code(code, error)
        log_action("CoderAgent", "Code fixed", f"Length: {len(fixed_code)}")
        return fixed_code

coder_agent = CoderAgent()
