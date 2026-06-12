import fitz  # PyMuPDF

class PDFExtractor:

    @staticmethod
    def extract_text(file_bytes: bytes) -> str:
        """
        Takes PDF as bytes.
        Returns full extracted text as string.
        """
        text = ""

        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()

        return text.strip()