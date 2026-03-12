from ai.model_loader import model_loader
from agents.knowledge_agent import knowledge_agent
from agents.agent_logs import log_action

class ChatEngine:
    def __init__(self):
        self.history = []
        self.system_prompt = "You are the Termux AGI Control Center, a helpful and efficient AI assistant running locally on a mobile device. You provide concise and accurate information. Use the provided context if relevant."

    def get_response(self, user_input):
        log_action("ChatEngine", "Processing query", user_input)

        # RAG: Search knowledge base
        context_chunks = knowledge_agent.find_knowledge(user_input)
        context_str = ""
        if context_chunks:
            context_str = "\nRelevant Knowledge Context:\n" + "\n".join(context_chunks[:3])
            log_action("ChatEngine", "RAG", f"Found {len(context_chunks)} relevant chunks")

        self.history.append({"role": "user", "content": user_input})

        # Build prompt from history
        full_prompt = f"{self.system_prompt}\n{context_str}\n\n"
        for msg in self.history[-10:]: # Keep last 10 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            full_prompt += f"{role}: {msg['content']}\n"
        full_prompt += "Assistant: "

        response = model_loader.generate(full_prompt)
        self.history.append({"role": "assistant", "content": response})
        return response

    def clear_history(self):
        self.history = []

chat_engine = ChatEngine()
