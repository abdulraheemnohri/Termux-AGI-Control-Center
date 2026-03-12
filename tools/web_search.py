from duckduckgo_search import DDGS
from agents.agent_logs import log_action

def web_search(query, max_results=5):
    log_action("WebSearchTool", "Searching", query)
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                results.append({
                    "title": r["title"],
                    "url": r["href"],
                    "snippet": r["body"]
                })
    except Exception as e:
        log_action("WebSearchTool", "Error", str(e))
    return results

if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "Termux AI"
    res = web_search(q)
    for r in res:
        print(f"Title: {r['title']}\nURL: {r['url']}\n")
