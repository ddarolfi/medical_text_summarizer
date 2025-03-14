# utils/text_processor.py
import re
from typing import List, Optional

def prepare(text: str, max_length: Optional[int] = None) -> str:
    """
    Prepare text for summarization by cleaning and trimming.
    
    Args:
        text: Input text to prepare
        max_length: Optional maximum length to trim to
        
    Returns:
        Cleaned and possibly trimmed text
    """
    # Remove extra whitespace but preserve line breaks for structure
    text = re.sub(r' +', ' ', text)
    text = re.sub(r'\n\s*\n+', '\n\n', text)  # Standardize paragraph breaks
    
    # Preserve structure markers (like === filename.txt ===)
    # but remove other potentially problematic characters
    # Allow = and [] characters which are often used for section marking
    text = re.sub(r'[^\w\s.,;:!?()\-=\[\]]', '', text)
    
    # Trim to max_length if specified
    if max_length and len(text) > max_length:
        text = text[:max_length]
        # Try to cut at the end of a sentence
        last_period = text.rfind('.')
        if last_period > max_length * 0.8:  # Only if the period is reasonably close to the end
            text = text[:last_period + 1]
    
    return text.strip()

def split_into_chunks(text: str, chunk_size: int = 4000, overlap: int = 200) -> List[str]:
    """
    Split text into overlapping chunks of specified size.
    
    Args:
        text: Text to split
        chunk_size: Maximum size of each chunk
        overlap: Number of characters to overlap between chunks
        
    Returns:
        List of text chunks
    """
    # If text is shorter than chunk_size, return as is
    if len(text) <= chunk_size:
        return [text]
    
    chunks = []
    start = 0
    
    while start < len(text):
        # Get chunk of size chunk_size
        end = start + chunk_size
        
        if end >= len(text):
            chunks.append(text[start:])
            break
        
        # Try to find a good breaking point (end of sentence)
        cut_point = find_sentence_boundary(text, end)
        
        chunks.append(text[start:cut_point])
        
        # Next chunk starts with some overlap
        start = cut_point - overlap
        
        # Ensure we're not going backwards
        if start < 0 or start >= len(text) - 1:
            break
    
    return chunks

def find_sentence_boundary(text: str, position: int) -> int:
    """
    Find the nearest sentence boundary after the given position.
    
    Args:
        text: The text to search in
        position: Position to start searching from
        
    Returns:
        Position of the nearest sentence boundary
    """
    # Look for end of sentence within 500 characters after position
    search_limit = min(position + 500, len(text))
    
    # Search for period, question mark, or exclamation mark followed by space or newline
    for pattern in ['. ', '? ', '! ', '.\n', '?\n', '!\n']:
        next_boundary = text.find(pattern, position, search_limit)
        if next_boundary != -1:
            return next_boundary + len(pattern)
    
    # If no sentence boundary found, use the position
    return position