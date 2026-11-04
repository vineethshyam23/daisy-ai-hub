from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from starlette import status
from starlette.responses import JSONResponse
import logging
import os
from typing import Optional, List

from models import MeetingMinutesResponse, DocumentDigitalizationResponse, DocumentAnalyzerResponse, ErrorResponse
from services.productivity_service import ProductivityService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/productivity", tags=["Productivity Assistant"])


@router.post(
    "/meeting-minutes",
    status_code=status.HTTP_200_OK,
    response_model=MeetingMinutesResponse,
    summary="Generate Meeting Minutes",
    description="Upload a meeting transcript file (TXT or DOCX) and get a comprehensive meeting summary. Choose from three template types: 'discussion' for general meetings with key decisions and action items, 'daily-weekly' for status meetings with participant-specific tabular format, or 'presentation' for presentation summaries. The AI will analyze the transcript and create professional meeting minutes with structured sections. This endpoint processes files entirely in memory for better deployment compatibility.",
    responses={
        200: {
            "description": "Successfully generated meeting minutes",
            "content": {
                "application/json": {
                    "examples": {
                        "discussion_template": {
                            "summary": "Discussion Template Example",
                            "description": "Example output using the 'discussion' template for general meetings",
                            "value": {
                                "meeting_summary": """<h3>Meeting Context:</h3>
<ul>
<li><strong>Project/Topic:</strong> Q4 Product Launch Planning</li>
<li><strong>Meeting Date:</strong> October 26, 2023</li>
<li><strong>Attendees:</strong> Sarah (PM), Tom (Engineering), Maria (Marketing), David (Design)</li>
</ul>

<h3>1. Executive Summary:</h3>
<p>The team aligned on Q4 product launch timeline and resource allocation, with final go-live date set for December 15th.</p>

<h3>2. Key Decisions Made:</h3>
<ul>
<li>Launch date confirmed for December 15th, 2023</li>
<li>Marketing budget approved at $150k for Q4 campaign</li>
<li>Engineering team will deliver MVP by November 30th</li>
<li>Beta testing phase scheduled for first week of December</li>
</ul>

<h3>3. Action Items:</h3>
<ul>
<li>Finalize technical specifications: <strong>Owner(s):</strong> Tom, David - <strong>Deadline:</strong> November 1st</li>
<li>Prepare marketing campaign materials: <strong>Owner(s):</strong> Maria - <strong>Deadline:</strong> November 15th</li>
<li>Set up beta testing program: <strong>Owner(s):</strong> Sarah - <strong>Deadline:</strong> November 20th</li>
<li>Conduct final security review: <strong>Owner(s):</strong> Tom - <strong>Deadline:</strong> December 1st</li>
</ul>

<h3>4. Open Questions / For Next Meeting:</h3>
<ul>
<li>Pricing strategy for premium features needs final approval</li>
<li>Customer support staffing requirements for launch week</li>
<li>Integration testing timeline with third-party services</li>
</ul>"""
                            }
                        },
                        "daily_weekly_template": {
                            "summary": "Daily/Weekly Template Example",
                            "description": "Example output using the 'daily-weekly' template for status meetings",
                            "value": {
                                "meeting_summary": """<h3>Meeting Context:</h3>
<ul>
<li><strong>Meeting Type:</strong> Daily Standup</li>
<li><strong>Meeting Date:</strong> October 26, 2023</li>
<li><strong>Team/Department:</strong> Engineering Team</li>
</ul>

<h3>1. Meeting Overview:</h3>
<p>Daily standup focused on Q4 product launch progress and identifying blockers.</p>

<h3>2. Team Status Table:</h3>
<table border="1" style="border-collapse: collapse; width: 100%;">
<tr><th>Participant</th><th>What They've Done</th><th>What They're Working On</th><th>Blockers/Issues</th><th>Additional Notes</th></tr>
<tr><td>Sarah</td><td>Completed user story prioritization</td><td>Setting up beta testing program</td><td>Waiting for legal approval</td><td>Needs design mockups by Friday</td></tr>
<tr><td>Tom</td><td>Fixed authentication bugs</td><td>Database optimization</td><td>Performance testing environment down</td><td>Will pair with David on API</td></tr>
<tr><td>Maria</td><td>Finalized campaign copy</td><td>Creating social media assets</td><td>None</td><td>Campaign launch ready</td></tr>
</table>

<h3>3. Key Announcements:</h3>
<ul>
<li>Performance testing environment will be restored by noon</li>
<li>Design review meeting scheduled for Friday 2PM</li>
</ul>

<h3>4. Action Items:</h3>
<ul>
<li>Restore performance testing environment: <strong>Owner:</strong> DevOps - <strong>Deadline:</strong> Today noon</li>
<li>Legal approval for beta program: <strong>Owner:</strong> Sarah - <strong>Deadline:</strong> Tomorrow</li>
</ul>

<h3>5. Next Meeting:</h3>
<p>Tomorrow 9AM, same agenda format</p>"""
                            }
                        },
                        "presentation_template": {
                            "summary": "Presentation Template Example",
                            "description": "Example output using the 'presentation' template for presentation summaries",
                            "value": {
                                "meeting_summary": """<h3>Presentation Context:</h3>
<ul>
<li><strong>Presentation Title:</strong> Q4 Marketing Strategy Overview</li>
<li><strong>Presenter:</strong> Maria Johnson, Marketing Director</li>
<li><strong>Date:</strong> October 26, 2023</li>
<li><strong>Audience:</strong> Executive Team, Department Heads</li>
</ul>

<h3>1. Executive Summary:</h3>
<p>Maria presented the comprehensive Q4 marketing strategy focused on digital transformation and customer retention, with projected 30% increase in lead generation through multi-channel campaigns.</p>

<h3>2. Key Topics Covered:</h3>
<ul>
<li>Digital marketing transformation initiatives</li>
<li>Customer retention strategies</li>
<li>Social media campaign optimization</li>
<li>Budget allocation across channels</li>
<li>Performance metrics and KPIs</li>
</ul>

<h3>3. Key Insights & Findings:</h3>
<ul>
<li>Customer acquisition cost decreased by 25% through targeted campaigns</li>
<li>Email marketing shows highest ROI at 4:1 ratio</li>
<li>Social media engagement increased 45% year-over-year</li>
<li>Video content generates 3x more leads than static content</li>
</ul>

<h3>4. Recommendations:</h3>
<ul>
<li>Increase video content production by 50%</li>
<li>Implement AI-powered personalization for email campaigns</li>
<li>Expand social media presence to LinkedIn and TikTok</li>
<li>Allocate 40% of budget to digital channels</li>
</ul>

<h3>5. Supporting Data:</h3>
<ul>
<li>Lead generation target: 10,000 qualified leads in Q4</li>
<li>Customer retention rate: 85% (target: 90%)</li>
<li>Marketing qualified leads conversion: 15%</li>
<li>Budget: $500K allocated for Q4 campaigns</li>
</ul>

<h3>6. Q&A Highlights:</h3>
<ul>
<li>Q: Timeline for AI implementation? A: Q1 2024 pilot program</li>
<li>Q: ROI projections for video content? A: 200% increase in engagement expected</li>
<li>Q: Staff resources needed? A: 2 additional content creators</li>
</ul>

<h3>7. Next Steps:</h3>
<ul>
<li>Finalize budget approval by October 30th</li>
<li>Begin video content production planning</li>
<li>Schedule AI platform vendor meetings</li>
<li>Prepare detailed implementation timeline</li>
</ul>"""
                            }
                        }
                    }
                }
            }
        },
        400: {
            "description": "Invalid file format or file processing error",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def generate_meeting_minutes(
    transcript_file: UploadFile = File(..., description="Meeting transcript file (TXT or DOCX format)"),
    template: Optional[str] = Form("discussion", description="Template type for meeting summary generation (discussion, daily-weekly, presentation)")
):
    """
    Generate meeting minutes from uploaded transcript files.
    Processes files entirely in memory for better deployment compatibility.
    Supports TXT and DOCX formats with comprehensive error handling.
    """
    try:
        # Validate template parameter
        valid_templates = ["discussion", "daily-weekly", "presentation"]
        if template not in valid_templates:
            raise ValueError(f"Invalid template '{template}'. Valid templates are: {', '.join(valid_templates)}")
        
        # Read file content
        file_content = await transcript_file.read()
        
        # Use the productivity service to generate meeting minutes
        productivity_service = ProductivityService()
        meeting_summary = productivity_service.generate_meeting_minutes(
            file_content=file_content,
            filename=transcript_file.filename,
            template=template
        )
        
        # Return the meeting minutes
        return JSONResponse(content={
            "meeting_summary": meeting_summary
        })
        
    except ValueError as e:
        logger.error(f"Validation error in meeting minutes generation: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in meeting minutes generation: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error processing meeting transcript: {str(e)}"}
        )


@router.post(
    "/document-digitalisation",
    status_code=status.HTTP_200_OK,
    response_model=DocumentDigitalizationResponse,
    summary="Document Digitalization",
    description="Upload a document (PDF, PNG, JPG) and extract text content using OCR and AI. Optionally provide specific instructions for what information to extract or the target structure required. Uses Gemini's multimodal capabilities for accurate text extraction from images and PDFs.",
    responses={
        200: {
            "description": "Successfully extracted text from document",
            "content": {
                "application/json": {
                    "example": {
                        "extracted_text": "Customer: John Smith\nAddress: 123 Main St, City, State 12345\nInvoice Number: INV-2023-001\nDate: January 15, 2023\nTotal Amount: $125.50\n\nItems:\n- Product A: $50.00\n- Product B: $75.50",
                        "processing_info": "Successfully processed PDF document (2.3MB) with custom extraction instructions"
                    }
                }
            }
        },
        400: {
            "description": "Invalid file format or file processing error",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def document_digitalisation(
    document_file: UploadFile = File(..., description="Document file (PDF, PNG, JPG, JPEG format)"),
    instruction: Optional[str] = Form(None, description="Optional instruction for what information to extract or target structure required")
):
    """
    Digitalize a document by extracting text content using OCR and AI.
    Supports PDF, PNG, JPG, and JPEG formats with comprehensive error handling.
    """
    try:
        # Validate file type
        allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg'}
        file_extension = os.path.splitext(document_file.filename.lower())[1] if document_file.filename else ''
        
        if file_extension not in allowed_extensions:
            raise ValueError(f"Unsupported file format '{file_extension}'. Supported formats: PDF, PNG, JPG, JPEG")
        
        # Read file content
        file_content = await document_file.read()
        
        # Use the productivity service to digitalize the document
        productivity_service = ProductivityService()
        result = productivity_service.digitalize_document(
            file_content=file_content,
            filename=document_file.filename,
            instruction=instruction
        )
        
        # Return the digitalized text
        return JSONResponse(content=result)
        
    except ValueError as e:
        logger.error(f"Validation error in document digitalization: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in document digitalization: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error processing document: {str(e)}"}
        )


@router.post(
    "/document-analyzer",
    status_code=status.HTTP_200_OK,
    response_model=DocumentAnalyzerResponse,
    summary="Document Analyzer",
    description="Upload up to 5 documents (PDF, PNG, JPG, JPEG, DOCX) and get comprehensive analysis based on your specific instructions. The AI will break down your instruction into steps, provide detailed analysis, and include citations from the documents. Perfect for analyzing reports, contracts, research papers, and other business documents.",
    responses={
        200: {
            "description": "Successfully analyzed documents",
            "content": {
                "application/json": {
                    "example": {
                        "analysis_result": """**STEP 1: INSTRUCTION BREAKDOWN**
1. Extract key financial metrics from quarterly reports
2. Compare performance across different quarters
3. Identify trends and potential risks

**STEP 2: DOCUMENT ANALYSIS & RESPONSE**
Based on the analysis of the provided quarterly reports, the company shows strong revenue growth of 15% year-over-year, with Q3 2023 revenue reaching $2.3M compared to $2.0M in Q2. The gross margin improved from 65% to 68%, indicating better cost management...

**STEP 3: CITATIONS & SOURCES**
- Document references: Q3_Report.pdf, page 3, Revenue Section; Q2_Report.pdf, page 2, Financial Summary
- Key evidence: "Total revenue increased to $2.3M" (Q3_Report.pdf, p.3), "Gross margin: 68%" (Q3_Report.pdf, p.5)
- Source reliability: Official quarterly reports with audited financial data""",
                        "processing_info": "Successfully analyzed 2 documents (2 PDF, 5.2MB total)",
                        "documents_processed": ["Q3_Report.pdf", "Q2_Report.pdf"]
                    }
                }
            }
        },
        400: {
            "description": "Invalid file format, file processing error, or missing instruction",
            "model": ErrorResponse
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def analyze_documents(
    document_files: List[UploadFile] = File(..., description="Document files to analyze (1-5 files: PDF, PNG, JPG, JPEG, DOCX formats)"),
    instruction: str = Form(..., description="Specific instruction for document analysis (e.g., 'Compare financial performance across quarters', 'Extract key contract terms and risks')")
):
    """
    Analyze multiple documents with comprehensive analysis including step breakdown, 
    detailed analysis, and citations. Supports up to 5 files simultaneously.
    """
    try:
        # Validate number of files
        if len(document_files) == 0:
            raise ValueError("At least one document file is required.")
        
        if len(document_files) > 5:
            raise ValueError(f"Too many files provided. Maximum 5 files allowed, received {len(document_files)}.")
        
        # Validate instruction
        if not instruction or not instruction.strip():
            raise ValueError("Analysis instruction is required.")
        
        # Prepare file data
        file_data_list = []
        for file in document_files:
            # Validate file type
            allowed_extensions = {'.pdf', '.png', '.jpg', '.jpeg', '.docx'}
            file_extension = os.path.splitext(file.filename.lower())[1] if file.filename else ''
            
            if file_extension not in allowed_extensions:
                raise ValueError(f"Unsupported file format '{file_extension}' in file '{file.filename}'. Supported formats: PDF, PNG, JPG, JPEG, DOCX")
            
            # Read file content
            file_content = await file.read()
            
            file_data_list.append({
                'content': file_content,
                'filename': file.filename,
                'size': len(file_content)
            })
        
        # Use the productivity service to analyze the documents
        productivity_service = ProductivityService()
        result = productivity_service.analyze_documents(
            file_data_list=file_data_list,
            instruction=instruction
        )
        
        # Return the analysis result
        return JSONResponse(content=result)
        
    except ValueError as e:
        logger.error(f"Validation error in document analysis: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in document analysis: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error analyzing documents: {str(e)}"}
        )