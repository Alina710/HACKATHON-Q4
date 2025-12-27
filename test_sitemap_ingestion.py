"""
Test script to verify sitemap functionality for the documentation site.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from book_ingestion.sitemap_parser import SitemapParser
from book_ingestion.sitemap_enhanced_crawler import SitemapEnhancedCrawler


def test_sitemap_parsing():
    """Test the sitemap parser functionality."""
    print("Testing Sitemap Parser...")
    parser = SitemapParser(delay=0.5)

    # Test with the target domain
    domain_url = "https://hackathon-q4-murex.vercel.app"
    urls = parser.get_all_urls_from_domain(domain_url)

    print(f"Found {len(urls)} URLs from sitemap:")
    for i, url in enumerate(urls):
        print(f"  {i+1:2d}. {url}")

    # Filter for documentation pages
    doc_urls = [url for url in urls if '/docs/' in url]
    print(f"\nFound {len(doc_urls)} documentation URLs:")
    for i, url in enumerate(doc_urls):
        print(f"  {i+1:2d}. {url}")

    return urls


def test_crawler_with_sitemap():
    """Test the sitemap-enhanced crawler functionality."""
    print("\nTesting Sitemap-Enhanced Crawler...")

    urls = ["https://hackathon-q4-murex.vercel.app"]
    crawler = SitemapEnhancedCrawler(
        base_urls=urls,
        delay=1.0,
        max_pages=50
    )

    print("Starting crawl with sitemap-enhanced crawler...")
    pages = crawler.crawl()

    print(f"Crawled {len(pages)} pages:")
    for i, page in enumerate(pages):
        print(f"  {i+1:2d}. {page['title'][:50]}... - {page['url']}")

    return pages


if __name__ == "__main__":
    print("Testing sitemap-based ingestion functionality...")
    print("=" * 50)

    # Test sitemap parsing
    sitemap_urls = test_sitemap_parsing()

    # Test crawler with sitemap
    crawled_pages = test_crawler_with_sitemap()

    print("\n" + "=" * 50)
    print("Test completed successfully!")
    print(f"Total URLs from sitemap: {len(sitemap_urls)}")
    print(f"Total pages crawled: {len(crawled_pages)}")
    print(f"Documentation pages found: {len([url for url in sitemap_urls if '/docs/' in url])}")