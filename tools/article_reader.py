import requests
import os
from bs4 import BeautifulSoup
from agents.agent_logs import log_action
from pypdf import PdfReader

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

def extract_from_file(filepath):
    log_action("ArticleReaderTool", "Extracting from file", filepath)
    try:
        ext = os.path.splitext(filepath)[1].lower()
        if ext == ".pdf":
            reader = PdfReader(filepath)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n\n"
            return {"title": os.path.basename(filepath), "content": text, "source": filepath}
        elif ext in [".txt", ".md", ".html"]:
            with open(filepath, "r") as f:
                content = f.read()
                return {"title": os.path.basename(filepath), "content": content, "source": filepath}
    except Exception as e:
        log_action("ArticleReaderTool", "Error extracting file", str(e))
    return None

class ArticleReader:
    def read(self, url):
        return read_article(url)

    def extract(self, filepath):
        return extract_from_file(filepath)

reader = ArticleReader()

if __name__ == "__main__":
    import sys
    u = sys.argv[1] if len(sys.argv) > 1 else "https://en.wikipedia.org/wiki/Artificial_intelligence"
    res = read_article(u)
    if res:
        print(f"Title: {res['title']}\nContent Length: {len(res['content'])}")
