import fitz  # PyMuPDF
import json
import csv
import io


class ContentExtractor:

    @staticmethod
    def extract(file_bytes: bytes, file_type: str) -> str:
        """
        Extracts text from file bytes based on file type.
        Returns plain text string.
        """

        if file_type == "pdf":
            return ContentExtractor._extract_pdf(file_bytes)

        elif file_type == "txt":
            return ContentExtractor._extract_txt(file_bytes)

        elif file_type == "markdown":
            return ContentExtractor._extract_txt(file_bytes)

        elif file_type == "json":
            return ContentExtractor._extract_json(file_bytes)

        elif file_type == "csv":
            return ContentExtractor._extract_csv(file_bytes)

        elif file_type == "code":
            return ContentExtractor._extract_txt(file_bytes)

        elif file_type == "text_snippet":
            return file_bytes.decode("utf-8") if isinstance(file_bytes, bytes) else file_bytes

        else:
            return file_bytes.decode("utf-8", errors="ignore")

    @staticmethod
    def _extract_pdf(file_bytes: bytes) -> str:
        text = ""
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text.strip()

    @staticmethod
    def _extract_txt(file_bytes: bytes) -> str:
        return file_bytes.decode("utf-8", errors="ignore").strip()

    @staticmethod
    def _extract_json(file_bytes: bytes) -> str:
        try:
            data = json.loads(file_bytes.decode("utf-8"))
            return json.dumps(data, indent=2)
        except Exception:
            return file_bytes.decode("utf-8", errors="ignore")

    @staticmethod
    def _extract_csv(file_bytes: bytes) -> str:
        try:
            text = file_bytes.decode("utf-8", errors="ignore")
            reader = csv.reader(io.StringIO(text))
            rows = []
            for row in reader:
                rows.append(", ".join(row))
            return "\n".join(rows)
        except Exception:
            return file_bytes.decode("utf-8", errors="ignore")