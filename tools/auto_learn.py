import chromadb
from chromadb.utils import embedding_functions
import config
from tools.web_search import web_search
from tools.article_reader import read_article
from agents.agent_logs import log_action

class AutoLearn:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=config.VECTOR_DB_DIR)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=config.EMBEDDING_MODEL_NAME
        )
        self.collection = self.client.get_or_create_collection(
            name="knowledge",
            embedding_function=self.embedding_function
        )

    def learn_topic(self, topic):
        log_action("AutoLearn", "Starting research", topic)

        # 1. Search
        search_results = web_search(topic, max_results=config.MAX_SEARCH_RESULTS)

        learned_count = 0
        for res in search_results:
            # 2. Read
            article = read_article(res['url'])
            if article and article['content']:
                # 3. Store
                self.store_knowledge(article['content'], {
                    "source": article['url'],
                    "title": article['title'],
                    "topic": topic
                })
                learned_count += 1
                log_action("AutoLearn", "Learned from", article['url'])

        log_action("AutoLearn", "Completed research", f"Learned from {learned_count} sources")
        return learned_count

    def store_knowledge(self, text, metadata):
        # Split text into chunks (simple paragraph splitting for now)
        chunks = [c.strip() for c in text.split("\n\n") if len(c.strip()) > 50]

        ids = [f"{metadata['source']}_{i}" for i in range(len(chunks))]
        metadatas = [metadata for _ in range(len(chunks))]

        if chunks:
            self.collection.add(
                documents=chunks,
                metadatas=metadatas,
                ids=ids
            )

    def search_knowledge(self, query, n_results=3):
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        return results['documents'][0] if results['documents'] else []

auto_learn = AutoLearn()

if __name__ == "__main__":
    import sys
    topic = sys.argv[1] if len(sys.argv) > 1 else "Python programming"
    auto_learn.learn_topic(topic)
