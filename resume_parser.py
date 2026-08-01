from pypdf import PdfReader
from docx import Document

class ResumeParser:
    def extract(self, file):
        filename = file.name.lower()
        if filename.endswith(".pdf"):
            return self.extract_pdf(file)
        elif filename.endswith(".docx"):
            return self.extract_docx(file)
        else:
            raise ValueError("unsupported file format")
        
    def extract_pdf(self,file):
            reader = PdfReader(file)
            
            text =""
            
            for page in reader.pages:
                page_text = page.extract_text()
                
                if page_text:
                    text+=page_text + "\n"
            return text
                    
    def extract_docx(self,file):
            doc = Document(file)
            
            text =""
            
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n" 
            return text
                   
    