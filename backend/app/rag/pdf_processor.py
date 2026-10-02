from pypdf import PdfReader


def get_pdf_page_count(file_path: str) -> int:
    reader = PdfReader(file_path)
    return len(reader.pages)


def extract_pages_from_pdf(file_path: str) -> list[str]:
    reader = PdfReader(file_path)
    return [page.extract_text() or "" for page in reader.pages]
