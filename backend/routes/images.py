from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse
import logging
from typing import List

from models import ImageGenerationRequest, ErrorResponse
from modules.image_generation import ImageGenerator

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/images", tags=["Image Generation"])


@router.post(
    "/generate",
    status_code=status.HTTP_200_OK,
    response_model=List[str],
    summary="Generate AI Images",
    description="Generate high-quality images from text prompts using advanced AI image generation models. Supports various aspect ratios, safety filters, and customization options.",
    responses={
        200: {
            "description": "Successfully generated images",
            "content": {
                "application/json": {
                    "example": [
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg==",
                        "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8/5+hHgAHggJ/PchI7wAAAABJRU5ErkJggg=="
                    ]
                }
            }
        },
        500: {
            "description": "Internal server error",
            "model": ErrorResponse
        }
    }
)
async def generate_images(request: ImageGenerationRequest):
    """
    Generate high-quality images from text prompts using AI.
    """
    try:
        # Initialize the image generator
        try:
            image_generator = ImageGenerator()
        except Exception as init_error:
            logger.error(f"Failed to initialize image generator: {str(init_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize image generation service: {str(init_error)}"
            )
        
        # Generate images
        try:
            images = image_generator.generate_images(
                prompt=request.prompt,
                number_of_images=request.number_of_images,
                aspect_ratio=request.aspect_ratio,
                negative_prompt=request.negative_prompt,
                person_generation=request.person_generation,
                safety_filter_level=request.safety_filter_level,
                add_watermark=request.add_watermark
            )
            
            if not images:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to generate images - empty response from image generation service"
                )
                
        except Exception as generation_error:
            logger.error(f"Image generation error: {str(generation_error)}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to generate images: {str(generation_error)}"
            )
        
        # Return the generated images
        return JSONResponse(content=images)
        
    except HTTPException:
        # Re-raise HTTP exceptions (validation errors)
        raise
    except Exception as e:
        logger.error(f"Unexpected error in image generation: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error generating images: {str(e)}"}
        ) 