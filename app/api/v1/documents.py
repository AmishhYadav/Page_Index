from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.document import IngestionResponse
from app.services.pdf_processor import PDFProcessor
import logging
import uuid

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/", response_model=IngestionResponse)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """
    Upload a PDF document for hierarchical ingestion.
    """
    if not file.filename.endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")

    logger.info(f"Received document upload: {file.filename}")
    
    try:
        pdf_bytes = await file.read()
        processor = PDFProcessor()
        # For Wave 2, we just parse it to verify the flow is working.
        # Wave 3 will handle the actual database persistence logic.
        results = processor.process_pdf(pdf_bytes)
        
        # Temporary UUID for Wave 2 response
        doc_id = uuid.uuid4()
        
        return IngestionResponse(
            document_id=doc_id,
            status="received",
            message=f"Document '{file.filename}' processed successfully. Found {len(results)} pages."
        )
    except Exception as e:
        logger.error(f"Error processing document {file.filename}: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing document.")
