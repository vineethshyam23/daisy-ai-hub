from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse
import logging

from models import SocialMediaPostRequest, SocialMediaPostResponse, ErrorResponse
from services.content_service import ContentService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/social-media", tags=["Content Creation"])


@router.post(
    "/post",
    status_code=status.HTTP_200_OK,
    response_model=SocialMediaPostResponse,
    summary="Generate Social Media Post",
    description="Create engaging social media posts tailored to specific platforms, topics, and audiences using AI content generation with customizable tone, style, and formatting options. Optionally generate accompanying images.",
    responses={
        200: {
            "description": "Successfully generated social media post with optional image",
            "content": {
                "application/json": {
                    "example": {
                        "content": "🚀 Just wrapped up an amazing week helping teams work smarter with AI!\n\nOne of the most rewarding moments: seeing how automation reduced manual work by 30% and freed up time for what actually matters.\n\nIt's incredible to see how the right technology can transform how teams operate. 🌱\n\nWhat challenges are you facing in your daily operations?\n\n#AI #Productivity #DigitalTransformation #Automation",
                        "image": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
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
async def social_media_post(request: SocialMediaPostRequest):
    """
    Create engaging social media posts with optional image generation.
    """
    try:
        content_service = ContentService()
        result = content_service.generate_social_media_post(
            topic=request.topic,
            key_message=request.key_message,
            target_audience=request.target_audience,
            call_to_action=request.call_to_action,
            platform=request.platform,
            tone=request.tone,
            content_style=request.content_style,
            include_hashtags=request.include_hashtags,
            include_emojis=request.include_emojis,
            generate_image=request.generate_image
        )
        
        return JSONResponse(content=result)
        
    except ValueError as e:
        logger.error(f"Validation error in social media post generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in social media post generation: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error generating social media post: {str(e)}"}
        ) 