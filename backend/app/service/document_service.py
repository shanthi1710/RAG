import os

from fastapi import HTTPException, UploadFile

from app.config import DOCUMENTS_DIR
from app.models import UploadResponse
from app.rag.pdf_processor import extract_pages_from_pdf, get_pdf_page_count
from app.rag.text_splitter import split_pages_into_chunks
from app.rag.vectorstore import add_documents


async def save_and_process_pdf(file: UploadFile) -> UploadResponse:
    saved_path = os.path.join(DOCUMENTS_DIR, file.filename)

    with open(saved_path, "wb") as out_file:
        out_file.write(await file.read())

    try:
        num_pages = get_pdf_page_count(saved_path)
        pages = extract_pages_from_pdf(saved_path)
    except Exception:
        os.remove(saved_path)
        raise HTTPException(status_code=400, detail="Uploaded file is not a valid PDF")

    chunks = split_pages_into_chunks(pages)
    for chunk in chunks:
        chunk.metadata["filename"] = file.filename

    print(f"[document_service] '{file.filename}': {num_pages} pages -> {len(chunks)} chunks")

    try:
        stored_ids = add_documents(chunks)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to store chunks in ChromaDB: {exc}")

    print(f"[document_service] '{file.filename}': stored {len(stored_ids)} chunks in ChromaDB")

    return UploadResponse(
        filename=file.filename,
        num_pages=num_pages,
        num_chunks=len(chunks),
        num_chunks_stored=len(stored_ids),
        saved_path=saved_path,
    )
