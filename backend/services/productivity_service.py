import logging
import os
from modules.helper import loadConfig
from modules.llm import LLM
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class ProductivityService:
    """Service class for productivity-related operations."""
    
    def __init__(self):
        self.llm = LLM()
    
    def generate_meeting_minutes(self, file_content: bytes, filename: str, template: str = "discussion") -> str:
        """
        Generate meeting minutes from uploaded transcript files.
        
        Args:
            file_content: The raw file content as bytes
            filename: The name of the uploaded file
            template: The template type to use for meeting summary generation
            
        Returns:
            str: The generated meeting summary
        """
        try:
            # Validate file type (TXT and DOCX only for deployment stability)
            allowed_extensions = {'.txt', '.docx'}
            file_extension = os.path.splitext(filename.lower())[1] if filename else '.txt'
            
            if file_extension not in allowed_extensions:
                raise ValueError(f"Unsupported file format '{file_extension}'. Supported formats: TXT, DOCX")
            
            # Validate file size (10MB max for deployment stability)
            file_size = len(file_content)
            max_file_size = 10 * 1024 * 1024  # 10MB
            if file_size > max_file_size:
                raise ValueError(f"File too large. Maximum size is 10MB, received {file_size / (1024*1024):.1f}MB")
            
            if file_size == 0:
                raise ValueError("Empty file provided. Please upload a file with content.")
            
            # Process the file content
            transcript_text = self._extract_text_from_file(file_content, file_extension)
            
            # Validate extracted content
            if not transcript_text or not transcript_text.strip():
                raise ValueError("No text content could be extracted from the file. Please check that the file contains text content.")
            
            # Truncate if too long (to avoid token limits)
            max_text_length = 100000  # approximately 25k tokens
            if len(transcript_text) > max_text_length:
                transcript_text = transcript_text[:max_text_length] + "\n\n[Content truncated due to length...]"
                logger.warning(f"Transcript truncated from {len(transcript_text)} to {max_text_length} characters")
            
            # Load the meeting minutes prompt template based on the template parameter
            template_key = f"meeting-minutes-{template}"
            prompt_configs = loadConfig('prompt.yml', namespace=False)
            
            # Fall back to original template if specific template not found
            if template_key not in prompt_configs:
                template_key = "meeting-minutes"
            
            prompt_template = prompt_configs[template_key]
            
            # Format the prompt with the extracted text
            full_prompt = prompt_template.format(transcript_content=transcript_text)
            
            # Generate meeting minutes
            meeting_summary = self.llm.get_prediction(prompt=full_prompt)
            
            if not meeting_summary or not meeting_summary.strip():
                raise ValueError("Failed to generate meeting summary - empty response from AI model")
            
            return meeting_summary
            
        except Exception as e:
            logger.error(f"Error generating meeting minutes: {str(e)}")
            raise
    
    def _extract_text_from_file(self, file_content: bytes, file_extension: str) -> str:
        """
        Extract text content from uploaded file.
        
        Args:
            file_content: The raw file content as bytes
            file_extension: The file extension
            
        Returns:
            str: The extracted text content
        """
        if file_extension == '.txt':
            # For text files, decode directly
            try:
                return file_content.decode('utf-8')
            except UnicodeDecodeError:
                try:
                    return file_content.decode('latin-1')
                except UnicodeDecodeError:
                    return file_content.decode('utf-8', errors='ignore')
                    
        elif file_extension == '.docx':
            # For DOCX files, process in memory
            try:
                import io
                # Try docx2txt first (simpler and more reliable)
                try:
                    import docx2txt
                    return docx2txt.process(io.BytesIO(file_content))
                except ImportError:
                    # Fallback to python-docx
                    try:
                        from docx import Document
                        doc = Document(io.BytesIO(file_content))
                        text_content = []
                        
                        # Extract text from paragraphs
                        for paragraph in doc.paragraphs:
                            if paragraph.text.strip():
                                text_content.append(paragraph.text)
                        
                        # Extract text from tables
                        for table in doc.tables:
                            for row in table.rows:
                                for cell in row.cells:
                                    if cell.text.strip():
                                        text_content.append(cell.text)
                        
                        return '\n'.join(text_content)
                    except ImportError:
                        raise ValueError("DOCX processing libraries not available. Please install 'docx2txt' or 'python-docx': pip install docx2txt python-docx")
            except Exception as docx_error:
                raise ValueError(f"Failed to process DOCX file: {str(docx_error)}")
        
        raise ValueError(f"Unsupported file extension: {file_extension}")

    def digitalize_document(self, file_content: bytes, filename: str, instruction: str = None) -> dict:
        """
        Digitalize a document (PDF, image, etc.) by extracting text content using OCR and AI.
        
        Args:
            file_content: The raw file content as bytes
            filename: The name of the uploaded file
            instruction: Optional instruction for what information to extract
            
        Returns:
            dict: Contains extracted_text and processing_info
        """
        try:
            # Validate file type (PDF, PNG, JPG, JPEG)
            allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg'}
            file_extension = os.path.splitext(filename.lower())[1] if filename else ''
            
            if file_extension not in allowed_extensions:
                raise ValueError(f"Unsupported file format '{file_extension}'. Supported formats: PDF, PNG, JPG, JPEG")
            
            # Validate file size (20MB max for images, 50MB for PDFs)
            file_size = len(file_content)
            if file_extension == '.pdf':
                max_file_size = 50 * 1024 * 1024  # 50MB for PDFs
            else:
                max_file_size = 20 * 1024 * 1024  # 20MB for images
                
            if file_size > max_file_size:
                raise ValueError(f"File too large. Maximum size is {max_file_size / (1024*1024):.0f}MB for {file_extension.upper()}, received {file_size / (1024*1024):.1f}MB")
            
            if file_size == 0:
                raise ValueError("Empty file provided. Please upload a file with content.")
            
            # Load the document digitalization prompt template
            prompt_template = loadConfig('prompt.yml', namespace=False)['document-digitalization']
            
            # Prepare instruction text
            if instruction and instruction.strip():
                instruction_text = f"SPECIFIC EXTRACTION INSTRUCTIONS: {instruction.strip()}"
            else:
                instruction_text = "GENERAL EXTRACTION: Extract all text content from the document comprehensively."
            
            # Format the prompt
            full_prompt = prompt_template.format(instruction_text=instruction_text)
            
            # Process the file using the LLM's multimodal capabilities
            extracted_text = self.llm.process_file_content(
                file_content=file_content,
                filename=filename,
                text_prompt=full_prompt
            )
            
            if not extracted_text or not extracted_text.strip():
                raise ValueError("No text could be extracted from the document. The document may be empty or contain only images without text.")
            
            # Prepare processing info
            processing_info = f"Successfully processed {file_extension.upper()} document ({file_size / (1024*1024):.1f}MB)"
            if instruction:
                processing_info += f" with custom extraction instructions"
            
            return {
                "extracted_text": extracted_text.strip(),
                "processing_info": processing_info
            }
            
        except ValueError as e:
            logger.error(f"Validation error in document digitalization: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in document digitalization: {str(e)}")
            raise ValueError(f"Failed to process document: {str(e)}")

    def analyze_documents(self, file_data_list: List[Dict[str, Any]], instruction: str) -> dict:
        """
        Analyze multiple documents (PDF, PNG, JPG, JPEG, DOCX) with comprehensive analysis including
        step breakdown, detailed analysis, and citations.
        
        Args:
            file_data_list: List of dictionaries containing:
                - 'content': Raw file content as bytes
                - 'filename': Name of the file
                - 'size': Size of the file in bytes
            instruction: Instruction for what analysis to perform
            
        Returns:
            dict: Contains analysis_result, processing_info, and documents_processed
        """
        try:
            # Validate that we have files to process
            if not file_data_list or len(file_data_list) == 0:
                raise ValueError("No files provided for analysis.")
            
            if len(file_data_list) > 5:
                raise ValueError(f"Too many files provided. Maximum 5 files allowed, received {len(file_data_list)}.")
            
            # Validate instruction
            if not instruction or not instruction.strip():
                raise ValueError("Analysis instruction is required.")
            
            processed_files = []
            total_size = 0
            
            # Validate each file
            for i, file_data in enumerate(file_data_list):
                filename = file_data.get('filename', f'document_{i+1}')
                file_content = file_data.get('content')
                file_size = file_data.get('size', len(file_content) if file_content else 0)
                
                # Validate file type (PDF, PNG, JPG, JPEG, DOCX)
                allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.docx'}
                file_extension = os.path.splitext(filename.lower())[1] if filename else ''
                
                if file_extension not in allowed_extensions:
                    raise ValueError(f"Unsupported file format '{file_extension}' in file '{filename}'. Supported formats: PDF, PNG, JPG, JPEG, DOCX")
                
                # Validate file size (individual limits)
                if file_extension == '.pdf':
                    max_file_size = 50 * 1024 * 1024  # 50MB for PDFs
                elif file_extension == '.docx':
                    max_file_size = 25 * 1024 * 1024  # 25MB for DOCX
                else:
                    max_file_size = 20 * 1024 * 1024  # 20MB for images
                
                if file_size > max_file_size:
                    raise ValueError(f"File '{filename}' is too large. Maximum size is {max_file_size / (1024*1024):.0f}MB for {file_extension.upper()}, received {file_size / (1024*1024):.1f}MB")
                
                if file_size == 0:
                    raise ValueError(f"Empty file provided: '{filename}'. Please upload files with content.")
                
                total_size += file_size
                processed_files.append(filename)
            
            # Validate total size (100MB max for all files combined)
            max_total_size = 100 * 1024 * 1024  # 100MB total
            if total_size > max_total_size:
                raise ValueError(f"Combined file size too large. Maximum total size is 100MB, received {total_size / (1024*1024):.1f}MB")
            
            # Load the document analyzer prompt template
            prompt_template = loadConfig('prompt.yml', namespace=False)['document-analyzer']
            
            # Prepare instruction text
            instruction_text = f"USER INSTRUCTION: {instruction.strip()}"
            
            # Format the prompt
            full_prompt = prompt_template.format(instruction_text=instruction_text)
            
            # Process the files using the LLM's multi-document capabilities
            analysis_result = self.llm.process_multiple_file_contents(
                file_data_list=file_data_list,
                text_prompt=full_prompt
            )
            
            if not analysis_result or not analysis_result.strip():
                raise ValueError("No analysis could be generated from the documents. The documents may be empty or contain unreadable content.")
            
            # Prepare processing info
            file_types = {}
            for file_data in file_data_list:
                filename = file_data.get('filename', '')
                ext = os.path.splitext(filename.lower())[1]
                file_types[ext] = file_types.get(ext, 0) + 1
            
            file_type_summary = ', '.join([f"{count} {ext.upper()}" for ext, count in file_types.items()])
            processing_info = f"Successfully analyzed {len(file_data_list)} documents ({file_type_summary}, {total_size / (1024*1024):.1f}MB total)"
            
            return {
                "analysis_result": analysis_result.strip(),
                "processing_info": processing_info,
                "documents_processed": processed_files
            }
            
        except ValueError as e:
            logger.error(f"Validation error in document analysis: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in document analysis: {str(e)}")
            raise ValueError(f"Failed to analyze documents: {str(e)}")