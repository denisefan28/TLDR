import os
import pytest
from app.services.file_manager import save_files, get_file_paths, ensure_folders_exist

def test_save_files():
    # Mock file objects
    class MockFile:
        def __init__(self, filename, content):
            self.filename = filename
            self.content = content

        def save(self, path):
            with open(path, 'w') as f:
                f.write(self.content)

    video_file = MockFile("test_video.mp4", "video content")
    transcript_file = MockFile("test_transcript.txt", "transcript content")

    # Save files
    file_id, video_path, transcript_path = save_files(video_file, transcript_file)

    # Check if files exist
    assert os.path.exists(video_path)
    assert os.path.exists(transcript_path)

    # Clean up
    os.remove(video_path)
    os.remove(transcript_path)

def test_get_file_paths():
    file_id = "test_id"
    video_path, transcript_path = get_file_paths(file_id)

    assert video_path == os.path.join('uploads', f"{file_id}_video.mp4")
    assert transcript_path == os.path.join('uploads', f"{file_id}_transcript.txt")

def test_ensure_folders_exist():
    ensure_folders_exist()
    assert os.path.exists('uploads')
    assert os.path.exists('summaries')