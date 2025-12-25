from langchain_text_splitters import RecursiveCharacterTextSplitter
import pdfplumber
import easyocr
import numpy as np

class IngestionAgent:
    
    def __init__(self):
        """Initialize EasyOCR reader (loads model once)"""
        try:
            self.ocr_reader = easyocr.Reader(['en'], gpu=False)
        except Exception as e:
            print(f"Warning: Could not initialize OCR: {e}")
            self.ocr_reader = None

    def extract_text(self, file_path):
        if file_path.endswith(".pdf"):
            return self._extract_from_pdf(file_path)
        else:
            return self._extract_from_image(file_path)
    
    def _extract_from_image(self, image_path):
        """Extract text from image using EasyOCR"""
        if not self.ocr_reader:
            return ""
        try:
            result = self.ocr_reader.readtext(image_path)
            return " ".join([text[1] for text in result])
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return ""

    def _extract_from_pdf(self, file_path):
        """Extract text from PDF, handling both text and scanned images"""
        text_content = ""
        
        # First, try to extract text using pdfplumber
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    extracted_text = page.extract_text()
                    if extracted_text:
                        text_content += extracted_text + " "
                    
                    # Check if page has images (likely scanned)
                    try:
                        page_images = page.images
                        if page_images and (not extracted_text or len(extracted_text.strip()) < 20):
                            # This page has images and little text, mark for OCR
                            pass
                    except:
                        pass
        except Exception as e:
            print(f"Error extracting text with pdfplumber: {e}")
        
        # If little to no text extracted, use OCR by converting pages to images
        if not text_content or len(text_content.strip()) < 50:
            if not self.ocr_reader:
                return text_content
                
            try:
                print("Using EasyOCR for scanned PDF pages...")
                with pdfplumber.open(file_path) as pdf:
                    for i, page in enumerate(pdf.pages):
                        try:
                            # Convert PDF page to image
                            im = page.to_image()
                            if im:
                                # Convert PIL Image to numpy array for EasyOCR
                                img_array = np.array(im.original)
                                ocr_result = self.ocr_reader.readtext(img_array)
                                ocr_text = " ".join([text[1] for text in ocr_result])
                                text_content += ocr_text + " "
                        except Exception as e:
                            print(f"Error processing page {i} with OCR: {e}")
                            continue
            except Exception as e:
                print(f"Error in OCR process: {e}")
                
        return text_content
                
        return text_content

    def process(self, file_path):
        text = self.extract_text(file_path)

        splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=100
        )
        return splitter.split_text(text)
