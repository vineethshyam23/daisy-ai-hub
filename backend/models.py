from pydantic import BaseModel, Field
from typing import List, Optional


class EmailReplyRequest(BaseModel):
    subject: str = Field(
        ...,
        description="The subject line of the original email",
        example="Re: Project Proposal Discussion"
    )
    from_sender: str = Field(
        ...,
        description="The sender of the original email",
        example="john.smith@company.com"
    )
    email_content: str = Field(
        ...,
        description="The full content of the original email to reply to",
        example="Hello, I received your proposal and would like to discuss the pricing. Could we schedule a meeting next week to go over the details?"
    )
    tone: str = Field(
        ...,
        description="The desired tone for the reply",
        example="Professional"
    )
    reply_type: str = Field(
        ...,
        description="The type of reply to generate",
        example="Response"
    )
    length: str = Field(
        ...,
        description="The desired length of the reply",
        example="Medium"
    )
    priority: str = Field(
        ...,
        description="The priority level of the response",
        example="Normal"
    )
    additional_instructions: Optional[str] = Field(
        None,
        description="Additional specific instructions for the reply",
        example="Please mention our upcoming product launch and include pricing information"
    )


class Query(BaseModel):
    email: str = Field(
        ...,
        description="The email content to process",
        example="Hello, I received your proposal and would like to discuss the pricing. Could we schedule a meeting next week?"
    )


class SocialMediaPostRequest(BaseModel):
    topic: str = Field(
        ...,
        description="The main topic of the social media post",
        example="New product launch"
    )
    key_message: str = Field(
        ...,
        description="The detailed key message or content for the post",
        example="We're excited to announce our new eco-friendly water bottles that help reduce plastic waste while keeping you hydrated throughout the day."
    )
    target_audience: str = Field(
        ...,
        description="The target audience for this post",
        example="Environmentally conscious consumers aged 25-45"
    )
    call_to_action: Optional[str] = Field(
        None,
        description="Optional call to action for the post",
        example="Visit our website to learn more"
    )
    platform: str = Field(
        ...,
        description="The social media platform for the post",
        example="LinkedIn"
    )
    tone: str = Field(
        ...,
        description="The desired tone for the post",
        example="Professional"
    )
    content_style: str = Field(
        ...,
        description="The style of content to create",
        example="Storytelling"
    )
    include_hashtags: bool = Field(
        ...,
        description="Whether to include hashtags in the post",
        example=True
    )
    include_emojis: bool = Field(
        ...,
        description="Whether to include emojis in the post",
        example=True
    )
    generate_image: bool = Field(
        ...,
        description="Whether to generate an accompanying image for the post",
        example=True
    )


class ImageGenerationRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="The text prompt describing the image to generate",
        example="A beautiful sunset over a mountain landscape with vibrant colors"
    )
    number_of_images: Optional[int] = Field(
        1,
        description="Number of images to generate",
        example=2,
        ge=1,
        le=10
    )
    aspect_ratio: Optional[str] = Field(
        "1:1",
        description="Aspect ratio for the generated images",
        example="16:9"
    )
    negative_prompt: Optional[str] = Field(
        "",
        description="What to avoid in the generated image",
        example="blurry, low quality, distorted"
    )
    person_generation: Optional[str] = Field(
        None,
        description="Settings for person generation in images",
        example="allow"
    )
    safety_filter_level: Optional[str] = Field(
        None,
        description="Safety filter level for content moderation",
        example="medium"
    )
    add_watermark: Optional[bool] = Field(
        None,
        description="Whether to add a watermark to generated images",
        example=False
    )


class ImageResponse(BaseModel):
    images: List[str] = Field(
        ...,
        description="List of base64-encoded images as data URLs",
        example=["data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="]
    )


class InterviewQuestionRequest(BaseModel):
    job_id: str = Field(
        ...,
        description="The job ID from your configured career portal",
        example="1549397"
    )


class LearningPathRequest(BaseModel):
    skill: str = Field(
        ...,
        description="The topic, skill, or job title to create a learning path for",
        example="Data Science"
    )
    skill_level: str = Field(
        ...,
        description="Current skill level (e.g., Beginner, Intermediate, Advanced)",
        example="Beginner"
    )
    target_time: str = Field(
        ...,
        description="Target timeline for completing the learning path",
        example="6 months"
    )
    study_commitment: str = Field(
        ...,
        description="How much time can be committed to studying per week",
        example="10 hours per week"
    )


