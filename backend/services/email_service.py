import logging
from modules.helper import loadConfig
from modules.llm import LLM

logger = logging.getLogger(__name__)


class EmailService:
    """Service class for email-related operations."""
    
    def __init__(self):
        self.llm = LLM()
    
    def generate_reply(self, subject: str, from_sender: str, email_content: str, 
                      tone: str, reply_type: str, length: str, priority: str, 
                      additional_instructions: str = None) -> str:
        """
        Generate an intelligent reply to an incoming email.
        
        Args:
            subject: The subject line of the original email
            from_sender: The sender of the original email
            email_content: The full content of the original email
            tone: The desired tone for the reply
            reply_type: The type of reply to generate
            length: The desired length of the reply
            priority: The priority level of the response
            additional_instructions: Additional specific instructions
            
        Returns:
            str: The generated email reply
        """
        try:
            # Load the email reply prompt template
            prompt_template = loadConfig('prompt.yml', namespace=False)['email-reply']
            
            # Format the prompt with the request data
            full_prompt = prompt_template.format(
                subject=subject,
                from_sender=from_sender,
                email_content=email_content,
                tone=tone,
                reply_type=reply_type,
                length=length,
                priority=priority,
                additional_instructions=additional_instructions or ""
            )
            
            # Generate the reply
            reply = self.llm.get_prediction(prompt=full_prompt)
            
            if not reply or not reply.strip():
                raise ValueError("Failed to generate email reply - empty response from AI model")
            
            return reply
            
        except Exception as e:
            logger.error(f"Error generating email reply: {str(e)}")
            raise
    
    def improve_email(self, email_content: str) -> str:
        """
        Enhance and improve the quality, tone, and clarity of an existing email draft.
        
        Args:
            email_content: The email content to improve
            
        Returns:
            str: The improved email content
        """
        try:
            # Load the email improvement prompt template
            prompt_template = loadConfig('prompt.yml', namespace=False)['email-improve']
            
            # Format the prompt with the email content
            full_prompt = prompt_template.format(email_content=email_content)
            
            # Generate the improved email
            improved_email = self.llm.get_prediction(prompt=full_prompt)
            
            if not improved_email or not improved_email.strip():
                raise ValueError("Failed to improve email - empty response from AI model")
            
            return improved_email
            
        except Exception as e:
            logger.error(f"Error improving email: {str(e)}")
            raise 