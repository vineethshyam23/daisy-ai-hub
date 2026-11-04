from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse
import logging

from models import Query, StandardResponse, ErrorResponse
from services.content_service import ContentService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/shopping", tags=["Shopping Assistant"])


@router.post(
    "/assistant",
    status_code=status.HTTP_200_OK,
    response_model=StandardResponse,
    summary="Get Shopping Recommendations",
    description="Get personalized shopping recommendations and gift suggestions based on budget and preferences using AI.",
    responses={
        200: {
            "description": "Successfully generated shopping recommendations",
            "content": {
                "application/json": {
                    "example": {
                        "content": "Based on your budget, here are some great gift recommendations: 1. A premium coffee subscription ($25-30/month) 2. A cozy reading nook setup with a soft throw blanket and book light ($40-50) 3. A gourmet cooking spice set ($35-45)..."
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
async def shopping_assistant(query: Query):
    """
    Get personalized shopping recommendations and gift suggestions.
    """
    try:
        content_service = ContentService()
        recommendations = content_service.get_shopping_recommendations(query=query.email)
        
        return JSONResponse(content={"content": recommendations})
        
    except ValueError as e:
        logger.error(f"Validation error in shopping assistant: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in shopping assistant: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error generating shopping recommendations: {str(e)}"}
        ) 