class LearningPathResponse(BaseModel):
    content: str = Field(
        ...,
        description="The generated learning path content",
        example="# Data Science Learning Path\n\n## Personalized Overview\nThis 6-month learning path is designed for beginners..."
    )
    citations: dict = Field(
        ...,
        description="Grounding citations and sources used",
        example={
            "search_queries": ["data science learning resources"],
            "sources": [
                {"title": "coursera.org", "uri": "https://..."},
                {"title": "kaggle.com", "uri": "https://..."}
            ],
            "num_sources": 5
        }
    )


class MeetingMinutesRequest(BaseModel):
    template: Optional[str] = Field(
        "discussion",
        description="The template type for meeting summary generation",
        enum=["discussion", "daily-weekly", "presentation"],
        example="discussion"
    )


class MeetingMinutesResponse(BaseModel):
    meeting_summary: str = Field(
        ...,
        description="The comprehensive meeting summary with structured sections",
        example="""**Meeting Context:**
* **Project/Topic:** Q4 Product Launch Planning
* **Meeting Date:** October 26, 2023
* **Attendees:** Sarah (PM), Tom (Engineering), Maria (Marketing), David (Design)

**1. Executive Summary:** The team aligned on Q4 product launch timeline and resource allocation, with final go-live date set for December 15th.

**2. Key Decisions Made:**
• Launch date confirmed for December 15th, 2023
• Marketing budget approved at $150k for Q4 campaign
• Engineering team will deliver MVP by November 30th
• Beta testing phase scheduled for first week of December

**3. Action Items:**
• Finalize technical specifications: **Owner(s):** Tom, David - **Deadline:** November 1st
• Prepare marketing campaign materials: **Owner(s):** Maria - **Deadline:** November 15th
• Set up beta testing program: **Owner(s):** Sarah - **Deadline:** November 20th
• Conduct final security review: **Owner(s):** Tom - **Deadline:** December 1st

**4. Open Questions / For Next Meeting:**
• Pricing strategy for premium features needs final approval
• Customer support staffing requirements for launch week
• Integration testing timeline with third-party services"""
    )


class SocialMediaPostResponse(BaseModel):
    content: str = Field(
        ...,
        description="The generated social media post content",
        example="🚀 Just wrapped up an amazing week helping local restaurants streamline their operations!..."
    )
    image: Optional[str] = Field(
        None,
        description="Base64-encoded image data URL if image generation was requested",
        example="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
    )


class StandardResponse(BaseModel):
    content: str = Field(
        ...,
        description="The generated content or response",
        example="Generated content will appear here..."
    )


class ErrorResponse(BaseModel):
    error: str = Field(
        ...,
        description="Error message describing what went wrong",
        example="An error occurred while processing your request"
    )


class GeneralLLMRequest(BaseModel):
    prompt: str = Field(
        ...,
        description="The prompt to send to the LLM",
        example="Explain the benefits of machine learning in simple terms"
    )
    llm_model_name: Optional[str] = Field(
        None,
        description="The name of the LLM model to use (e.g., 'gemini-2.0-flash-001', 'gemini-1.5-flash-002')",
        example="gemini-2.0-flash-001"
    )
    llm_model_location: Optional[str] = Field(
        None,
        description="The location of the LLM model (e.g., 'us-central1', 'europe-west3')",
        example="europe-west4"
    )
    output_token_limit: Optional[int] = Field(
        8192,
        description="Maximum number of output tokens to generate",
        example=4096,
        ge=1,
        le=32768
    )
    temperature: Optional[float] = Field(
        1.0,
        description="Temperature for text generation (0.0 to 2.0)",
        example=0.7,
        ge=0.0,
        le=2.0
    )
    top_k: Optional[int] = Field(
        1,
        description="Top-k sampling parameter (1 to 40)",
        example=1,
        ge=1,
        le=40
    )
    top_p: Optional[float] = Field(
        1.0,
        description="Top-p sampling parameter (0.0 to 1.0)",
        example=0.8,
        ge=0.0,
        le=1.0
    ) 


