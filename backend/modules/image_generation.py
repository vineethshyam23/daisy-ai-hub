from vertexai.preview.vision_models import ImageGenerationModel
import vertexai
from .helper import loadConfig
import logging
import os

# Use centralized logging configuration
try:
    from config import get_logger
    logger = get_logger(__name__)
except ImportError:
    # Fallback to basic logging if config module is not available
    logger = logging.getLogger(__name__)

class ImageGenerator(object):
    def __init__(
            self,
            model_name=None
    ):
        try:
            # Load configuration from gcp.yml
            self.config = loadConfig('gcp.yml', namespace=False)
            
            # Use provided model_name or default from config
            self.model_name = model_name or self.config.get('image_model_name')
            
            # Get image settings from config
            self.image_settings = self.config.get('image_settings', {})
            
            # Initialize Vertex AI with project and location from config
            project_id = self.config.get('project_id')
            location = self.config.get('image_model_location')
            
            logger.info(f"Initializing Vertex AI with project: {project_id}, location: {location}")
            
            # Log the authentication method being used
            credentials_file = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
            if credentials_file:
                logger.info(f"Using service account credentials from: {credentials_file}")
            else:
                logger.info("No GOOGLE_APPLICATION_CREDENTIALS found, using default credentials")
            
            vertexai.init(
                project=project_id,
                location=location
            )
            
            # Load the image generation model
            logger.info(f"Loading image generation model: {self.model_name}")
            self.generation_model = ImageGenerationModel.from_pretrained(self.model_name)
            logger.info("Image generation model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error initializing ImageGenerator: {str(e)}")
            raise
    
    def generate_images(
            self, 
            prompt, 
            number_of_images=1, 
            aspect_ratio="1:1", 
            negative_prompt="",
            person_generation=None, 
            safety_filter_level=None, 
            add_watermark=None
    ):
        """
        Generate images based on the provided prompt and parameters
        
        Args:
            prompt (str): The text prompt to generate images from
            number_of_images (int): Number of images to generate (1-4)
            aspect_ratio (str): Aspect ratio of the generated images ("1:1", "16:9", "9:16", etc.)
            negative_prompt (str): Concepts to avoid in the generated images
            person_generation (str): Settings for generating people, defaults to config value
            safety_filter_level (str): Safety filter settings, defaults to config value
            add_watermark (bool): Whether to add a watermark, defaults to config value
            
        Returns:
            list: List of base64-encoded image data URLs
        """
        try:
            # Use parameters from config if not explicitly provided
            if person_generation is None:
                person_generation = self.image_settings.get('person_generation', 'allow_adult')
                
            if safety_filter_level is None:
                safety_filter_level = self.image_settings.get('safety_filter_level', 'block_few')
                
            if add_watermark is None:
                add_watermark = self.image_settings.get('add_watermark', True)
            
            logger.info(f"Generating images with prompt: '{prompt[:50]}...', "
                       f"number_of_images: {number_of_images}, "
                       f"aspect_ratio: {aspect_ratio}, "
                       f"person_generation: {person_generation}, "
                       f"safety_filter_level: {safety_filter_level}")
            
            response = self.generation_model.generate_images(
                prompt=prompt,
                number_of_images=number_of_images,
                aspect_ratio=aspect_ratio,
                negative_prompt=negative_prompt,
                person_generation=person_generation,
                safety_filter_level=safety_filter_level,
                add_watermark=add_watermark
            )

            # Extract base64 data from the response
            image_data_urls = []
            for image in response.images:
                try:
                    # Get the base64 string from the image
                    base64_string = image._as_base64_string()
                    # Create a proper data URL with the base64 data
                    data_url = f"data:image/png;base64,{base64_string}"
                    image_data_urls.append(data_url)
                except Exception as img_error:
                    logger.error(f"Error extracting base64 from image: {str(img_error)}")
                    continue
            
            if not image_data_urls:
                logger.warning("No images were successfully processed from the response")
            else:
                logger.info(f"Successfully processed {len(image_data_urls)} images")
            
            return image_data_urls
            
        except Exception as e:
            logger.error(f"Error generating images: {str(e)}")
            raise 