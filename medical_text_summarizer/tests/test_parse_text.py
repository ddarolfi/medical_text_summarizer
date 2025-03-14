import pytest
from utils.parse_text import prepare, split_into_chunks, find_sentence_boundary

def test_prepare_basic_cleaning():
    """Test basic text cleaning functionality"""
    input_text = "This   is    a    test   with    extra    spaces."
    expected = "This is a test with extra spaces."
    assert prepare(input_text) == expected

def test_prepare_with_max_length():
    """Test text preparation with max length limit"""
    input_text = "This is a long sentence. This is another sentence."
    max_length = 20
    result = prepare(input_text, max_length)
    assert len(result) <= max_length
    assert result.endswith(".")  # Should cut at sentence boundary

def test_prepare_special_characters():
    """Test handling of special characters"""
    input_text = "Test with @#$% special &*() chars [section] = heading"
    expected = "Test with  special  chars [section] = heading"
    assert prepare(input_text) == expected

def test_split_into_chunks_short_text():
    """Test splitting when text is shorter than chunk size"""
    text = "Short text."
    chunk_size = 100
    chunks = split_into_chunks(text, chunk_size)
    assert len(chunks) == 1
    assert chunks[0] == text

def test_split_into_chunks_with_overlap():
    """Test splitting text into chunks with overlap"""
    text = "First sentence. Second sentence. Third sentence. Fourth sentence."
    chunks = split_into_chunks(text, chunk_size=30, overlap=10)
    assert len(chunks) > 1
    # Check for overlap
    assert chunks[0][-10:] in chunks[1]

def test_find_sentence_boundary():
    """Test finding sentence boundaries"""
    text = "First sentence. Second sentence? Third sentence! Fourth sentence."
    # Test finding boundary after period
    assert find_sentence_boundary(text, 10) > text.find("First sentence.")
    # Test finding boundary after question mark
    assert find_sentence_boundary(text, 25) > text.find("Second sentence?")
    # Test finding boundary after exclamation mark
    assert find_sentence_boundary(text, 40) > text.find("Third sentence!")

def test_prepare_preserves_structure():
    """Test that structural elements are preserved"""
    input_text = """=== Section 1 ===
    Content here.
    
    [Important] More content."""
    result = prepare(input_text)
    assert "===" in result
    assert "[Important]" in result

@pytest.mark.parametrize("text,expected", [
    ("Single line.", ["Single line."]),
    ("A. B. C.", ["A. B. C."]),
    ("Very long text that should be split." * 10, None)  # Will check length only
])
def test_split_into_chunks_parametrized(text, expected):
    """Parametrized test for different splitting scenarios"""
    chunks = split_into_chunks(text, chunk_size=100, overlap=10)
    if expected:
        assert chunks == expected
    else:
        assert len(chunks) > 1  # For long text, verify it was split