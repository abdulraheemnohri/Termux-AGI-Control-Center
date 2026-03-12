import os
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer
import config

class ModelLoader:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ModelLoader, cls).__new__(cls)
            cls._instance.tokenizer = None
            cls._instance.model = None
            cls._instance.device = "cuda" if torch.cuda.is_available() else "cpu"
        return cls._instance

    def download_model(self):
        print(f"Downloading AI model {config.MODEL_NAME} to {config.MODEL_DIR}...")
        os.makedirs(config.MODEL_DIR, exist_ok=True)

        self.tokenizer = AutoTokenizer.from_pretrained(
            config.MODEL_NAME,
            cache_dir=config.MODEL_DIR,
            trust_remote_code=True
        )
        self.model = AutoModelForCausalLM.from_pretrained(
            config.MODEL_NAME,
            cache_dir=config.MODEL_DIR,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True
        )
        # Also save it directly to MODEL_DIR for easier future loading if cache_dir structure is complex
        self.tokenizer.save_pretrained(config.MODEL_DIR)
        self.model.save_pretrained(config.MODEL_DIR)
        print("Download complete.")
        return self.tokenizer, self.model

    def load_local_model(self):
        print(f"Loading local AI model from {config.MODEL_DIR}")
        self.tokenizer = AutoTokenizer.from_pretrained(config.MODEL_DIR, trust_remote_code=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            config.MODEL_DIR,
            torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            device_map="auto" if self.device == "cuda" else None,
            trust_remote_code=True
        )
        if self.device == "cpu":
            self.model.to(self.device)
        return self.tokenizer, self.model

    def load_model(self):
        if self.model is None:
            if os.path.exists(os.path.join(config.MODEL_DIR, "config.json")):
                self.load_local_model()
            else:
                self.download_model()
        return self.tokenizer, self.model

    def generate(self, prompt, max_new_tokens=512, temperature=0.7, top_p=0.9):
        tokenizer, model = self.load_model()
        inputs = tokenizer(prompt, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=max_new_tokens,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )

        response = tokenizer.decode(outputs[0][inputs['input_ids'].shape[1]:], skip_special_tokens=True)
        return response

model_loader = ModelLoader()
