import logging
from modules.helper import loadConfig
from modules.llm import LLM
from modules.image_generation import ImageGenerator

logger = logging.getLogger(__name__)


class ContentService:
    """Service class for content generation operations."""
    
    def __init__(self):
        self.llm = LLM()
        self.image_generator = ImageGenerator()
    
    def generate_social_media_post(self, topic: str, key_message: str, target_audience: str,
                                 call_to_action: str, platform: str, tone: str, 
                                 content_style: str, include_hashtags: bool, 
                                 include_emojis: bool, generate_image: bool = False) -> dict:
        """
        Create engaging social media posts with optional image generation.
        
        Args:
            topic: The main topic of the social media post
            key_message: The detailed key message or content for the post
            target_audience: The target audience for this post
            call_to_action: Optional call to action for the post
            platform: The social media platform for the post
            tone: The desired tone for the post
            content_style: The style of content to create
            include_hashtags: Whether to include hashtags in the post
            include_emojis: Whether to include emojis in the post
            generate_image: Whether to generate an accompanying image
            
        Returns:
            dict: Contains 'content' and optionally 'image'
        """
        try:
            # Load the social media post prompt template
            prompt_template = loadConfig('prompt.yml', namespace=False)['social-media-post']
            
            # Generate dynamic instructions based on request parameters
            hashtag_instruction = "Include relevant hashtags at the end of the post" if include_hashtags else "Do not include any hashtags"
            emoji_instruction = "Use emojis appropriately to enhance engagement" if include_emojis else "Do not use any emojis"
            
            # Format the prompt with the request data
            full_prompt = prompt_template.format(
                topic=topic,
                key_message=key_message,
                target_audience=target_audience,
                call_to_action=call_to_action or "",
                platform=platform,
                tone=tone,
                content_style=content_style,
                hashtag_instruction=hashtag_instruction,
                emoji_instruction=emoji_instruction
            )
            
            # Generate the post content
            post_content = self.llm.get_prediction(prompt=full_prompt)
            
            if not post_content or not post_content.strip():
                raise ValueError("Failed to generate social media post - empty response from AI model")
            
            # Generate image if requested
            generated_image = None
            if generate_image:
                try:
                    # Create image prompt based on the post content
                    image_prompt = f"Create a professional, engaging image for a social media post about: {topic}. The image should be suitable for {platform} and match the {tone} tone."
                    
                    images = self.image_generator.generate_images(
                        prompt=image_prompt,
                        number_of_images=1,
                        aspect_ratio="1:1",  # Square format for most social media platforms
                        negative_prompt="text, watermark, logo, blurry, low quality"
                    )
                    
                    # images is now a list of base64 data URLs
                    if images and len(images) > 0:
                        generated_image = images[0]
                        
                except Exception as image_error:
                    logger.warning(f"Failed to generate image for social media post: {str(image_error)}")
                    # Don't fail the entire request if image generation fails
                    generated_image = None
            
            return {
                "content": post_content,
                "image": generated_image
            }
            
        except Exception as e:
            logger.error(f"Error generating social media post: {str(e)}")
            raise
    
    def get_shopping_recommendations(self, query: str) -> str:
        """
        Get personalized shopping recommendations and gift suggestions.
        
        Args:
            query: The shopping query or preferences
            
        Returns:
            str: The shopping recommendations
        """
        try:
            # Load the shopping assistant prompt template
            prompt_template = loadConfig('prompt.yml', namespace=False)['shopping-assistant']
            
            # Format the prompt with the query
            full_prompt = prompt_template.format(query=query)
            
            # Generate recommendations
            recommendations = self.llm.get_prediction(prompt=full_prompt)
            
            if not recommendations or not recommendations.strip():
                raise ValueError("Failed to generate shopping recommendations - empty response from AI model")
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating shopping recommendations: {str(e)}")
            raise 