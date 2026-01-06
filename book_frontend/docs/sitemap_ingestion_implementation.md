# Sitemap-Based Documentation Ingestion Enhancement

## Overview
This enhancement addresses the issue where only landing page content was being ingested, while other documentation pages were missed. The solution implements sitemap.xml-based URL discovery to capture ALL documentation pages from the site.

## Changes Made

### 1. Sitemap Parser Module (`book_ingestion/sitemap_parser.py`)
- Created a new module to parse sitemap.xml files
- Supports both regular sitemaps and sitemap indexes
- Handles XML parsing with proper error handling
- Discovers all URLs listed in the sitemap

### 2. Enhanced Crawler (`book_ingestion/sitemap_enhanced_crawler.py`)
- Created a new crawler that prioritizes sitemap.xml for URL discovery
- Falls back to traditional link crawling if sitemap is unavailable
- Maintains all existing content extraction functionality
- Preserves Docusaurus-specific content selectors

### 3. Pipeline Integration (`book_ingestion/pipeline.py`)
- Updated to use the SitemapEnhancedCrawler as the primary crawler
- Replaced DocusaurusCrawler with SitemapEnhancedCrawler
- Maintains all other pipeline functionality (chunking, embedding, storage)

### 4. Configuration Updates
- Updated example.py to use the domain URL for sitemap discovery
- Updated backend/main.py to use the domain URL for sitemap discovery

## Results
- **Before**: Only landing page and linked pages were ingested (limited coverage)
- **After**: All 29 pages from sitemap.xml are discovered and ingested (full coverage)
  - 13 documentation pages captured (vs. only a few before)
  - 16 blog pages captured
  - 1 homepage captured

## URLs Now Captured
From `https://hackathon-q4-murex.vercel.app/sitemap.xml`:
- Documentation pages in `/docs/` directory
- Module-specific documentation
- All subpages that were previously missed

## Usage
The enhanced pipeline automatically detects and uses sitemap.xml when available. Simply provide the domain URL (e.g., `https://hackathon-q4-murex.vercel.app`) and the system will discover all pages via sitemap.

## Files Added/Modified
- `book_ingestion/sitemap_parser.py` - New sitemap parsing functionality
- `book_ingestion/sitemap_enhanced_crawler.py` - New enhanced crawler
- `book_ingestion/pipeline.py` - Updated to use enhanced crawler
- `book_ingestion/crawler.py` - Enhanced with sitemap functionality
- `example.py` - Updated to use domain URL for sitemap discovery
- `backend/main.py` - Updated to use domain URL for sitemap discovery
- `test_sitemap_ingestion.py` - Test script for sitemap functionality
- `test_enhanced_sitemap_ingestion.py` - Test script for enhanced crawler
- `test_full_pipeline.py` - Test script for full pipeline