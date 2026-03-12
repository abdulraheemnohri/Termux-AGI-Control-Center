from tools.code_ai import generate_code, debug_code
from agents.agent_logs import log_action

class CoderAgent:
    def __init__(self):
        pass

    def create_script(self, requirement, language="Python"):
        log_action("CoderAgent", "Creating script", f"{language}: {requirement}")
        code = generate_code(requirement, language)
        log_action("CoderAgent", "Script created", f"Length: {len(code)}")
        return code

    def fix_code(self, code, error):
        log_action("CoderAgent", "Fixing code", f"Error: {error}")
        fixed_code = debug_code(code, error)
        log_action("CoderAgent", "Code fixed", f"Length: {len(fixed_code)}")
        return fixed_code

coder_agent = CoderAgent()
