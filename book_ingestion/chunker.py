"""
Module for chunking text content into smaller pieces for embedding.
"""
import re
from typing import List, Dict
from dataclasses import dataclass


@dataclass
class TextChunk:
    """Represents a chunk of text with metadata."""
    id: str
    content: str
    source_url: str
    title: str
    position: int
    metadata: Dict[str, str]


class TextChunker:
    """
    Class for splitting large documents into smaller chunks.
    """

    def __init__(self, chunk_size: int = 512, overlap: int = 50, min_chunk_size: int = 100):
        """
        Initialize the text chunker.

        Args:
            chunk_size: Maximum size of each chunk (in characters)
            overlap: Number of characters to overlap between chunks
            min_chunk_size: Minimum size for a chunk to be included
        """
        self.chunk_size = chunk_size
        self.overlap = overlap
        self.min_chunk_size = min_chunk_size

    def chunk_by_paragraph(self, text: str, source_url: str, title: str) -> List[TextChunk]:
        """
        Split text by paragraphs, then by length if paragraphs are too long.

        Args:
            text: Input text to chunk
            source_url: URL where the text originated
            title: Title of the source document

        Returns:
            List of TextChunk objects
        """
        # Split by paragraphs first
        paragraphs = re.split(r'\n\s*\n', text)
        chunks = []
        chunk_id = 0

        for para_idx, paragraph in enumerate(paragraphs):
            paragraph = paragraph.strip()
            if not paragraph:
                continue

            # If paragraph is smaller than chunk size, use as is
            if len(paragraph) <= self.chunk_size:
                chunks.append(TextChunk(
                    id=f"{source_url}#{chunk_id}",
                    content=paragraph,
                    source_url=source_url,
                    title=title,
                    position=chunk_id,
                    metadata={"paragraph": str(para_idx)}
                ))
                chunk_id += 1
            else:
                # If paragraph is too long, split it further
                sub_chunks = self._split_long_text(paragraph, source_url, title, chunk_id)
                chunks.extend(sub_chunks)
                chunk_id += len(sub_chunks)

        return chunks

    def _split_long_text(self, text: str, source_url: str, title: str, start_id: int) -> List[TextChunk]:
        """
        Split long text into overlapping chunks.

        Args:
            text: Text to split
            source_url: URL where the text originated
            title: Title of the source document
            start_id: Starting ID for chunks

        Returns:
            List of TextChunk objects
        """
        chunks = []
        current_id = start_id

        start = 0
        while start < len(text):
            end = start + self.chunk_size

            # If we're at the end, take the remaining text
            if end > len(text):
                end = len(text)

            # Extract chunk
            chunk_text = text[start:end]

            # Add overlap if not at the end
            if end < len(text) and self.overlap > 0:
                overlap_end = min(end + self.overlap, len(text))
                chunk_text = text[start:overlap_end]

            # Only add if chunk is large enough
            if len(chunk_text) >= self.min_chunk_size:
                chunks.append(TextChunk(
                    id=f"{source_url}#{current_id}",
                    content=chunk_text,
                    source_url=source_url,
                    title=title,
                    position=current_id,
                    metadata={"start_pos": str(start), "end_pos": str(end)}
                ))
                current_id += 1

            # Move start position
            start = end

        return chunks

    def chunk_pages(self, pages: List[Dict[str, str]]) -> List[TextChunk]:
        """
        Chunk a list of crawled pages.

        Args:
            pages: List of page dictionaries from the crawler

        Returns:
            List of TextChunk objects
        """
        all_chunks = []
        for page in pages:
            chunks = self.chunk_by_paragraph(
                page['content'],
                page['url'],
                page['title']
            )
            all_chunks.extend(chunks)

        return all_chunks


def main():
    """
    Main function to demonstrate the text chunker.
    """
    # Example usage
    sample_text = """
    This is the first paragraph of our documentation. It contains important information
    about how the system works. The system is designed to be efficient and scalable.

    The second paragraph continues with more details. It explains additional features
    and capabilities that users should be aware of when implementing the solution.

    Finally, the third paragraph provides a conclusion and summary of the key points.
    It also includes references to other related documentation that might be helpful.
    """

    chunker = TextChunker(chunk_size=100, overlap=20)
    chunks = chunker.chunk_by_paragraph(sample_text, "https://example.com/docs", "Sample Document")

    print(f"Split into {len(chunks)} chunks:")
    for i, chunk in enumerate(chunks):
        print(f"Chunk {i+1} (chars: {len(chunk.content)}): {chunk.content[:50]}...")
        print(f"  ID: {chunk.id}")
        print(f"  Position: {chunk.position}")
        print("-" * 50)


if __name__ == "__main__":
    main()