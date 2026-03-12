import requests
from bs4 import BeautifulSoup
from agents.agent_logs import log_action

def read_article(url):
    log_action("ArticleReaderTool", "Reading", url)
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')

        # Remove navigation and other noise
        for tag in soup(['nav', 'header', 'footer', 'script', 'style', 'aside']):
            tag.decompose()

        # Extract text from paragraphs
        paragraphs = soup.find_all('p')
        text = "\n\n".join([p.get_text().strip() for p in paragraphs if p.get_text().strip()])

        return {
            "title": soup.title.string if soup.title else "No Title",
            "content": text,
            "url": url
        }
    except Exception as e:
        log_action("ArticleReaderTool", "Error", str(e))
        return None

if __name__ == "__main__":
    import sys
    u = sys.argv[1] if len(sys.argv) > 1 else "https://en.wikipedia.org/wiki/Artificial_intelligence"
    res = read_article(u)
    if res:
        print(f"Title: {res['title']}\nContent Length: {len(res['content'])}")
