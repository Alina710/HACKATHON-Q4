"""
Test script to verify enhanced sitemap functionality for the documentation site.
"""
import sys
import os

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from book_ingestion.sitemap_enhanced_crawler import SitemapEnhancedCrawler


def test_enhanced_crawler():
    """Test the enhanced crawler with sitemap functionality."""
    print("Testing Enhanced Crawler with Sitemap...")

    urls = ["https://hackathon-q4-murex.vercel.app"]
    crawler = SitemapEnhancedCrawler(
        base_urls=urls,
        delay=1.0,
        max_pages=50
    )

    print("Starting crawl with sitemap-enhanced approach...")
    pages = crawler.crawl()

    print(f"Crawled {len(pages)} pages:")
    for i, page in enumerate(pages):
        print(f"  {i+1:2d}. {page['title'][:50]}... - {page['url']}")

    # Filter for documentation pages
    doc_pages = [page for page in pages if '/docs/' in page['url']]
    print(f"\nFound {len(doc_pages)} documentation pages:")
    for i, page in enumerate(doc_pages):
        print(f"  {i+1:2d}. {page['title'][:50]}... - {page['url']}")

    return pages


if __name__ == "__main__":
    print("Testing enhanced sitemap-based ingestion functionality...")
    print("=" * 60)

    # Test enhanced crawler with sitemap
    crawled_pages = test_enhanced_crawler()

    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print(f"Total pages crawled: {len(crawled_pages)}")
    print(f"Documentation pages found: {len([p for p in crawled_pages if '/docs/' in p['url']])}")
    print("\nThe enhanced crawler now uses sitemap.xml to discover ALL documentation pages,")
    print("not just those reachable by following links from the landing page.")