from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse
import logging

from models import EmailReplyRequest, Query, StandardResponse, ErrorResponse
from services.email_service import EmailService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/email", tags=["Email Assistant"])


@router.post(
    "/reply",
    status_code=status.HTTP_200_OK,
    response_model=StandardResponse,
    summary="Generate Email Reply",
    description="Generate an intelligent reply to an incoming email using AI. Customize tone, reply type, length, and priority to create the perfect response.",
    responses={
        200: {
            "description": "Successfully generated email reply",
            "content": {
                "application/json": {
                    "example": {
                        "content": "Dear John,\n\nThank you for your email regarding the project proposal. I appreciate your interest in discussing the pricing details.\n\nI'd be happy to schedule a meeting next week to go over everything in detail. I have availability on Tuesday afternoon or Wednesday morning. Please let me know which time works better for your schedule.\n\nLooking forward to our discussion.\n\nBest regards,\n[Your name]"
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def email_reply(request: EmailReplyRequest):
    """
    Generate an intelligent reply to an incoming email using AI.
    """
    try:
        email_service = EmailService()
        reply = email_service.generate_reply(
            subject=request.subject,
            from_sender=request.from_sender,
            email_content=request.email_content,
            tone=request.tone,
            reply_type=request.reply_type,
            length=request.length,
            priority=request.priority,
            additional_instructions=request.additional_instructions
        )
        
        return JSONResponse(content={"content": reply})
        
    except ValueError as e:
        logger.error(f"Validation error in email reply generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in email reply generation: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error generating email reply: {str(e)}"}
        )


@router.post(
    "/improve",
    status_code=status.HTTP_200_OK,
    response_model=StandardResponse,
    summary="Improve Email Content",
    description="Enhance and improve the quality, tone, and clarity of an existing email draft using AI assistance.",
    responses={
        200: {
            "description": "Successfully improved email content",
            "content": {
                "application/json": {
                    "example": {
                        "content": "Dear [Recipient], I hope this message finds you well. I wanted to follow up on our previous discussion regarding the project proposal. After careful consideration of your feedback, I believe we can address your concerns about the timeline and budget..."
                    }
                }
            }
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def improve_email(query: Query):
    """
    Enhance and improve the quality, tone, and clarity of an existing email draft.
    """
    try:
        email_service = EmailService()
        improved_email = email_service.improve_email(email_content=query.email)
        
        return JSONResponse(content={"content": improved_email})
        
    except ValueError as e:
        logger.error(f"Validation error in email improvement: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in email improvement: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error improving email: {str(e)}"}
        ) 