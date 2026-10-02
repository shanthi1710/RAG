from fastapi import HTTPException, UploadFile

from app.models import UploadResponse
from app.service.document_service import save_and_process_pdf


async def upload_document(file: UploadFile) -> UploadResponse:
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported")

    return await save_and_process_pdf(file)
