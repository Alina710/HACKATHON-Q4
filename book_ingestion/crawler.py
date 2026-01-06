"""
Module for crawling Docusaurus documentation sites and extracting content.
"""
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
from typing import List, Set, Dict, Optional
import logging

logger = logging.getLogger(__name__)

class DocusaurusCrawler:
    """
    Crawler specifically designed for Docusaurus documentation sites.
    """

    def __init__(self, base_urls: List[str], delay: float = 1.0, max_pages: int = 100):
        """
        Initialize the crawler.

        Args:
            base_urls: List of base URLs to crawl
            delay: Delay between requests in seconds
            max_pages: Maximum number of pages to crawl
        """
        self.base_urls = base_urls
        self.delay = delay
        self.max_pages = max_pages
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; DocusaurusCrawler/1.0; +http://example.com/bot)'
        })

    def is_valid_url(self, url: str) -> bool:
        """
        Check if a URL is valid and within the allowed domains.
        """
        parsed = urllib.parse.urlparse(url)
        for base_url in self.base_urls:
            base_parsed = urllib.parse.urlparse(base_url)
            if parsed.netloc == base_parsed.netloc:
                return True
        return False

    def extract_content(self, html: str, url: str) -> Dict[str, str]:
        """
        Extract content from Docusaurus HTML page.

        Args:
            html: HTML content of the page
            url: URL of the page

        Returns:
            Dictionary containing title, content, and metadata
        """
        soup = BeautifulSoup(html, 'html.parser')

        # Remove script and style elements
        for script in soup(["script", "style"]):
            script.decompose()

        # Try to find the main content area in Docusaurus sites
        # Common selectors for Docusaurus content
        content_selectors = [
            '[class*="docItemContainer"]',
            '[class*="docContent"]',
            '[class*="main-wrapper"]',
            '[class*="container"]',
            'main',
            '.main-content',
            '.docs-content',
            '.theme-doc-markdown'
        ]

        content_element = None
        for selector in content_selectors:
            content_element = soup.select_one(selector)
            if content_element:
                break

        # If no specific content area found, use body
        if not content_element:
            content_element = soup.find('body')

        # Extract title
        title_tag = soup.find('title')
        title = title_tag.get_text().strip() if title_tag else ''

        # Extract content text
        content_text = ''
        if content_element:
            # Remove navigation elements that might be in the main content
            for nav in content_element.select('nav, .navbar, .sidebar, .menu'):
                nav.decompose()
            content_text = content_element.get_text(separator=' ', strip=True)

        # Clean up the text
        import re
        content_text = re.sub(r'\s+', ' ', content_text)

        return {
            'url': url,
            'title': title,
            'content': content_text,
            'html': str(soup)
        }

    def crawl(self) -> List[Dict[str, str]]:
        """
        Crawl all pages starting from base URLs.

        Returns:
            List of dictionaries containing page content and metadata
        """
        visited_urls: Set[str] = set()
        pages_to_crawl: List[str] = list(self.base_urls)
        crawled_pages = []

        while pages_to_crawl and len(visited_urls) < self.max_pages:
            current_url = pages_to_crawl.pop(0)

            if current_url in visited_urls:
                continue

            visited_urls.add(current_url)

            try:
                logger.info(f"Crawling: {current_url}")
                response = self.session.get(current_url, timeout=30)
                response.raise_for_status()

                # Check if it's HTML content
                content_type = response.headers.get('content-type', '')
                if 'text/html' not in content_type.lower():
                    continue

                # Extract content
                page_data = self.extract_content(response.text, current_url)
                crawled_pages.append(page_data)

                # Find links in the page
                soup = BeautifulSoup(response.text, 'html.parser')
                for link in soup.find_all('a', href=True):
                    href = link['href']
                    absolute_url = urllib.parse.urljoin(current_url, href)

                    # Normalize URL
                    parsed = urllib.parse.urlparse(absolute_url)
                    normalized_url = urllib.parse.urlunparse(
                        (parsed.scheme, parsed.netloc, parsed.path, '', parsed.query, '')
                    )

                    # Only add if it's a valid URL within our domain and not already visited
                    if (self.is_valid_url(normalized_url) and
                        normalized_url not in visited_urls and
                        normalized_url not in pages_to_crawl):
                        # Check if it's likely a documentation page
                        path = parsed.path.lower()
                        if (path.endswith('.html') or
                            not any(ext in path for ext in ['.pdf', '.jpg', '.png', '.css', '.js'])):
                            pages_to_crawl.append(normalized_url)

                # Be respectful with delays
                time.sleep(self.delay)

            except requests.RequestException as e:
                logger.error(f"Error crawling {current_url}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error crawling {current_url}: {str(e)}")
                continue

        logger.info(f"Crawled {len(crawled_pages)} pages")
        return crawled_pages


def main():
    """
    Main function to demonstrate the crawler.
    """
    # Example usage
    urls = [
        "https://docusaurus.io/docs"  # Example URL - replace with actual URLs
    ]

    crawler = DocusaurusCrawler(
        base_urls=urls,
        delay=1.0,
        max_pages=50
    )

    pages = crawler.crawl()

    # Print summary
    for i, page in enumerate(pages[:5]):  # Show first 5 pages
        print(f"Page {i+1}: {page['title'][:100]}...")
        print(f"URL: {page['url']}")
        print(f"Content length: {len(page['content'])} characters")
        print("-" * 50)


if __name__ == "__main__":
    main()