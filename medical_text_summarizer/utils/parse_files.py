# utils/parse_files.py
from typing import List, Union
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

def get_files(input_path: Union[str, Path]) -> List[str]:
    """
    Get all text files from a path (file or directory).
    
    Args:
        input_path: Path to a file or directory
        
    Returns:
        List of file paths
    """
    input_path = Path(input_path)
    
    if input_path.is_file():
        return [str(input_path)]
    
    if input_path.is_dir():
        # Find all text files in the directory
        text_files = []
        for file in input_path.glob("**/*.txt"):
            text_files.append(str(file))
        return sorted(text_files)  # Sort for consistent order
    
    raise FileNotFoundError(f"Path not found: {input_path}")

def read_file(file_path: Union[str, Path]) -> str:
    """
    Read content from a text file.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        Content of the file as string
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()

def read_and_concatenate(input_path: Union[str, Path]) -> str:
    """
    Read all text files from input path and concatenate their contents.
    
    Args:
        input_path: Path to file or directory with text files
        
    Returns:
        Concatenated text from all files with headers
    """
    files = get_files(input_path)
    
    if not files:
        logger.warning(f"No text files found at {input_path}")
        return ""
    
    # Concatenate all file contents with headers
    combined_text = ""
    for file_path in files:
        logger.info(f"Reading file: {file_path}")
        text = read_file(file_path)
        file_name = Path(file_path).name
        # Add file name as a header to help with context
        combined_text += f"\n\n=== {file_name} ===\n\n{text}"
    
    return combined_text.strip()

def write_output(content: str, output_path: Union[str, Path]) -> None:
    """
    Write content to output file.
    
    Args:
        content: Text content to write
        output_path: Path to write the content
    """
    output_path = Path(output_path)
    
    # Ensure the directory exists
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    logger.info(f"Content written to {output_path}")