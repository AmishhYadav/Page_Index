from app.api.v1 import documents
from app.services.ingestion import IngestionService
import logging

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
        pages_data = processor.process_pdf(pdf_bytes)
        
        ingest_service = IngestionService(db)
        db_doc = ingest_service.ingest_document(file.filename, pages_data)
        
        return IngestionResponse(
            document_id=db_doc.id,
            status=db_doc.status,
            message=f"Document '{file.filename}' processed and indexed successfully."
        )
    except Exception as e:
        logger.error(f"Error processing document {file.filename}: {str(e)}", exc_info=True)
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail="Error processing document.")
