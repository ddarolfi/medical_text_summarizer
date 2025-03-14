# core/openai_client.py
import logging
from typing import Optional
import os
from openai import OpenAI


# Load environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
MAX_RETRIES = 3

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenAIClient:
    """Client for interacting with OpenAI API to generate summaries."""
    def __init__(self, model: str = "gpt-4o-mini", api_key: Optional[str] = None):
        """
        Initialize the OpenAI client.
        
        Args:
            model: The OpenAI model to use (default: gpt-4)
            api_key: OpenAI API key (if None, loads from settings)
        """
        self.model = model
        self.api_key = api_key or OPENAI_API_KEY
        print(self.api_key)
        self.client = OpenAI(api_key=self.api_key)
    def summarize(self, text: str, max_tokens: int = 500) -> str:
        """
        Generate a summary of the provided text.
        
        Args:
            text: The text to summarize
            max_tokens: Maximum number of tokens in the summary
            
        Returns:
            str: The generated summary
        """
        prompt = f"Please provide a concise summary of the following text:\n\n{text}"
        
        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.responses.create(
                    model=self.model,
                    instructions="You are a helpful medical assistant that summarizes text accurately and concisely. Keep all dates and important details, and make sure the summary is easy to understand with structure.",
                    input =prompt,
                    temperature=0.3, 
                )
                
                summary = response.choices[0].message.content.strip()
                return summary

            except Exception as e:
                logger.error(f"Unexpected error: {str(e)}")
                raise
                
        raise Exception(f"Failed to summarize text after {MAX_RETRIES} attempts")
    
    def chunk_summarize(self, chunks: list, max_tokens: int = 300) -> str:
        """
        Split text into chunks and summarize each chunk, then combine summaries.
        Useful for longer texts that exceed token limits.
        
        Args:
            chunks: The chunks of text to summarize
            max_tokens: Maximum tokens for the final summary
            
        Returns:
            str: The combined summary
        """
        if len(chunks) == 1:
            return self.summarize(chunks[0], max_tokens)
            
        # Summarize each chunk
        chunk_summaries = []
        for i, chunk in enumerate(chunks):
            logger.info(f"Summarizing chunk {i+1}/{len(chunks)}")
            summary = self.summarize(chunk, max_tokens=200)
            chunk_summaries.append(summary)
            
        # Combine chunk summaries into a single coherent summary
        combined_text = "\n\n".join(chunk_summaries)
        final_summary = self.summarize(
            f"These are summaries of different sections of a document. Please create a coherent overall summary:\n\n{combined_text}",
            max_tokens=max_tokens
        )
        
        return final_summary