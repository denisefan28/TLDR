import os
import uuid
from werkzeug.utils import secure_filename

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
SUMMARY_FOLDER = 'summaries'

def save_files(video_file, transcript_file):
    """
    Save uploaded video and transcript files to the uploads folder.
    
    Args:
        video_file: Uploaded video file.
        transcript_file: Uploaded transcript file.
    
    Returns:
        file_id (str): Unique ID for the uploaded files.
        video_path (str): Path to the saved video file.
        transcript_path (str): Path to the saved transcript file.
    """
    # Generate a unique file ID
    file_id = str(uuid.uuid4())

    # Save video file
    video_filename = secure_filename(f"{file_id}_video.mp4")
    video_path = os.path.join(UPLOAD_FOLDER, video_filename)
    video_file.save(video_path)

    # Save transcript file
    transcript_filename = secure_filename(f"{file_id}_transcript.txt")
    transcript_path = os.path.join(UPLOAD_FOLDER, transcript_filename)
    transcript_file.save(transcript_path)

    return file_id, video_path, transcript_path

def get_file_paths(file_id):
    """
    Retrieve the paths of the uploaded video and transcript files using the file ID.
    
    Args:
        file_id (str): Unique ID of the uploaded files.
    
    Returns:
        video_path (str): Path to the video file.
        transcript_path (str): Path to the transcript file.
    """
    video_filename = f"{file_id}_video.mp4"
    transcript_filename = f"{file_id}_transcript.txt"

    video_path = os.path.join(UPLOAD_FOLDER, video_filename)
    transcript_path = os.path.join(UPLOAD_FOLDER, transcript_filename)

    return video_path, transcript_path

def ensure_folders_exist():
    """
    Ensure that the uploads and summaries folders exist.
    If they don't, create them.
    """
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(SUMMARY_FOLDER, exist_ok=True)