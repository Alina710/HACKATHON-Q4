"""
Simple test to verify that the backend modules can be imported correctly.
"""
import sys
import os

# Add the backend directory to the path so we can import modules
sys.path.insert(0, os.path.abspath('backend'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")

    try:
        # Import the main components from main.py
        from backend.main import TextCleaner, TextChunker, URLFetcher, Embedder, QdrantStorage, IngestionPipeline
        print("+ All modules imported successfully")
        return True
    except ImportError as e:
        print(f"- Failed to import modules: {e}")
        return False

def test_functionality():
    """Test basic functionality without API keys."""
    print("\nTesting basic functionality...")

    try:
        from backend.main import TextCleaner, TextChunker, URLFetcher

        # Test TextCleaner
        cleaner = TextCleaner()
        sample_html = "<html><body><h1>Title</h1><p>This is a sample paragraph.</p></body></html>"
        cleaned = cleaner.clean_html_content(sample_html)
        print(f"+ TextCleaner processed HTML: '{cleaned[:50]}...'")

        # Test TextChunker
        chunker = TextChunker(chunk_size=100, overlap=20)
        sample_text = "This is a sample text for testing. " * 10  # Repeat to make it longer
        chunks = chunker.chunk_text(sample_text, "https://example.com", "Test Document")
        print(f"+ TextChunker created {len(chunks)} chunks from sample text")

        # Test URLFetcher (without actually fetching)
        fetcher = URLFetcher(delay=0.1)
        print("+ URLFetcher initialized successfully")

        return True
    except Exception as e:
        print(f"- Error in functionality test: {e}")
        return False

def main():
    """Run all tests."""
    print("Running backend module tests...\n")

    imports_ok = test_imports()
    if not imports_ok:
        print("\n[FAILED] Import tests failed!")
        return False

    functionality_ok = test_functionality()
    if not functionality_ok:
        print("\n[FAILED] Basic functionality tests failed!")
        return False

    print("\n[PASSED] All tests passed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)