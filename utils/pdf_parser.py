"""PDF extraction utilities."""
import io

from pypdf import PdfReader


class PDFParser:
    @staticmethod
    def extract_text(pdf_file: bytes) -> str:
        try:
            reader = PdfReader(io.BytesIO(pdf_file))
            return "\n".join(page.extract_text() or "" for page in reader.pages)
        except Exception as exc:
            return f"Error parsing PDF: {exc}"

    @staticmethod
    def extract_text_from_path(pdf_path: str) -> str:
        try:
            with open(pdf_path, "rb") as handle:
                return PDFParser.extract_text(handle.read())
        except Exception as exc:
            return f"Error reading PDF: {exc}"

    @staticmethod
    def is_valid_pdf(pdf_file: bytes) -> bool:
        try:
            PdfReader(io.BytesIO(pdf_file))
            return True
        except Exception:
            return False
