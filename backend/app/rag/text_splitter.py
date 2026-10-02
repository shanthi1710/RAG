from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHUNK_SIZE = 500
CHUNK_OVERLAP = 50


def split_pages_into_chunks(pages: list[str]) -> list[Document]:
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )

    documents = []
    for page_number, page_text in enumerate(pages, start=1):
        for chunk_text in splitter.split_text(page_text):
            documents.append(Document(page_content=chunk_text, metadata={"page": page_number}))

    return documents
