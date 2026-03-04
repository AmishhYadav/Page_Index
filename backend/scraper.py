import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
from urllib.robotparser import RobotFileParser
import logging
import re

logger = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "PageIndexBot/1.0 (Educational Project)",
    "Accept": "text/html,application/xhtml+xml",
    "Accept-Language": "en-US,en;q=0.9",
}

TIMEOUT = 15  # seconds
MAX_CONTENT_LENGTH = 5 * 1024 * 1024  # 5MB


def check_robots_txt(url):
    """Check if we're allowed to scrape this URL."""
    try:
        parsed = urlparse(url)
        robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch("*", url)
    except Exception as e:
        logger.warning(f"Could not check robots.txt for {url}: {e}")
        return True  # Allow if robots.txt is unreachable


def scrape_page(url):
    """Scrape a web page and return structured data."""
    try:
        # Check robots.txt
        if not check_robots_txt(url):
            logger.warning(f"Blocked by robots.txt: {url}")
            return None

        # Make request with timeout and size limit
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=TIMEOUT,
            allow_redirects=True,
            verify=True,
            stream=True
        )
        response.raise_for_status()

        # Check content type
        content_type = response.headers.get("Content-Type", "")
        if "text/html" not in content_type and "application/xhtml" not in content_type:
            logger.warning(f"Non-HTML content at {url}: {content_type}")
            return None

        # Check content length
        content_length = response.headers.get("Content-Length")
        if content_length and int(content_length) > MAX_CONTENT_LENGTH:
            logger.warning(f"Content too large at {url}: {content_length}")
            return None

        # Read content with size limit
        content = response.text[:MAX_CONTENT_LENGTH]

        soup = BeautifulSoup(content, "html.parser")

        # Remove script, style, nav, footer, header tags
        for tag in soup(["script", "style", "nav", "footer", "header", "aside", "noscript"]):
            tag.decompose()

        # Extract title
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        elif soup.find("h1"):
            title = soup.find("h1").get_text(strip=True)
        else:
            title = urlparse(url).netloc

        # Extract meta description
        meta_desc = ""
        meta_tag = soup.find("meta", attrs={"name": "description"})
        if meta_tag and meta_tag.get("content"):
            meta_desc = meta_tag["content"].strip()

        # Extract main text content
        text = soup.get_text(separator=" ", strip=True)
        # Clean up whitespace
        text = re.sub(r'\s+', ' ', text).strip()

        if not text and not title:
            return None

        # Extract links
        links = []
        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            absolute_url = urljoin(url, href)
            if absolute_url.startswith(("http://", "https://")):
                links.append(absolute_url)

        # Extract headings for better context
        headings = []
        for h in soup.find_all(["h1", "h2", "h3"]):
            h_text = h.get_text(strip=True)
            if h_text:
                headings.append(h_text)

        return {
            "url": url,
            "title": title,
            "description": meta_desc,
            "content": text,
            "links": links[:50],  # Limit links
            "headings": headings[:20],  # Limit headings
        }

    except requests.exceptions.Timeout:
        logger.error(f"Timeout scraping {url}")
        return None
    except requests.exceptions.SSLError:
        logger.error(f"SSL error for {url}")
        # Retry without SSL verification
        try:
            response = requests.get(url, headers=HEADERS, timeout=TIMEOUT, verify=False)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            title = soup.title.string.strip() if soup.title and soup.title.string else urlparse(url).netloc
            text = re.sub(r'\s+', ' ', soup.get_text(separator=" ", strip=True))
            return {"url": url, "title": title, "description": "", "content": text, "links": [], "headings": []}
        except Exception:
            return None
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error for {url}")
        return None
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error for {url}: {e}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error scraping {url}: {e}")
        return None
