import json
from ai.model_loader import model_loader
from agents.agent_logs import log_action

class PlannerAgent:
    def __init__(self):
        self.system_prompt = """You are the Planner Agent. Your job is to decompose a user request into a sequence of tasks.
Available Tools:
- web_search(query): Search the internet.
- read_article(url): Read a webpage.
- store_knowledge(content, metadata): Store information.
- generate_code(prompt, language): Write code.
- search_knowledge(query): Search the internal knowledge base.

Respond ONLY with a JSON list of tasks, each with 'tool' and 'params' keys.
Example: [{"tool": "web_search", "params": {"query": "current weather in Tokyo"}}]
"""

    def plan(self, user_request):
        log_action("PlannerAgent", "Planning", user_request)

        full_prompt = f"{self.system_prompt}\n\nUser Request: {user_request}\nPlan:"

        response = model_loader.generate(full_prompt)

        try:
            # Try to extract JSON from response
            start = response.find("[")
            end = response.rfind("]") + 1
            if start != -1 and end != -1:
                plan_json = response[start:end]
                tasks = json.loads(plan_json)
                log_action("PlannerAgent", "Plan Generated", f"{len(tasks)} tasks")
                return tasks
        except Exception as e:
            log_action("PlannerAgent", "Error parsing plan", str(e))

        # Fallback plan if LLM fails to produce JSON
        return [{"tool": "chat", "params": {"message": user_request}}]

if __name__ == "__main__":
    planner = PlannerAgent()
    print(planner.plan("Research how to build a Flask app"))
