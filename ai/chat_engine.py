from ai.model_loader import model_loader

class ChatEngine:
    def __init__(self):
        self.history = []
        self.system_prompt = "You are the Termux AGI Control Center, a helpful and efficient AI assistant running locally on a mobile device. You provide concise and accurate information."

    def get_response(self, user_input):
        self.history.append({"role": "user", "content": user_input})

        # Build prompt from history
        full_prompt = f"{self.system_prompt}\n\n"
        for msg in self.history[-5:]: # Keep last 5 messages for context
            role = "User" if msg["role"] == "user" else "Assistant"
            full_prompt += f"{role}: {msg['content']}\n"
        full_prompt += "Assistant: "

        response = model_loader.generate(full_prompt)
        self.history.append({"role": "assistant", "content": response})
        return response

    def clear_history(self):
        self.history = []

chat_engine = ChatEngine()
