class Chunker:

    @staticmethod
    def chunk_text(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
        """
        Splits large text into smaller overlapping chunks.

        chunk_size: number of characters per chunk
        overlap: how many characters repeat between chunks
        """
        chunks = []
        start = 0

        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start += chunk_size - overlap

        return chunks