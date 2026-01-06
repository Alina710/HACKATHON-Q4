"""
Module for parsing sitemap.xml files and extracting URLs.
"""
import requests
from bs4 import BeautifulSoup
from typing import List
import urllib.parse
import logging

logger = logging.getLogger(__name__)


class SitemapParser:
    """
    Parser for sitemap.xml files to extract URLs.
    """

    def __init__(self, delay: float = 1.0):
        """
        Initialize the sitemap parser.

        Args:
            delay: Delay between requests in seconds
        """
        self.delay = delay
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (compatible; SitemapParser/1.0; +http://example.com/bot)'
        })

    def parse_sitemap(self, sitemap_url: str) -> List[str]:
        """
        Parse a sitemap.xml file and extract all URLs.

        Args:
            sitemap_url: URL to the sitemap.xml file

        Returns:
            List of URLs extracted from the sitemap
        """
        try:
            logger.info(f"Parsing sitemap: {sitemap_url}")
            response = self.session.get(sitemap_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')

            # Find all <url> elements and extract the <loc> values
            urls = []
            for url_element in soup.find_all('url'):
                loc_element = url_element.find('loc')
                if loc_element and loc_element.text:
                    urls.append(loc_element.text.strip())

            logger.info(f"Found {len(urls)} URLs in sitemap")
            return urls

        except Exception as e:
            logger.error(f"Error parsing sitemap {sitemap_url}: {str(e)}")
            return []

    def parse_sitemap_index(self, sitemap_index_url: str) -> List[str]:
        """
        Parse a sitemap index file that may contain multiple sitemaps.

        Args:
            sitemap_index_url: URL to the sitemap index file

        Returns:
            List of URLs from all sitemaps referenced in the index
        """
        try:
            logger.info(f"Parsing sitemap index: {sitemap_index_url}")
            response = self.session.get(sitemap_index_url, timeout=30)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'xml')

            all_urls = []

            # Check if this is a sitemap index with multiple sitemaps
            sitemap_elements = soup.find_all('sitemap')
            if sitemap_elements:
                # This is a sitemap index, parse each sitemap
                for sitemap_element in sitemap_elements:
                    loc_element = sitemap_element.find('loc')
                    if loc_element and loc_element.text:
                        sitemap_url = loc_element.text.strip()
                        sitemap_urls = self.parse_sitemap(sitemap_url)
                        all_urls.extend(sitemap_urls)
            else:
                # This is a regular sitemap, not an index
                all_urls = self.parse_sitemap(sitemap_index_url)

            return all_urls

        except Exception as e:
            logger.error(f"Error parsing sitemap index {sitemap_index_url}: {str(e)}")
            return []

    def get_all_urls_from_domain(self, base_url: str) -> List[str]:
        """
        Get all URLs from a domain by checking for sitemap.xml and parsing it.

        Args:
            base_url: Base URL of the domain (e.g., https://example.com)

        Returns:
            List of all URLs found in the sitemap(s)
        """
        # Try to find sitemap at common locations
        sitemap_urls = [
            urllib.parse.urljoin(base_url, 'sitemap.xml'),
            urllib.parse.urljoin(base_url, '/sitemap.xml'),
            urllib.parse.urljoin(base_url, 'sitemap_index.xml'),
            urllib.parse.urljoin(base_url, '/sitemap_index.xml')
        ]

        all_urls = []
        for sitemap_url in sitemap_urls:
            logger.info(f"Checking for sitemap at: {sitemap_url}")
            try:
                # First check if the sitemap exists
                head_response = self.session.head(sitemap_url, timeout=10)
                if head_response.status_code == 200:
                    # Parse the sitemap
                    sitemap_urls_result = self.parse_sitemap_index(sitemap_url)
                    all_urls.extend(sitemap_urls_result)
                    break  # Found and parsed a sitemap, so break
            except Exception as e:
                logger.debug(f"Sitemap not found at {sitemap_url}: {str(e)}")
                continue

        # Remove duplicates while preserving order
        unique_urls = list(dict.fromkeys(all_urls))
        logger.info(f"Total unique URLs found from sitemap(s): {len(unique_urls)}")

        return unique_urls


def main():
    """
    Main function to demonstrate the sitemap parser.
    """
    import os
    import sys

    if len(sys.argv) < 2:
        print("Usage: python sitemap_parser.py <sitemap_url_or_domain>")
        print("Example: python sitemap_parser.py https://hackathon-q4-murex.vercel.app")
        return

    target = sys.argv[1]

    parser = SitemapParser(delay=1.0)

    if target.endswith('sitemap.xml'):
        # If it's a direct sitemap URL
        urls = parser.parse_sitemap_index(target)
    else:
        # If it's a domain, try to find the sitemap
        urls = parser.get_all_urls_from_domain(target)

    print(f"Found {len(urls)} URLs:")
    for i, url in enumerate(urls, 1):
        print(f"{i:3d}. {url}")
        if i >= 20:  # Limit output for large sitemaps
            print(f"... and {len(urls) - 20} more URLs")
            break


if __name__ == "__main__":
    main()