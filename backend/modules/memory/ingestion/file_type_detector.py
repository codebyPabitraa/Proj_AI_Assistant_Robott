import os


class FileTypeDetector:

    # Supported file types
    PDF = "pdf"
    DOCX = "docx"
    TXT = "txt"
    MARKDOWN = "markdown"
    CSV = "csv"
    JSON = "json"
    CODE = "code"
    UNKNOWN = "unknown"

    # Code file extensions
    CODE_EXTENSIONS = {
        ".py", ".js", ".ts", ".java", ".cpp", ".c",
        ".cs", ".go", ".rb", ".php", ".swift", ".kt"
    }

    @staticmethod
    def detect(filename: str) -> str:
        """
        Detects file type from filename extension.
        Returns a string type constant.
        """
        ext = os.path.splitext(filename)[1].lower()

        if ext == ".pdf":
            return FileTypeDetector.PDF
        elif ext == ".docx":
            return FileTypeDetector.DOCX
        elif ext == ".txt":
            return FileTypeDetector.TXT
        elif ext in (".md", ".markdown"):
            return FileTypeDetector.MARKDOWN
        elif ext == ".csv":
            return FileTypeDetector.CSV
        elif ext == ".json":
            return FileTypeDetector.JSON
        elif ext in FileTypeDetector.CODE_EXTENSIONS:
            return FileTypeDetector.CODE
        else:
            return FileTypeDetector.UNKNOWN

    @staticmethod
    def detect_from_text(text: str) -> str:
        """
        Detects type from raw text input (no file).
        Used for short notes, voice transcripts, etc.
        """
        return "text_snippet"