class DocumentDigitalizationRequest(BaseModel):
    instruction: Optional[str] = Field(
        None,
        description="Optional instruction for what information to extract or target structure required",
        example="Extract only the customer name, address, and total amount from this invoice"
    )


class DocumentDigitalizationResponse(BaseModel):
    extracted_text: str = Field(
        ...,
        description="The extracted and digitalized text content from the document",
        example="Customer: John Smith\nAddress: 123 Main St, City, State 12345\nTotal Amount: $125.50"
    )
    processing_info: Optional[str] = Field(
        None,
        description="Additional information about the processing or any issues encountered",
        example="Successfully processed 1 page PDF document"
    ) 


class InvoiceValidatorRequest(BaseModel):
    sheet_name: str = Field(
        "Deckblatt",
        description="Sheet name in the invoice file to process",
        example="Deckblatt"
    )


class InvoiceValidatorResponse(BaseModel):
    output_file_path: str = Field(
        ...,
        description="Path to the validated invoice file with computed columns",
        example="/path/to/invoice_validated.xlsx"
    )
    validation_summary: str = Field(
        ...,
        description="Summary of the validation process and results",
        example="Validation completed successfully! Found 15 items with differences ranging from -5% to +25%"
    )
    processing_info: Optional[str] = Field(
        None,
        description="Additional processing information and statistics",
        example="Processed 20 invoice items against 150 Jira records"
    )


class DocumentAnalyzerResponse(BaseModel):
    analysis_result: str = Field(
        ...,
        description="The comprehensive document analysis result including step breakdown, analysis, and citations",
        example="""**STEP 1: INSTRUCTION BREAKDOWN**
1. Extract key financial data from quarterly reports
2. Compare revenue trends across documents
3. Identify potential risks or opportunities

**STEP 2: DOCUMENT ANALYSIS & RESPONSE**
Based on the analysis of the provided quarterly reports, the company shows strong revenue growth of 15% year-over-year...

**STEP 3: CITATIONS & SOURCES**
- Document references: Q3_Report.pdf, page 3, Revenue Section
- Key evidence: "Total revenue increased to $2.3M compared to $2.0M in Q2"
- Source reliability: Official quarterly report with verified financial data"""
    )
    processing_info: str = Field(
        ...,
        description="Information about the processed documents and analysis",
        example="Successfully analyzed 3 documents: 2 PDFs (5.2MB total), 1 Word document (1.1MB)"
    )
    documents_processed: List[str] = Field(
        ...,
        description="List of processed document filenames",
        example=["quarterly_report_Q3.pdf", "financial_summary.docx", "market_analysis.png"]
    )


class JobDescriptionRequest(BaseModel):
    job_title: str = Field(
        ...,
        description="The job title for the position",
        example="Senior UX/UI Designer (M/F/D)"
    )
    department: str = Field(
        ...,
        description="Department or team name with context",
        example="Design team, focusing on creating user-centric digital experiences"
    )
    employment_type: Optional[str] = Field(
        None,
        description="Type of employment",
        example="Full-time"
    )
    role_context: str = Field(
        ...,
        description="How this role fits into the bigger picture and contributes to the company's mission",
        example="Creating exceptional user experiences for digital tools serving the restaurant industry"
    )
    key_responsibilities: str = Field(
        ...,
        description="Main responsibilities and duties (3-4 key points)",
        example="Designing UX/UI elements, collaborating with design team, conducting usability tests, creating Jobs to be Done frameworks"
    )
    required_skills: str = Field(
        ...,
        description="Essential technical and professional skills",
        example="Deep understanding of UX/UI design principles, experience with JTBD frameworks, presentation skills, usability testing experience"
    )
    nice_to_have_skills: Optional[str] = Field(
        None,
        description="Preferred but not essential skills",
        example="Experience with segmentation frameworks, knowledge of additional design tools"
    )
    experience_level: str = Field(
        ...,
        description="Required years and type of experience",
        example="Few years of experience in a senior position with deep understanding of design principles"
    )
    soft_skills: str = Field(
        ...,
        description="Personality traits, interpersonal skills, and behavioral competencies needed",
        example="Passionate about user-centric design, confident in presenting ideas, initiative-taking, collaborative mindset"
    )
    special_benefits: Optional[str] = Field(
        None,
        description="Specific benefits or opportunities this role offers",
        example="Opportunity to make significant impact on growth and success, collaborative environment where ideas are valued"
    )


