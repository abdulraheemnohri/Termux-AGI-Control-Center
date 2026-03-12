from tools.web_search import web_search
from tools.article_reader import read_article
from tools.auto_learn import auto_learn
from agents.agent_logs import log_action

class ResearchAgent:
    def __init__(self):
        pass

    def perform_research(self, topic):
        log_action("ResearchAgent", "Researching topic", topic)

        # We can use auto_learn tool directly as it encapsulates search and read
        learned_count = auto_learn.learn_topic(topic)

        # Or do it manually if we want more control
        # results = web_search(topic)
        # for r in results:
        #    content = read_article(r['url'])
        #    ...

        summary = f"Research on '{topic}' completed. Learned from {learned_count} sources and updated knowledge base."
        log_action("ResearchAgent", "Result", summary)
        return summary

    def search_knowledge(self, query):
        log_action("ResearchAgent", "Searching Knowledge Base", query)
        results = auto_learn.search_knowledge(query)
        return results

research_agent = ResearchAgent()
