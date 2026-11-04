import logging
import re
import requests
import xml.etree.ElementTree as ET
from modules.helper import loadConfig
from modules.llm import LLM

logger = logging.getLogger(__name__)


class CareerService:
    """Service class for career-related operations."""
    
    def __init__(self):
        self.llm = LLM()
    
    def generate_interview_questions(self, job_id: str) -> str:
        """
        Generate relevant interview questions based on a job ID from the configured career portal.

        Args:
            job_id: The job ID from the career portal XML feed
            
        Returns:
            str: The generated interview questions
        """
        try:
            # Fetch the job description using the job ID
            job_description = self.get_job_description_by_id(job_id)
            
            if not job_description:
                raise ValueError(f"No job description found for job ID: {job_id}")
            
            # Load the interview questions prompt template
            prompt_template = loadConfig('prompt.yml', namespace=False)['interview-questions']
            
            # Format the prompt with the job description instead of URL
            full_prompt = prompt_template.format(job_description=job_description)
            
            # Generate interview questions
            questions = self.llm.get_prediction(prompt=full_prompt)
            
            if not questions or not questions.strip():
                raise ValueError("Failed to generate interview questions - empty response from AI model")
            
            return questions
            
        except Exception as e:
            logger.error(f"Error generating interview questions: {str(e)}")
            raise
    
    def generate_learning_path(self, skill: str, skill_level: str, target_time: str, 
                             study_commitment: str) -> dict:
        """
        Generate a personalized learning path based on skill and preferences.
        
        Args:
            skill: The topic, skill, or job title to create a learning path for
            skill_level: Current skill level (e.g., Beginner, Intermediate, Advanced)
            target_time: Target timeline for completing the learning path
            study_commitment: How much time can be committed to studying per week
            
        Returns:
            dict: Contains 'content' and 'citations'
        """
        try:
            # Load the learning path prompt template
            prompt_template = loadConfig('prompt.yml', namespace=False)['learning-path']
            
            # Format the prompt with the request data
            full_prompt = prompt_template.format(
                skill=skill,
                skill_level=skill_level,
                target_time=target_time,
                study_commitment=study_commitment
            )
            
            # Generate learning path
            learning_path = self.llm.get_prediction(prompt=full_prompt)
            
            if not learning_path or not learning_path.strip():
                raise ValueError("Failed to generate learning path - empty response from AI model")
            
            # For now, return a simple response structure
            # In a real implementation, you might want to parse the response to extract citations
            citations = {
                "search_queries": [f"{skill} learning resources"],
                "sources": [],
                "num_sources": 0
            }
            
            return {
                "content": learning_path,
                "citations": citations
            }
            
        except Exception as e:
            logger.error(f"Error generating learning path: {str(e)}")
            raise
    
    def generate_job_description(self, job_title: str, department: str, employment_type: str, 
                               role_context: str, key_responsibilities: str, required_skills: str, 
                               nice_to_have_skills: str, experience_level: str, soft_skills: str, 
                               special_benefits: str) -> dict:
        """
        Generate a comprehensive job description following a structured template.

        Args:
            job_title: The job title for the position
            department: Department or team name with context
            employment_type: Type of employment
            role_context: How this role fits into the company's mission
            key_responsibilities: Main responsibilities and duties
            required_skills: Essential technical and professional skills
            nice_to_have_skills: Preferred but not essential skills
            experience_level: Required years and type of experience
            soft_skills: Personality traits and behavioral competencies
            special_benefits: Specific benefits this role offers
            
        Returns:
            dict: Contains 'job_description' and 'template_sections'
        """
        try:
            # Load the job description prompt template
            prompt_template = loadConfig('prompt.yml', namespace=False)['job-description-generator']
            
            # Format the prompt with all the parameters
            full_prompt = prompt_template.format(
                job_title=job_title,
                department=department,
                employment_type=employment_type or "",
                role_context=role_context,
                key_responsibilities=key_responsibilities,
                required_skills=required_skills,
                nice_to_have_skills=nice_to_have_skills or "",
                experience_level=experience_level,
                soft_skills=soft_skills,
                special_benefits=special_benefits or ""
            )
            
            # Generate the job description
            job_description = self.llm.get_prediction(prompt=full_prompt)
            
            if not job_description or not job_description.strip():
                raise ValueError("Failed to generate job description - empty response from AI model")
            
            # Parse sections for easy editing (basic implementation)
            sections = self._parse_job_description_sections(job_description)
            
            return {
                "job_description": job_description,
                "template_sections": sections
            }
            
        except Exception as e:
            logger.error(f"Error generating job description: {str(e)}")
            raise
    
    def _parse_job_description_sections(self, job_description: str) -> dict:
        """Parse job description into sections for easier editing."""
        sections = {}
        current_section = ""
        current_content = []
        
        for line in job_description.split('\n'):
            line = line.strip()
            if not line:
                continue
                
            # Detect section headers
            if any(header in line.upper() for header in ['YOUR CONTRIBUTION:', 'MENU OF RESPONSIBILITIES', 'INGREDIENTS FOR SUCCESS:', 'RECIPE CARD', 'JOIN OUR HORECA REVOLUTION']):
                if current_section and current_content:
                    sections[current_section] = '\n'.join(current_content).strip()
                current_section = line.lower().replace(':', '').replace(' ', '_')
                current_content = []
            else:
                current_content.append(line)
        
        # Add the last section
        if current_section and current_content:
            sections[current_section] = '\n'.join(current_content).strip()
            
        return sections
    
    def get_job_description_by_id(self, job_id: str) -> str:
        """
        Fetch job description for a specific job ID from both English and German XML feeds.
        
        Args:
            job_id: The job ID to search for
            
        Returns:
            str: Combined job description from available languages
        """
        try:
            # URLs for both language versions — configure CAREER_PORTAL_XML_FEED_URL in env
            import os
            base_url = os.environ.get("CAREER_PORTAL_XML_FEED_URL", "https://your-company.jobs.personio.de/xml")
            urls = {
                'en': f"{base_url}?language=en",
                'de': f"{base_url}?language=de"
            }
            
            job_descriptions = {}
            job_title = ""
            
            # Fetch from both XML feeds
            for lang, url in urls.items():
                try:
                    response = requests.get(url, timeout=30)
                    response.raise_for_status()
                    
                    # Parse the XML
                    root = ET.fromstring(response.content)
                    
                    # Find the position with matching ID
                    for position in root.findall('.//position'):
                        position_id_elem = position.find('id')
                        if position_id_elem is not None and position_id_elem.text.strip() == job_id:
                            # Get job title
                            name_elem = position.find('name')
                            if name_elem is not None and not job_title:
                                job_title = name_elem.text.strip()
                            
                            # Get job descriptions (there can be multiple sections)
                            job_desc_container = position.find('jobDescriptions')
                            if job_desc_container is not None:
                                job_sections = []
                                for job_desc in job_desc_container.findall('jobDescription'):
                                    name_elem = job_desc.find('name')
                                    value_elem = job_desc.find('value')
                                    
                                    if name_elem is not None and value_elem is not None:
                                        section_name = name_elem.text.strip() if name_elem.text else ""
                                        section_value = value_elem.text.strip() if value_elem.text else ""
                                        
                                        if section_name and section_value:
                                            # Clean up HTML tags and CDATA
                                            section_value = re.sub(r'<[^>]+>', '', section_value)  # Remove HTML tags
                                            section_value = section_value.replace('&amp;', '&')  # Decode HTML entities
                                            job_sections.append(f"{section_name}\n{section_value}")
                                
                                if job_sections:
                                    job_descriptions[lang] = '\n\n'.join(job_sections)
                            break
                            
                except requests.RequestException as e:
                    logger.warning(f"Failed to fetch {lang.upper()} XML feed: {str(e)}")
                    continue
                except ET.ParseError as e:
                    logger.warning(f"Failed to parse {lang.upper()} XML: {str(e)}")
                    continue
            
            # Combine descriptions
            if not job_descriptions and not job_title:
                return ""
            
            combined_description = f"Job Title: {job_title}\n\n"
            
            if 'en' in job_descriptions and 'de' in job_descriptions:
                combined_description += f"English Description:\n{job_descriptions['en']}\n\n"
                combined_description += f"German Description:\n{job_descriptions['de']}"
            elif 'en' in job_descriptions:
                combined_description += f"Description:\n{job_descriptions['en']}"
            elif 'de' in job_descriptions:
                combined_description += f"Description (German):\n{job_descriptions['de']}"
            else:
                combined_description += "No detailed job description available."
            
            logger.info(f"Successfully fetched job description for job ID {job_id}")
            return combined_description
            
        except Exception as e:
            logger.error(f"Unexpected error fetching job description for ID {job_id}: {str(e)}")
            raise ValueError(f"Failed to fetch job description: {str(e)}")
    
    def get_open_positions(self) -> list:
        """
        Fetch all open positions from the configured career portal XML feed.
        
        Returns:
            list: List of dictionaries containing job position id and name
        """
        try:
            import os
            base_url = os.environ.get("CAREER_PORTAL_XML_FEED_URL", "https://your-company.jobs.personio.de/xml")
            url = f"{base_url}?language=en"
            
            # Fetch the XML data
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            
            # Parse the XML
            root = ET.fromstring(response.content)
            
            positions = []
            # Find all position elements
            for position in root.findall('.//position'):
                position_id = position.find('id')
                position_name = position.find('name')
                
                if position_id is not None and position_name is not None:
                    positions.append({
                        "id": position_id.text.strip(),
                        "name": position_name.text.strip()
                    })
            
            logger.info(f"Successfully fetched {len(positions)} job positions")
            return positions
            
        except requests.RequestException as e:
            logger.error(f"Error fetching job positions from API: {str(e)}")
            raise ValueError(f"Failed to fetch job positions: {str(e)}")
        except ET.ParseError as e:
            logger.error(f"Error parsing XML response: {str(e)}")
            raise ValueError(f"Failed to parse job positions data: {str(e)}")
        except Exception as e:
            logger.error(f"Unexpected error fetching job positions: {str(e)}")
            raise 