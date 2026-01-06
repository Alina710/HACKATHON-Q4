"""
Enhanced crawler that uses sitemap.xml for comprehensive documentation ingestion.
"""
import requests
from bs4 import BeautifulSoup
import time
import urllib.parse
from typing import List, Set, Dict, Optional
import logging
import re

# Import the sitemap parser
from book_ingestion.sitemap_parser import SitemapParser

logger = logging.getLogger(__name__)


class SitemapEnhancedCrawler:
    """
    Enhanced crawler that prioritizes sitemap.xml for comprehensive URL discovery.
    """

    def __init__(self, base_urls: List[str], delay: float = 1.0, max_pages: int = 100):
        """
        Initialize the enhanced crawler.

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
            'User-Agent': 'Mozilla/5.0 (compatible; SitemapEnhancedCrawler/1.0; +http://example.com/bot)'
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
        content_text = re.sub(r'\s+', ' ', content_text)

        return {
            'url': url,
            'title': title,
            'content': content_text,
            'html': str(soup)
        }

    def get_urls_from_sitemap(self) -> List[str]:
        """
        Get all URLs from the sitemap.xml of the base domains.

        Returns:
            List of URLs extracted from sitemap(s)
        """
        all_urls = []

        for base_url in self.base_urls:
            try:
                logger.info(f"Attempting to get URLs from sitemap for: {base_url}")
                parser = SitemapParser(delay=self.delay)
                domain_urls = parser.get_all_urls_from_domain(base_url)
                all_urls.extend(domain_urls)
            except Exception as e:
                logger.error(f"Error getting URLs from sitemap for {base_url}: {str(e)}")
                # Continue with other base URLs if one fails

        # Remove duplicates while preserving order
        unique_urls = list(dict.fromkeys(all_urls))
        logger.info(f"Total unique URLs found from sitemap(s): {len(unique_urls)}")

        return unique_urls

    def crawl(self) -> List[Dict[str, str]]:
        """
        Crawl all pages using sitemap.xml for comprehensive URL discovery.

        Returns:
            List of dictionaries containing page content and metadata
        """
        logger.info("Attempting to use sitemap for URL discovery...")
        sitemap_urls = self.get_urls_from_sitemap()

        if not sitemap_urls:
            logger.warning("No sitemap found, falling back to basic crawling from base URLs")
            sitemap_urls = self.base_urls

        # Filter URLs to only include valid ones
        pages_to_crawl = [url for url in sitemap_urls if self.is_valid_url(url)]
        # Limit to max_pages if needed
        pages_to_crawl = pages_to_crawl[:self.max_pages]

        logger.info(f"Will crawl {len(pages_to_crawl)} URLs found from sitemap")
        crawled_pages = []

        for current_url in pages_to_crawl:
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

                # Be respectful with delays
                time.sleep(self.delay)

            except requests.RequestException as e:
                logger.error(f"Error crawling {current_url}: {str(e)}")
                continue
            except Exception as e:
                logger.error(f"Unexpected error crawling {current_url}: {str(e)}")
                continue

        logger.info(f"Crawled {len(crawled_pages)} pages using sitemap-enhanced approach")
        return crawled_pages


def main():
    """
    Main function to demonstrate the enhanced crawler.
    """
    # Example usage
    urls = [
        "https://hackathon-q4-murex.vercel.app"  # Updated to use the actual site
    ]

    crawler = SitemapEnhancedCrawler(
        base_urls=urls,
        delay=1.0,
        max_pages=50
    )

    pages = crawler.crawl()

    # Print summary
    for i, page in enumerate(pages[:10]):  # Show first 10 pages
        print(f"Page {i+1}: {page['title'][:100]}...")
        print(f"URL: {page['url']}")
        print(f"Content length: {len(page['content'])} characters")
        print("-" * 50)


if __name__ == "__main__":
    main()