class JobDescriptionResponse(BaseModel):
    job_description: str = Field(
        ...,
        description="The complete generated job description",
        example="SENIOR UX/UI DESIGNER (M/F/D)\n\nYOUR CONTRIBUTION:\nAre you a visionary Senior Product Designer..."
    )
    template_sections: dict = Field(
        ...,
        description="Breakdown of each section for easy editing",
        example={
            "title": "SENIOR UX/UI DESIGNER (M/F/D)",
            "contribution": "Are you a visionary...",
            "responsibilities": "This role is part of...",
            "ingredients": "You will need to have...",
            "call_to_action": "Join our HoReCa revolution..."
        }
    )


class JobPosition(BaseModel):
    id: str = Field(
        ...,
        description="Unique identifier for the job position",
        example="1549397"
    )
    name: str = Field(
        ...,
        description="Name/title of the job position",
        example="Digital Sales Manager (m/w/d) im Außendienst - Berlin"
    )


class JobPositionsResponse(BaseModel):
    positions: List[JobPosition] = Field(
        ...,
        description="List of available job positions with their IDs and names",
        example=[
            {"id": "1549397", "name": "Digital Sales Manager (m/w/d) im Außendienst - Berlin"},
            {"id": "1788763", "name": "Digital Sales Manager (m/w/d) im Außendienst - Bremen"}
        ]
    )


class ChatMessage(BaseModel):
    role: str = Field(
        ...,
        description="The role of the message sender - either 'user' or 'model'",
        example="user"
    )
    message: str = Field(
        ...,
        description="The text content of the message",
        example="Hello, can you help me analyze this image?"
    )
    multimedia: Optional[List[str]] = Field(
        None,
        description="Optional list of base64-encoded multimedia content (images)",
        example=["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."]
    )


class MultiTurnChatRequest(BaseModel):
    prompt: List[ChatMessage] = Field(
        ...,
        description="List of messages representing the conversation history",
        example=[
            {
                "role": "user", 
                "message": "Hello, how are you?",
                "multimedia": None
            },
            {
                "role": "model",
                "message": "Hi! I'm doing well, thank you for asking. How can I help you today?",
                "multimedia": None
            },
            {
                "role": "user",
                "message": "Can you analyze this image for me?",
                "multimedia": ["data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/..."]
            }
        ]
    )
    llm_model_name: Optional[str] = Field(
        None,
        description="The name of the LLM model to use (e.g., 'gemini-2.0-flash-001', 'gemini-1.5-flash-002')",
        example="gemini-2.0-flash-001"
    )
    llm_model_location: Optional[str] = Field(
        None,
        description="The location of the LLM model (e.g., 'us-central1', 'europe-west3')",
        example="europe-west4"
    )
    output_token_limit: Optional[int] = Field(
        8192,
        description="Maximum number of output tokens to generate",
        example=4096,
        ge=1,
        le=32768
    )
    temperature: Optional[float] = Field(
        1.0,
        description="Temperature for text generation (0.0 to 2.0)",
        example=0.7,
        ge=0.0,
        le=2.0
    )
    top_k: Optional[int] = Field(
        1,
        description="Top-k sampling parameter (1 to 40)",
        example=1,
        ge=1,
        le=40
    )
    top_p: Optional[float] = Field(
        1.0,
        description="Top-p sampling parameter (0.0 to 1.0)",
        example=0.8,
        ge=0.0,
        le=1.0
    )


class MultiTurnChatResponse(BaseModel):
    content: str = Field(
        ...,
        description="The generated response from the model",
        example="I can see this is a beautiful landscape photo with mountains and a sunset. The colors are very vibrant with oranges and purples in the sky."
    )
    conversation_context: Optional[dict] = Field(
        None,
        description="Additional context about the conversation processing",
        example={
            "messages_processed": 3,
            "multimedia_items": 1,
            "total_tokens_used": 245
        }
    )