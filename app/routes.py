from flask import Blueprint, request, jsonify, send_from_directory
from flask import current_app
import os
import uuid
from werkzeug.utils import secure_filename
from .services.file_manager import save_files, get_file_paths
from .services.summarizer import summarize_transcript
from .services.video_processor import create_summary_video

# Create a Blueprint for the routes
main_bp = Blueprint('main', __name__)

# Configuration for file uploads
UPLOAD_FOLDER = 'uploads'
SUMMARY_FOLDER = 'summaries'
ALLOWED_EXTENSIONS = {'mp4', 'vtt'}

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main_bp.route('/upload', methods=['POST'])
def upload_files():
    """
    API endpoint to upload a video and transcript file.
    """
    if 'video_file' not in request.files or 'transcript_file' not in request.files:
        return jsonify({"error": "Missing video or transcript file"}), 400

    video_file = request.files['video_file']
    transcript_file = request.files['transcript_file']

    # Validate file extensions
    if not allowed_file(video_file.filename) or not allowed_file(transcript_file.filename):
        return jsonify({"error": "Invalid file type. Only .mp4 and .txt files are allowed."}), 400

    # Generate a unique file ID
    file_id = str(uuid.uuid4())

    # Save files
    try:
        video_filename = secure_filename(f"{file_id}_video.mp4")
        transcript_filename = secure_filename(f"{file_id}_transcript.txt")
        video_path = os.path.join(UPLOAD_FOLDER, video_filename)
        transcript_path = os.path.join(UPLOAD_FOLDER, transcript_filename)

        video_file.save(video_path)
        transcript_file.save(transcript_path)

        return jsonify({"file_id": file_id}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to save files: {str(e)}"}), 500

@main_bp.route('/summarize', methods=['POST'])
def summarize_files():
    """
    API endpoint to generate a summary from uploaded files.
    """
    data = request.json
    file_id = data.get('file_id')
    summary_length = data.get('summary_length', 200)  # Default summary length

    if not file_id:
        return jsonify({"error": "Missing file_id"}), 400

    # Locate files
    video_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_video.mp4")
    transcript_path = os.path.join(UPLOAD_FOLDER, f"{file_id}_transcript.txt")

    if not os.path.exists(video_path) or not os.path.exists(transcript_path):
        return jsonify({"error": "Files not found"}), 404

    try:
        # Summarize transcript
        captions, summary_text = summarize_transcript(transcript_path, summary_length)
        print("finish text summarization", summary_text)

        # Create summarized video
        summary_video_path = os.path.join(SUMMARY_FOLDER, f"{file_id}_summary.mp4")
        create_summary_video(video_path, captions, summary_text, summary_video_path)
        print("finish video summarization", summary_video_path)

        # Generate URL for the summarized video
        summary_video_url = f"/summaries/{file_id}_summary.mp4"

        return jsonify({
            "summary_text": summary_text,
            "summary_video_url": summary_video_url
        }), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate summary: {str(e)}"}), 500

@main_bp.route('/summaries/<filename>')
def download_summary(filename):
    """
    API endpoint to download the summarized video.
    """
    try:
        return send_from_directory(SUMMARY_FOLDER, filename)
    except FileNotFoundError:
        return jsonify({"error": "File not found"}), 404
    

@main_bp.route('/config')
def show_config():
    return {
        'upload_folder': current_app.config['UPLOAD_FOLDER'],
        'summary_folder': current_app.config['SUMMARY_FOLDER'],
        'debug_mode': current_app.config['DEBUG'],
    }