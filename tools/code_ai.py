from ai.model_loader import model_loader
from agents.agent_logs import log_action

def generate_code(prompt, language="Python"):
    log_action("CodeAI", "Generating", f"{language}: {prompt}")

    full_prompt = f"### System: You are an expert programmer. Generate efficient and clean {language} code for the following request.\n\n### Request: {prompt}\n\n### Code:\n"

    code = model_loader.generate(full_prompt)
    return code

def debug_code(code, error):
    log_action("CodeAI", "Debugging", f"Error: {error}")

    full_prompt = f"### System: You are an expert debugger. Fix the following code based on the error provided.\n\n### Code:\n{code}\n\n### Error:\n{error}\n\n### Fixed Code:\n"

    fixed_code = model_loader.generate(full_prompt)
    return fixed_code

if __name__ == "__main__":
    # Test generation
    prompt = "A function to calculate fibonacci sequence"
    print(generate_code(prompt))
