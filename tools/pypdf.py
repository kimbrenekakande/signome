
from crewai.tools import BaseTool
from pydantic import BaseModel, Field
import pypdf
from typing import Type


class PDFReaderInput(BaseModel):
    """Input schema for PDFReaderTool."""
    file_path: str = Field(..., description="Path to the PDF file to read")

class pypdfTool(BaseTool):
    name: str = "PDF Reader"
    description: str = "Reads and extracts all text content from a PDF file"
    args_schema: Type[BaseModel] = PDFReaderInput

    def _run(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = pypdf.PdfReader(file)
                text = ""
                for page_num, page in enumerate(pdf_reader.pages, 1):
                    text += f"\n## Page {page_num}\n\n"
                    text += page.extract_text() + "\n"
                
                # Save to markdown file
                import os
                os.makedirs('output', exist_ok=True)
                output_path = 'output/raw.md'
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(text)
                    
                return f'PDF text extracted and saved to {output_path}'
        except Exception as e:
            return f"Error reading PDF: {str(e)}"