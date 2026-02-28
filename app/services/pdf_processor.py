import fitz  # PyMuPDF
import io
from typing import List, Dict, Any
import logging

logger = logging.getLogger(__name__)

class PDFProcessor:
    """
    Service to extract hierarchical text (Page -> Section) from PDF documents.
    """
    def __init__(self, min_header_size: float = 12.0):
        self.min_header_size = min_header_size

    def process_pdf(self, pdf_bytes: bytes) -> List[Dict[str, Any]]:
        """
        Processes PDF bytes and returns a structured hierarchy of pages and sections.
        """
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages_data = []

        for page_num, page in enumerate(doc):
            blocks = page.get_text("dict")["blocks"]
            sections = []
            current_section = {
                "title": f"Page {page_num + 1} Introduction",
                "content": "",
                "section_index": 0
            }
            section_count = 1

            for b in blocks:
                if "lines" in b:
                    for l in b["lines"]:
                        for s in l["spans"]:
                            text = s["text"].strip()
                            if not text:
                                continue
                            
                            # Heuristic for header: Font size > min_header_size or Bold
                            # Note: flags bit 4 is bold
                            is_bold = s["flags"] & 2**4
                            if s["size"] >= self.min_header_size or is_bold:
                                # Start a new section if we have content in the current one
                                if current_section["content"].strip():
                                    sections.append(current_section)
                                    current_section = {
                                        "title": text,
                                        "content": "",
                                        "section_index": section_count
                                    }
                                    section_count += 1
                                else:
                                    # If current section is empty, just update the title
                                    current_section["title"] = text
                            else:
                                current_section["content"] += text + " "

            # Add the last section of the page
            if current_section["content"].strip() or current_section["title"]:
                sections.append(current_section)

            pages_data.append({
                "page_number": page_num + 1,
                "sections": sections
            })

        doc.close()
        return pages_data
