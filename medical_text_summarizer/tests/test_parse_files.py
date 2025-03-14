import pytest
from pathlib import Path
import tempfile
import os
from utils import parse_files

@pytest.fixture
def sample_files():
    """Create temporary test files and directories."""
    with tempfile.TemporaryDirectory() as temp_dir:
        # Create a directory structure
        dir_path = Path(temp_dir)
        
        # Create test files with content
        file1_path = dir_path / "test1.txt"
        file2_path = dir_path / "test2.txt"
        subdir = dir_path / "subdir"
        subdir.mkdir()
        file3_path = subdir / "test3.txt"
        
        # Write content to files
        file1_path.write_text("Content of test1")
        file2_path.write_text("Content of test2")
        file3_path.write_text("Content of test3")
        
        yield {
            'dir_path': dir_path,
            'file1_path': file1_path,
            'file2_path': file2_path,
            'file3_path': file3_path,
            'subdir': subdir
        }

class TestParseFiles:
    def test_get_files_single_file(self, sample_files):
        """Test get_files with a single file path."""
        files = parse_files.get_files(sample_files['file1_path'])
        assert len(files) == 1
        assert str(sample_files['file1_path']) in files

    def test_get_files_directory(self, sample_files):
        """Test get_files with a directory path."""
        files = parse_files.get_files(sample_files['dir_path'])
        assert len(files) == 3
        assert all(f.endswith('.txt') for f in files)
        
    def test_get_files_nonexistent_path(self):
        """Test get_files with a non-existent path."""
        with pytest.raises(FileNotFoundError):
            parse_files.get_files("nonexistent/path")

    def test_read_file(self, sample_files):
        """Test reading content from a single file."""
        content = parse_files.read_file(sample_files['file1_path'])
        assert content == "Content of test1"

    def test_read_file_nonexistent(self):
        """Test reading from a non-existent file."""
        with pytest.raises(FileNotFoundError):
            parse_files.read_file("nonexistent.txt")

    def test_read_and_concatenate_single_file(self, sample_files):
        """Test concatenating content from a single file."""
        content = parse_files.read_and_concatenate(sample_files['file1_path'])
        assert "=== test1.txt ===" in content
        assert "Content of test1" in content

    def test_read_and_concatenate_directory(self, sample_files):
        """Test concatenating content from multiple files in a directory."""
        content = parse_files.read_and_concatenate(sample_files['dir_path'])
        
        # Check that all file contents are present
        assert "Content of test1" in content
        assert "Content of test2" in content
        assert "Content of test3" in content
        
        # Check that headers are present
        assert "=== test1.txt ===" in content
        assert "=== test2.txt ===" in content
        assert "=== test3.txt ===" in content

    def test_read_and_concatenate_empty_directory(self):
        """Test concatenating from an empty directory."""
        with tempfile.TemporaryDirectory() as temp_dir:
            content = parse_files.read_and_concatenate(temp_dir)
            assert content == ""

    def test_write_output(self, tmp_path):
        """Test writing content to a file."""
        output_file = tmp_path / "output.txt"
        test_content = "Test content"
        
        parse_files.write_output(test_content, output_file)
        
        # Verify file was created and content was written
        assert output_file.exists()
        assert output_file.read_text() == test_content

    def test_write_output_nested_directory(self, tmp_path):
        """Test writing output to a nested directory structure."""
        nested_path = tmp_path / "nested" / "dirs" / "output.txt"
        test_content = "Test content"
        
        parse_files.write_output(test_content, nested_path)
        
        # Verify directories were created and file exists
        assert nested_path.exists()
        assert nested_path.read_text() == test_content