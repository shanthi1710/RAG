from fastapi import APIRouter, File, UploadFile

from app.controller.document_controller import upload_document
from app.models import UploadResponse

router = APIRouter(prefix="/api/documents", tags=["documents"])


@router.post("/upload", response_model=UploadResponse)
async def upload(file: UploadFile = File(...)):
    return await upload_document(file)
