from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse
import logging

from models import InterviewQuestionRequest, LearningPathRequest, LearningPathResponse, StandardResponse, ErrorResponse, JobDescriptionRequest, JobDescriptionResponse, JobPositionsResponse
from services.career_service import CareerService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/career", tags=["Career Assistant"])


@router.post(
    "/interview-questions",
    status_code=status.HTTP_200_OK,
    response_model=StandardResponse,
    summary="Generate Interview Questions",
    description="Generate relevant interview questions based on a job ID from your configured career portal. Fetches the job description from both English and German feeds to create targeted questions for interview preparation.",
    responses={
        200: {
            "description": "Successfully generated interview questions",
            "content": {
                "application/json": {
                    "example": {
                        "content": "Based on the job posting for Digital Sales Manager, here are some relevant interview questions you should prepare for:\n\n1. Can you describe your experience in B2B digital solutions sales?\n2. How do you approach customer relationship building in the HoReCa industry?\n3. Tell us about your experience with field sales and customer acquisition...\n\n[Additional questions and preparation tips would follow]"
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
async def generate_interview_questions(request: InterviewQuestionRequest):
    """
    Generate relevant interview questions based on a job ID from your configured career portal.
    """
    try:
        career_service = CareerService()
        questions = career_service.generate_interview_questions(job_id=request.job_id)
        
        return JSONResponse(content={"content": questions})
        
    except ValueError as e:
        logger.error(f"Validation error in interview questions generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in interview questions generation: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error generating interview questions: {str(e)}"}
        )


@router.post(
    "/learning-path",
    status_code=status.HTTP_200_OK,
    response_model=LearningPathResponse,
    summary="Generate Learning Path",
    description="Generate a personalized learning path based on the skill, skill level, target time, and study commitment.",
    responses={
        200: {
            "description": "Successfully generated learning path",
            "content": {
                "application/json": {
                    "example": {
                        "content": "# Data Science Learning Path\n\n## Personalized Overview\nThis 6-month learning path is designed for beginners...",
                        "citations": {
                            "search_queries": ["data science learning resources"],
                            "sources": [
                                {"title": "coursera.org", "uri": "https://..."},
                                {"title": "kaggle.com", "uri": "https://..."}
                            ],
                            "num_sources": 5
                        }
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
async def generate_learning_path(request: LearningPathRequest):
    """
    Generate a personalized learning path based on skill and preferences.
    """
    try:
        career_service = CareerService()
        result = career_service.generate_learning_path(
            skill=request.skill,
            skill_level=request.skill_level,
            target_time=request.target_time,
            study_commitment=request.study_commitment
        )
        
        return JSONResponse(content=result)
        
    except ValueError as e:
        logger.error(f"Validation error in learning path generation: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in learning path generation: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": f"Unexpected error generating learning path: {str(e)}"}
        )


@router.post(
    "/job-description",
    response_model=JobDescriptionResponse,
    responses={400: {"model": ErrorResponse}, 500: {"model": ErrorResponse}},
    summary="Generate Job Description",
    description="Generate a comprehensive job description following a structured template and branding guidelines."
)
async def generate_job_description(request: JobDescriptionRequest):
    """
    Generate a structured job description using a configurable template format.

    This endpoint creates compelling job descriptions that:
    - Follow a structured template
    - Include all required sections (Contribution, Responsibilities, Requirements, etc.)
    - Maintain consistent brand voice and mission focus
    - Ensure gender-neutral language
    """
    try:
        logger.info(f"Generating job description for: {request.job_title}")
        
        career_service = CareerService()
        result = career_service.generate_job_description(
            job_title=request.job_title,
            department=request.department,
            employment_type=request.employment_type,
            role_context=request.role_context,
            key_responsibilities=request.key_responsibilities,
            required_skills=request.required_skills,
            nice_to_have_skills=request.nice_to_have_skills,
            experience_level=request.experience_level,
            soft_skills=request.soft_skills,
            special_benefits=request.special_benefits
        )
        
        return JobDescriptionResponse(
            job_description=result["job_description"],
            template_sections=result["template_sections"]
        )
        
    except Exception as e:
        logger.error(f"Error in job description generation endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate job description: {str(e)}")


@router.get(
    "/open-positions",
    status_code=status.HTTP_200_OK,
    response_model=JobPositionsResponse,
    summary="Get Open Positions",
    description="Fetch all currently open job positions from the configured career portal. Returns a list of positions with their IDs and names for use in interview question generation.",
    responses={
        200: {
            "description": "Successfully retrieved open positions",
            "content": {
                "application/json": {
                    "example": {
                        "positions": [
                            {"id": "1549397", "name": "Digital Sales Manager (m/w/d) im Außendienst - Berlin"},
                            {"id": "1788763", "name": "Digital Sales Manager (m/w/d) im Außendienst - Bremen"},
                            {"id": "2157593", "name": "Lead Architect (m/f/d)"}
                        ]
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
async def get_open_positions():
    """
    Retrieve all currently open job positions from the configured career portal.

    This endpoint fetches the latest job openings directly from the XML feed
    and returns them in a structured format suitable for interview question generation
    and other career-related services.
    """
    try:
        career_service = CareerService()
        positions_data = career_service.get_open_positions()
        
        return JobPositionsResponse(positions=positions_data)
        
    except ValueError as e:
        logger.error(f"Validation error in open positions retrieval: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        logger.error(f"Unexpected error in open positions retrieval: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Unexpected error retrieving open positions: {str(e)}"
        ) 