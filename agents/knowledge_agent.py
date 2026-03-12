import os
from tools.auto_learn import auto_learn
from agents.agent_logs import log_action

class KnowledgeAgent:
    def __init__(self):
        pass

    def add_document(self, content, metadata):
        log_action("KnowledgeAgent", "Storing Document", metadata.get("title", "Untitled"))
        auto_learn.store_knowledge(content, metadata)
        return "Knowledge successfully stored."

    def find_knowledge(self, query):
        log_action("KnowledgeAgent", "Searching Knowledge", query)
        results = auto_learn.search_knowledge(query)
        return results

    def list_knowledge(self):
        # Retrieve all IDs or a sample of metadatas from ChromaDB
        # For now, a simple list of topics or titles if possible
        try:
            coll = auto_learn.collection.get()
            return coll['metadatas']
        except Exception as e:
            log_action("KnowledgeAgent", "Error listing knowledge", str(e))
            return []

    def delete_document(self, source_url):
        log_action("KnowledgeAgent", "Deleting Knowledge", source_url)
        try:
            # Delete all chunks from a specific source
            auto_learn.collection.delete(where={"source": source_url})
            return f"Deleted knowledge from {source_url}"
        except Exception as e:
            log_action("KnowledgeAgent", "Error deleting knowledge", str(e))
            return str(e)

knowledge_agent = KnowledgeAgent()
