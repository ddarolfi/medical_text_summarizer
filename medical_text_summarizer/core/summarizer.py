from .client import OpenAIClient
from utils import  parse_files, parse_text
import logging

class Summarizer:
    TOKEN_LIMIT = 4000

    def __init__(self, model: str = "gpt-4o-mini"):
        """ Initialize the summarizer with the OpenAI client """
        self.client = OpenAIClient(model)

    def process(self, input_path: str, output_path: str = None):
        """
        Summarize content from files in the input path and save to output path
        """
        content = parse_files.read_and_concatenate(input_path)

        if len(content) == 0:
            logging.warning("No content to summarize")
            return
        
        text = parse_text.prepare(content)
        if len(text) == 0:
            logging.warning("No text to summarize")
            return

        summary = ''
        
        if len(text) > self.TOKEN_LIMIT:
            logging.info("Text exceeds maximum token limit of %d. Splitting text into chunks for summarization." % self.TOKEN_LIMIT)
            chunks = parse_text.split_into_chunks(text)
            summary = self.client.chunk_summarize(chunks)
        else:
            summary = self.client.summarize(text)

        if output_path:
            parse_files.write_output(summary, output_path)
            
        return summary