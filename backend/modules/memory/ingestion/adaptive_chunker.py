import json
import csv
import io


class AdaptiveChunker:

    @staticmethod
    def chunk(text: str, strategy: str) -> list[str]:
        """
        Chunks text based on strategy.
        Returns list of text chunks.
        """

        if strategy == "direct":
            return [text]

        elif strategy == "semantic":
            return AdaptiveChunker._semantic_chunk(text)

        elif strategy == "markdown":
            return AdaptiveChunker._markdown_chunk(text)

        elif strategy == "csv":
            return AdaptiveChunker._csv_chunk(text)

        elif strategy == "json":
            return AdaptiveChunker._json_chunk(text)

        elif strategy == "code":
            return AdaptiveChunker._code_chunk(text)

        elif strategy == "hierarchical":
            return AdaptiveChunker._hierarchical_chunk(text)

        else:
            return AdaptiveChunker._semantic_chunk(text)

    @staticmethod
    def _semantic_chunk(text: str, chunk_size: int = 800, overlap: int = 100) -> list[str]:
        """Standard overlapping character chunks."""
        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunks.append(text[start:end])
            start += chunk_size - overlap
        return chunks

    @staticmethod
    def _hierarchical_chunk(text: str) -> list[str]:
        """
        For very large documents.
        Split by paragraphs first.
        If paragraph too large, split further.
        """
        paragraphs = text.split("\n\n")
        chunks = []
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            if len(para.split()) > 300:
                # Too large — split further
                sub_chunks = AdaptiveChunker._semantic_chunk(para)
                chunks.extend(sub_chunks)
            else:
                chunks.append(para)
        return chunks

    @staticmethod
    def _markdown_chunk(text: str) -> list[str]:
        """Split markdown by headings."""
        lines = text.split("\n")
        chunks = []
        current_chunk = []

        for line in lines:
            if line.startswith("#") and current_chunk:
                chunks.append("\n".join(current_chunk).strip())
                current_chunk = [line]
            else:
                current_chunk.append(line)

        if current_chunk:
            chunks.append("\n".join(current_chunk).strip())

        return [c for c in chunks if c]

    @staticmethod
    def _csv_chunk(text: str, rows_per_chunk: int = 50) -> list[str]:
        """Split CSV by row groups."""
        reader = csv.reader(io.StringIO(text))
        rows = list(reader)
        chunks = []

        for i in range(0, len(rows), rows_per_chunk):
            group = rows[i:i + rows_per_chunk]
            chunk_text = "\n".join([", ".join(row) for row in group])
            chunks.append(chunk_text)

        return chunks

    @staticmethod
    def _json_chunk(text: str) -> list[str]:
        """Split JSON by top level keys."""
        try:
            data = json.loads(text)
            if isinstance(data, list):
                chunks = []
                for i in range(0, len(data), 10):
                    chunk = data[i:i + 10]
                    chunks.append(json.dumps(chunk, indent=2))
                return chunks
            elif isinstance(data, dict):
                chunks = []
                for key, value in data.items():
                    chunks.append(f"{key}: {json.dumps(value, indent=2)}")
                return chunks
        except Exception:
            pass
        return [text]

    @staticmethod
    def _code_chunk(text: str) -> list[str]:
        """Split code by functions and classes."""
        lines = text.split("\n")
        chunks = []
        current_chunk = []

        for line in lines:
            if (line.startswith("def ") or
                line.startswith("class ") or
                line.startswith("function ") or
                line.startswith("public ") or
                line.startswith("private ")):
                if current_chunk:
                    chunks.append("\n".join(current_chunk).strip())
                current_chunk = [line]
            else:
                current_chunk.append(line)

        if current_chunk:
            chunks.append("\n".join(current_chunk).strip())

        return [c for c in chunks if c]