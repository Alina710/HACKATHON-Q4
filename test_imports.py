"""
Simple test to verify that all modules can be imported correctly.
"""
import sys
import os

# Add the project root to the path so we can import modules
sys.path.insert(0, os.path.abspath('.'))

def test_imports():
    """Test that all modules can be imported."""
    print("Testing module imports...")

    try:
        from book_ingestion.crawler import DocusaurusCrawler
        print("+ Crawler module imported successfully")
    except ImportError as e:
        print(f"- Failed to import crawler: {e}")
        return False

    try:
        from book_ingestion.chunker import TextChunker, TextChunk
        print("+ Chunker module imported successfully")
    except ImportError as e:
        print(f"- Failed to import chunker: {e}")
        return False

    try:
        from book_ingestion.embedder import CohereEmbedder
        print("+ Embedder module imported successfully")
    except ImportError as e:
        print(f"- Failed to import embedder: {e}")
        return False

    try:
        from book_ingestion.storage import QdrantStorage
        print("+ Storage module imported successfully")
    except ImportError as e:
        print(f"- Failed to import storage: {e}")
        return False

    try:
        from book_ingestion.pipeline import BookIngestionPipeline
        print("+ Pipeline module imported successfully")
    except ImportError as e:
        print(f"- Failed to import pipeline: {e}")
        return False

    try:
        import yaml
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)
        print("+ Configuration file loaded successfully")
    except Exception as e:
        print(f"- Failed to load configuration: {e}")
        return False

    print("\nAll imports successful!")
    return True

def test_basic_functionality():
    """Test basic functionality of the modules."""
    print("\nTesting basic functionality...")

    # Test chunker
    try:
        from book_ingestion.chunker import TextChunker
        chunker = TextChunker(chunk_size=100, overlap=20)
        sample_text = "This is a sample text for testing. " * 10  # Repeat to make it longer
        chunks = chunker.chunk_by_paragraph(sample_text, "https://example.com", "Test Document")
        print(f"+ Chunker created {len(chunks)} chunks from sample text")
    except Exception as e:
        print(f"- Chunker test failed: {e}")
        return False

    # Test configuration loading
    try:
        import yaml
        with open('config.yaml', 'r') as f:
            config = yaml.safe_load(f)

        crawler_config = config.get('CRAWLER', {})
        chunker_config = config.get('CHUNKER', {})
        print(f"+ Configuration loaded with CRAWLER: {crawler_config.get('DELAY')}s delay")
    except Exception as e:
        print(f"- Configuration test failed: {e}")
        return False

    print("\nAll basic functionality tests passed!")
    return True

def main():
    """Run all tests."""
    print("Running import and basic functionality tests...\n")

    imports_ok = test_imports()
    if not imports_ok:
        print("\n[FAILED] Import tests failed!")
        return False

    functionality_ok = test_basic_functionality()
    if not functionality_ok:
        print("\n[FAILED] Basic functionality tests failed!")
        return False

    print("\n[PASSED] All tests passed successfully!")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)