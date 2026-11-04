from vertexai.generative_models import SafetySetting, GenerativeModel, GenerationConfig, Part
from .helper import loadConfig
import base64
import vertexai
from vertexai.preview.generative_models import Tool
from vertexai.preview.generative_models import grounding
import os
import mimetypes
from typing import List, Union, Dict, Any
import logging

# Use centralized logging configuration
try:
    from config import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback to basic logging if config module is not available
    logger = logging.getLogger(__name__)

# Document processing imports
try:
    import docx2txt  # For DOCX files
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False

try:
    from docx import Document  # Alternative for DOCX files
    PYTHON_DOCX_AVAILABLE = True
except ImportError:
    PYTHON_DOCX_AVAILABLE = False


class LLM(object):
    def __init__(
            self,
            model_name=None,
            model_location=None,
            max_output_tokens=None,
            temperature=None,
            top_k=None,
            top_p=None
    ):
        # Load configuration from gcp.yml
        self.config = loadConfig('gcp.yml', namespace=False)
        
        # Use provided model_name or default from config
        self.model_name = model_name or self.config.get('llm_model_name')
        self.model_location = model_location or self.config.get('llm_model_location', 'us-central1')
        
        vertexai.init(
            project=os.environ.get("GCP_PROJECT"),
            location=self.model_location,
            api_endpoint=f"{self.model_location}-aiplatform.googleapis.com"
        )

        self.generative_model = GenerativeModel(self.model_name)
        self.safety_settings = [
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HATE_SPEECH,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
            SafetySetting(
                category=SafetySetting.HarmCategory.HARM_CATEGORY_HARASSMENT,
                threshold=SafetySetting.HarmBlockThreshold.OFF
            ),
        ]
        
        # Use provided parameters or defaults
        self.generation_config = GenerationConfig(
            max_output_tokens=max_output_tokens or 8192,
            temperature=temperature or 1.0,  # 1-2
            top_k=top_k or 1,  # 1-40
            top_p=top_p or 0.95  # 0-1
        )

    def _extract_text_from_response(self, prediction):
        """
        Extract text from a prediction response, handling both single and multiple content parts.
        
        Args:
            prediction: The response from the generative model
            
        Returns:
            str: The extracted text content
        """
        try:
            # Try to get text directly first (for simple responses)
            if hasattr(prediction, 'text') and prediction.text:
                return prediction.text.strip()
        except Exception:
            # If direct text access fails, try to extract from candidates
            pass
        
        try:
            # Handle multiple content parts
            if hasattr(prediction, 'candidates') and prediction.candidates:
                candidate = prediction.candidates[0]
                if hasattr(candidate, 'content') and candidate.content:
                    if hasattr(candidate.content, 'parts') and candidate.content.parts:
                        # Extract text from all parts
                        text_parts = []
                        for part in candidate.content.parts:
                            if hasattr(part, 'text') and part.text:
                                text_parts.append(part.text)
                        return ''.join(text_parts).strip()
        except Exception as e:
            logging.error(f"Error extracting text from response parts: {str(e)}")
        
        # Fallback: return empty string if all extraction methods fail
        logging.warning("Could not extract text from prediction response")
        return ""

    def get_prediction(self, prompt):
        prediction = self.generative_model.generate_content(prompt, generation_config=self.generation_config,
                                                            safety_settings=self.safety_settings,stream=False)
        return self._extract_text_from_response(prediction)

    def get_prediction_with_custom_config(self, prompt, max_output_tokens=None, temperature=None, top_k=None, top_p=None):
        """
        Get prediction with custom generation configuration parameters.
        
        Args:
            prompt: The prompt to send to the LLM
            max_output_tokens: Maximum number of output tokens (optional)
            temperature: Temperature for text generation (optional)
            top_k: Top-k sampling parameter (optional)
            top_p: Top-p sampling parameter (optional)
            
        Returns:
            The generated text response
        """
        # Create a new generation config with custom parameters
        custom_config = GenerationConfig(
            max_output_tokens=max_output_tokens or self.generation_config.max_output_tokens,
            temperature=temperature or self.generation_config.temperature,
            top_k=top_k or self.generation_config.top_k,
            top_p=top_p or self.generation_config.top_p
        )
        
        prediction = self.generative_model.generate_content(
            prompt, 
            generation_config=custom_config,
            safety_settings=self.safety_settings,
            stream=False
        )
        return self._extract_text_from_response(prediction)

    def get_multi_turn_chat_prediction(self, messages: List[Dict[str, Any]]):
        """
        Get prediction for multi-turn chat conversation with message history support.
        
        Args:
            messages: List of message dictionaries with 'role', 'message', and optional 'multimedia'
                     Role should be either 'user' or 'model'
                     Message is the text content
                     Multimedia is optional list of base64-encoded images
        
        Returns:
            The generated text response from the conversation
        """
        try:
            # Start a chat session
            chat = self.generative_model.start_chat()
            
            # Process messages in order to build conversation history
            last_response = None
            
            for i, msg in enumerate(messages):
                role = msg.get('role', 'user')
                message_text = msg.get('message', '')
                multimedia = msg.get('multimedia', [])
                
                # Only process user messages - model messages are responses we need to simulate
                if role == 'user':
                    # Create parts list starting with the text message
                    parts = []
                    if message_text:
                        parts.append(message_text)
                    
                    # Process multimedia content (base64 images)
                    if multimedia and isinstance(multimedia, list):
                        for media_item in multimedia:
                            if media_item and isinstance(media_item, str):
                                # Handle base64 data URLs (e.g., "data:image/jpeg;base64,/9j/...")
                                if media_item.startswith('data:'):
                                    try:
                                        # Extract mime type and base64 data
                                        header, base64_data = media_item.split(',', 1)
                                        mime_type = header.split(':')[1].split(';')[0]
                                        
                                        # Decode base64 data
                                        image_data = base64.b64decode(base64_data)
                                        
                                        # Create image part
                                        image_part = Part.from_data(
                                            data=image_data,
                                            mime_type=mime_type
                                        )
                                        parts.append(image_part)
                                    except Exception as e:
                                        logging.error(f"Error processing multimedia item: {str(e)}")
                                        continue
                                else:
                                    # Handle raw base64 (assume JPEG)
                                    try:
                                        image_data = base64.b64decode(media_item)
                                        image_part = Part.from_data(
                                            data=image_data,
                                            mime_type="image/jpeg"
                                        )
                                        parts.append(image_part)
                                    except Exception as e:
                                        logging.error(f"Error processing raw base64 multimedia: {str(e)}")
                                        continue
                    
                    # Send user message and get response
                    if parts:
                        response = chat.send_message(
                            parts,
                            generation_config=self.generation_config,
                            safety_settings=self.safety_settings
                        )
                        last_response = self._extract_text_from_response(response)
                        
                        # Check if the next message is a model response that should match our expectation
                        if i + 1 < len(messages) and messages[i + 1].get('role') == 'model':
                            # Skip the next message since we already have the model response
                            continue
                    
                elif role == 'model' and i == 0:
                    # If conversation starts with model message, we can't simulate that easily
                    # Just continue to the next user message
                    continue
            
            if last_response is None:
                # If no user messages were processed, send the last user message
                user_messages = [msg for msg in messages if msg.get('role') == 'user']
                if user_messages:
                    last_msg = user_messages[-1]
                    message_text = last_msg.get('message', '')
                    if message_text:
                        response = chat.send_message(
                            [message_text],
                            generation_config=self.generation_config,
                            safety_settings=self.safety_settings
                        )
                        last_response = self._extract_text_from_response(response)
                else:
                    return "No valid user messages found in conversation."
            
            return last_response or "No response generated."
            
        except Exception as e:
            logging.error(f"Error in multi-turn chat prediction: {str(e)}")
            return f"Error generating multi-turn chat response: {str(e)}"

    def get_prediction_google_grounded(self, prompt, include_citations=False):
        tools = [
            Tool.from_google_search_retrieval(
                google_search_retrieval=grounding.GoogleSearchRetrieval()
            ),
        ]
        model = GenerativeModel(
            "gemini-1.5-flash-002",
            tools=tools,
        )
        chat = model.start_chat()
        response = chat.send_message(
            [prompt],
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )
        
        # Extract the text response
        text_response = self._extract_text_from_response(response)
        
        # If citations are not requested, return just the text for backward compatibility
        if not include_citations:
            return text_response
        
        # Extract grounding metadata with citations
        citations = {
            'search_queries': [],
            'sources': [],
            'num_sources': 0
        }
        
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                grounding_metadata = candidate.grounding_metadata
                
                # Extract search queries used
                if hasattr(grounding_metadata, 'web_search_queries'):
                    citations['search_queries'].append(str(grounding_metadata.web_search_queries))
                
                # Extract grounding chunks (sources)
                if hasattr(grounding_metadata, 'grounding_chunks'):
                    for chunk in grounding_metadata.grounding_chunks:
                        if hasattr(chunk, 'web') and chunk.web:
                            source_info = {
                                'title': str(chunk.web.title) if hasattr(chunk.web, 'title') else 'Unknown',
                                'uri': str(chunk.web.uri) if hasattr(chunk.web, 'uri') else 'Unknown'
                            }
                            citations['sources'].append(source_info)
                
                citations['num_sources'] = len(citations['sources'])
        
        return {
            'text': text_response,
            'citations': citations
        }

    def add_documents_to_prompt(self, documents: List[Union[str, Dict[str, Any]]], text_prompt: str) -> List[Any]:
        """
        Add multiple documents as context to a prompt for Vertex AI Generative Models.
        
        Supported document types:
        - PDF files (application/pdf) - up to 50MB
        - TXT files (text/plain) - up to 10MB  
        - DOCX files (application/vnd.openxmlformats-officedocument.wordprocessingml.document) - converted to text
        - PNG images (image/png) - up to 20MB
        - JPG/JPEG images (image/jpeg) - up to 20MB
        
        Args:
            documents: List of document paths (strings) or document dictionaries with 'path' and optional 'type'
            text_prompt: The text prompt to include with the documents
            
        Returns:
            List of Parts ready for GenerativeModel.generate_content()
            
        Example:
            documents = [
                "path/to/document.pdf",
                {"path": "path/to/document.docx", "type": "docx"},
                "path/to/document.txt",
                "path/to/image.png"
            ]
            parts = llm.add_documents_to_prompt(documents, "Analyze these documents")
            response = llm.generative_model.generate_content(parts)
        """
        parts = []
        
        for doc in documents:
            try:
                # Handle both string paths and dictionary format
                if isinstance(doc, str):
                    doc_path = doc
                    doc_type = None
                elif isinstance(doc, dict):
                    doc_path = doc.get('path')
                    doc_type = doc.get('type')
                else:
                    logging.warning(f"Invalid document format: {doc}. Skipping.")
                    continue
                
                if not os.path.exists(doc_path):
                    logging.warning(f"Document not found: {doc_path}. Skipping.")
                    continue
                
                # Auto-detect MIME type if not specified
                if not doc_type:
                    mime_type, _ = mimetypes.guess_type(doc_path)
                else:
                    mime_type = self._get_mime_type_from_extension(doc_type)
                
                # Get file size for validation
                file_size = os.path.getsize(doc_path)
                
                # Process document based on type
                if mime_type == "application/pdf":
                    part = self._process_pdf_document(doc_path, file_size)
                elif mime_type == "text/plain":
                    part = self._process_txt_document(doc_path, file_size)
                elif mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document" or doc_type == "docx":
                    part = self._process_docx_document(doc_path, file_size)
                elif mime_type in ["image/png", "image/jpeg"]:
                    part = self._process_image_document(doc_path, file_size, mime_type)
                else:
                    logging.warning(f"Unsupported document type {mime_type} for file: {doc_path}. Skipping.")
                    continue
                
                if part:
                    parts.append(part)
                    
            except Exception as e:
                logging.error(f"Error processing document {doc}: {str(e)}. Skipping.")
                continue
        
        # Add the text prompt
        parts.append(text_prompt)
        
        return parts
    
    def _get_mime_type_from_extension(self, extension: str) -> str:
        """Get MIME type from file extension."""
        extension_map = {
            'pdf': 'application/pdf',
            'txt': 'text/plain',
            'docx': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'png': 'image/png',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg'
        }
        return extension_map.get(extension.lower(), 'application/octet-stream')
    
    def _process_pdf_document(self, doc_path: str, file_size: int) -> Part:
        """
        Process PDF document for Vertex AI.
        
        Args:
            doc_path: Path to the PDF file
            file_size: File size in bytes
            
        Returns:
            Part object for Vertex AI or None if processing fails
        """
        # Check size limits (50MB for PDF)
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            logging.warning(f"PDF file {doc_path} is too large ({file_size / (1024*1024):.1f}MB). Max size is 50MB.")
            return None
        
        try:
            with open(doc_path, 'rb') as file:
                file_data = file.read()
                # For PDF, we can use Part.from_data with base64 encoding
                encoded_data = base64.b64encode(file_data).decode('utf-8')
                return Part.from_data(
                    data=base64.b64decode(encoded_data),
                    mime_type="application/pdf"
                )
        except Exception as e:
            logging.error(f"Error processing PDF {doc_path}: {str(e)}")
            return None
    
    def _process_txt_document(self, doc_path: str, file_size: int) -> Part:
        """
        Process TXT document for Vertex AI.
        
        Args:
            doc_path: Path to the TXT file
            file_size: File size in bytes
            
        Returns:
            Part object for Vertex AI or None if processing fails
        """
        # Check size limits (10MB for TXT)
        max_size = 10 * 1024 * 1024  # 10MB
        if file_size > max_size:
            logging.warning(f"TXT file {doc_path} is too large ({file_size / (1024*1024):.1f}MB). Max size is 10MB.")
            return None
        
        try:
            with open(doc_path, 'r', encoding='utf-8', errors='ignore') as file:
                text_content = file.read()
                return Part.from_data(
                    data=text_content.encode('utf-8'),
                    mime_type="text/plain"
                )
        except Exception as e:
            logging.error(f"Error processing TXT {doc_path}: {str(e)}")
            return None
    
    def _process_docx_document(self, doc_path: str, file_size: int) -> Part:
        """
        Process DOCX document by converting to text for Vertex AI.
        
        Args:
            doc_path: Path to the DOCX file
            file_size: File size in bytes
            
        Returns:
            Part object for Vertex AI or None if processing fails
        """
        # Check size limits (50MB for DOCX, but we'll convert to text)
        max_size = 50 * 1024 * 1024  # 50MB
        if file_size > max_size:
            logging.warning(f"DOCX file {doc_path} is too large ({file_size / (1024*1024):.1f}MB). Max size is 50MB.")
            return None
        
        try:
            # Try docx2txt first (simpler and more reliable)
            if DOCX_AVAILABLE:
                text_content = docx2txt.process(doc_path)
            elif PYTHON_DOCX_AVAILABLE:
                # Fallback to python-docx
                doc = Document(doc_path)
                text_content = []
                
                # Extract text from paragraphs
                for paragraph in doc.paragraphs:
                    text_content.append(paragraph.text)
                
                # Extract text from tables
                for table in doc.tables:
                    for row in table.rows:
                        for cell in row.cells:
                            text_content.append(cell.text)
                
                text_content = '\n'.join(text_content)
            else:
                logging.error("No DOCX processing library available. Install docx2txt or python-docx.")
                return None
            
            if not text_content or not text_content.strip():
                logging.warning(f"No text content extracted from DOCX file: {doc_path}")
                return None
            
            # Return as text/plain since we converted DOCX to text
            return Part.from_data(
                data=text_content.encode('utf-8'),
                mime_type="text/plain"
            )
            
        except Exception as e:
            logging.error(f"Error processing DOCX {doc_path}: {str(e)}")
            return None
    
    def _process_image_document(self, doc_path: str, file_size: int, mime_type: str) -> Part:
        """
        Process image document for Vertex AI.
        
        Args:
            doc_path: Path to the image file
            file_size: File size in bytes
            mime_type: MIME type of the image
            
        Returns:
            Part object for Vertex AI or None if processing fails
        """
        # Check size limits (20MB for images)
        max_size = 20 * 1024 * 1024  # 20MB
        if file_size > max_size:
            logging.warning(f"Image file {doc_path} is too large ({file_size / (1024*1024):.1f}MB). Max size is 20MB.")
            return None
        
        try:
            with open(doc_path, 'rb') as file:
                image_data = file.read()
                return Part.from_data(
                    data=image_data,
                    mime_type=mime_type
                )
        except Exception as e:
            logging.error(f"Error processing image {doc_path}: {str(e)}")
            return None
    
    def process_file_content(self, file_content: bytes, filename: str, text_prompt: str) -> Union[str, Dict[str, Any]]:
        """
        Process file content directly from bytes (useful for file uploads).
        
        Args:
            file_content: Raw file content as bytes
            filename: Name of the file (used to determine MIME type)
            text_prompt: The text prompt to include with the document
            
        Returns:
            Generated text response from the document analysis
        """
        import tempfile
        import os
        
        # Get file extension and MIME type
        _, file_extension = os.path.splitext(filename.lower())
        mime_type = self._get_mime_type_from_extension(file_extension[1:])  # Remove the dot
        
        # Create temporary file to process
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
            temp_file.write(file_content)
            temp_file_path = temp_file.name
        
        try:
            # Process the temporary file
            parts = self.add_documents_to_prompt([temp_file_path], text_prompt)
            
            if not parts:
                return "No valid content could be extracted from the file."
            
            # Generate response
            response = self.generative_model.generate_content(
                parts,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            return self._extract_text_from_response(response)
            
        except Exception as e:
            logging.error(f"Error processing file content: {str(e)}")
            return f"Error processing file: {str(e)}"
        finally:
            # Clean up temporary file
            try:
                os.unlink(temp_file_path)
            except:
                pass
    
    def generate_content_with_documents(self, documents: List[Union[str, Dict[str, Any]]], 
                                      text_prompt: str, include_citations: bool = False) -> Union[str, Dict[str, Any]]:
        """
        Generate content using documents as context with optional grounding.
        
        Args:
            documents: List of document paths or document dictionaries
            text_prompt: The text prompt to include with the documents
            include_citations: Whether to include grounding citations in the response
            
        Returns:
            Generated text response or dictionary with text and citations
        """
        parts = self.add_documents_to_prompt(documents, text_prompt)
        
        if not parts:
            return "No valid documents provided for processing."
        
        try:
            if include_citations:
                # Use grounded model for citations
                tools = [
                    Tool.from_google_search_retrieval(
                        google_search_retrieval=grounding.GoogleSearchRetrieval()
                    ),
                ]
                model = GenerativeModel(
                    "gemini-1.5-flash-002",
                    tools=tools,
                )
                chat = model.start_chat()
                response = chat.send_message(
                    parts,
                    generation_config=self.generation_config,
                    safety_settings=self.safety_settings
                )
                
                # Extract grounding metadata
                text_response = self._extract_text_from_response(response)
                citations = self._extract_citations(response)
                
                return {
                    'text': text_response,
                    'citations': citations
                }
            else:
                # Use regular model without grounding
                response = self.generative_model.generate_content(
                    parts,
                    generation_config=self.generation_config,
                    safety_settings=self.safety_settings
                )
                return self._extract_text_from_response(response)
                
        except Exception as e:
            logging.error(f"Error generating content with documents: {str(e)}")
            return f"Error generating content: {str(e)}"
    
    def _extract_citations(self, response) -> Dict[str, Any]:
        """Extract citations from grounded response."""
        citations = {
            'search_queries': [],
            'sources': [],
            'num_sources': 0
        }
        
        if response.candidates and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if hasattr(candidate, 'grounding_metadata') and candidate.grounding_metadata:
                grounding_metadata = candidate.grounding_metadata
                
                # Extract search queries used
                if hasattr(grounding_metadata, 'web_search_queries'):
                    citations['search_queries'].append(str(grounding_metadata.web_search_queries))
                
                # Extract grounding chunks (sources)
                if hasattr(grounding_metadata, 'grounding_chunks'):
                    for chunk in grounding_metadata.grounding_chunks:
                        if hasattr(chunk, 'web') and chunk.web:
                            source_info = {
                                'title': str(chunk.web.title) if hasattr(chunk.web, 'title') else 'Unknown',
                                'uri': str(chunk.web.uri) if hasattr(chunk.web, 'uri') else 'Unknown'
                            }
                            citations['sources'].append(source_info)
                
                citations['num_sources'] = len(citations['sources'])
        
        return citations

    def process_multiple_file_contents(self, file_data_list: List[Dict[str, Any]], text_prompt: str) -> Union[str, Dict[str, Any]]:
        """
        Process multiple file contents directly from bytes (useful for multiple file uploads).
        
        Args:
            file_data_list: List of dictionaries containing:
                - 'content': Raw file content as bytes
                - 'filename': Name of the file (used to determine MIME type)
            text_prompt: The text prompt to include with the documents
            
        Returns:
            Generated text response from the multi-document analysis
        """
        import tempfile
        import os
        
        temp_file_paths = []
        
        try:
            # Create temporary files for all uploaded documents
            for file_data in file_data_list:
                file_content = file_data['content']
                filename = file_data['filename']
                
                # Get file extension
                _, file_extension = os.path.splitext(filename.lower())
                
                # Create temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=file_extension) as temp_file:
                    temp_file.write(file_content)
                    temp_file_paths.append(temp_file.name)
            
            # Process all files together using existing method
            parts = self.add_documents_to_prompt(temp_file_paths, text_prompt)
            
            if not parts:
                return "No valid content could be extracted from the files."
            
            # Generate response
            response = self.generative_model.generate_content(
                parts,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )
            
            return self._extract_text_from_response(response)
            
        except Exception as e:
            logging.error(f"Error processing multiple file contents: {str(e)}")
            return f"Error processing files: {str(e)}"
        finally:
            # Clean up all temporary files
            for temp_file_path in temp_file_paths:
                try:
                    os.unlink(temp_file_path)
                except:
                    pass 