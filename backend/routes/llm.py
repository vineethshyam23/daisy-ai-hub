from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse
import logging

from models import GeneralLLMRequest, StandardResponse, ErrorResponse, MultiTurnChatRequest, MultiTurnChatResponse
from modules.llm import LLM

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/llm", tags=["General LLM"])


@router.post(
    "/general",
    status_code=status.HTTP_200_OK,
    response_model=StandardResponse,
    summary="General LLM Endpoint",
    description="A flexible LLM endpoint that allows you to specify the model name, location, output token limit, and other generation parameters. Send any prompt and get a response from the specified Gemini model.",
    responses={
        200: {
            "description": "Successfully generated LLM response",
            "content": {
                "application/json": {
                    "example": {
                        "content": "Machine learning is a subset of artificial intelligence that enables computers to learn and make decisions from data without being explicitly programmed. The benefits include: 1) Automation of complex tasks, 2) Pattern recognition in large datasets, 3) Predictive analytics for better decision making, 4) Personalization of user experiences, and 5) Continuous improvement through learning from new data."
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
async def general_llm(request: GeneralLLMRequest):
    """
    General LLM endpoint that accepts custom model parameters and prompts.
    """
    try:
        # Initialize the LLM with custom parameters if provided
        llm = LLM(
            model_name=request.llm_model_name,
            model_location=request.llm_model_location,
            max_output_tokens=request.output_token_limit,
            temperature=request.temperature,
            top_k=request.top_k,
            top_p=request.top_p
        )
        
        # Get prediction with the provided prompt
        response = llm.get_prediction(prompt=request.prompt)
        
        # Return the generated response
        return JSONResponse(content={"content": response})
        
    except Exception as e:
        logger.error(f"Error in general LLM endpoint: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        )


@router.post(
    "/chat",
    status_code=status.HTTP_200_OK,
    response_model=MultiTurnChatResponse,
    summary="Multi-Turn Chat Endpoint",
    description="A multi-turn chat endpoint that maintains conversation history and supports multimedia content. Send a conversation thread with message history and get contextual responses from the specified Gemini model.",
    responses={
        200: {
            "description": "Successfully generated chat response",
            "content": {
                "application/json": {
                    "example": {
                        "content": "I can see the image you shared shows a beautiful landscape. The mountains in the background create a stunning contrast with the sunset colors. Based on our previous conversation about travel destinations, this looks like exactly the kind of scenic location you were looking for!",
                        "conversation_context": {
                            "messages_processed": 4,
                            "multimedia_items": 1,
                            "total_tokens_used": 187
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
async def multi_turn_chat(request: MultiTurnChatRequest):
    """
    Multi-turn chat endpoint that maintains conversation history and supports multimedia content.
    
    This endpoint processes a conversation thread with multiple messages, maintaining context
    across turns and supporting base64-encoded images within messages.
    """
    try:
        # Initialize the LLM with custom parameters if provided
        llm = LLM(
            model_name=request.llm_model_name,
            model_location=request.llm_model_location,
            max_output_tokens=request.output_token_limit,
            temperature=request.temperature,
            top_k=request.top_k,
            top_p=request.top_p
        )
        
        # Convert Pydantic models to dictionaries for the LLM method
        messages = []
        total_multimedia_items = 0
        
        for msg in request.prompt:
            message_dict = {
                'role': msg.role,
                'message': msg.message,
                'multimedia': msg.multimedia or []
            }
            if msg.multimedia:
                total_multimedia_items += len(msg.multimedia)
            messages.append(message_dict)
        
        # Get prediction with conversation history
        response = llm.get_multi_turn_chat_prediction(messages=messages)
        
        # Create conversation context info
        conversation_context = {
            "messages_processed": len(messages),
            "multimedia_items": total_multimedia_items,
            "model_used": request.llm_model_name or llm.model_name
        }
        
        # Return the generated response
        return JSONResponse(content={
            "content": response,
            "conversation_context": conversation_context
        })
        
    except Exception as e:
        logger.error(f"Error in multi-turn chat endpoint: {str(e)}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"error": str(e)}
        ) 