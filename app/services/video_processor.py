import os
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, concatenate_videoclips

# def create_summary_video(video_path, summary_text, output_path):
#     video = VideoFileClip(video_path)
#     text_clip = TextClip(summary_text, fontsize=24, color='white', bg_color='black')
#     text_clip = text_clip.set_position('center').set_duration(video.duration)
#     final_clip = CompositeVideoClip([video, text_clip])
#     final_clip.write_videofile(output_path, codec='libx264')


def extract_important_clips(video_path, webvtt_captions):
    """
    Extract important parts of the video based on WEBVTT timestamps.
    
    Args:
        video_path (str): Path to the video file.
        webvtt_captions (list): List of tuples containing (start_time, end_time, text).
    
    Returns:
        list: List of VideoFileClip objects representing the important parts of the video.
    """
    video = VideoFileClip(video_path)
    clips = []

    for start_time, end_time, text in webvtt_captions:
        # Convert start_time and end_time to seconds
        start_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(start_time.split(':'))))
        end_seconds = sum(float(x) * 60 ** i for i, x in enumerate(reversed(end_time.split(':'))))
        
        # Extract the clip from the video
        clip = video.subclip(start_seconds, end_seconds)
        clips.append(clip)

    return clips

def create_condensed_video(clips, output_path):
    """
    Create a condensed video by combining important clips.
    
    Args:
        clips (list): List of VideoFileClip objects.
        output_path (str): Path to save the condensed video.
    """
    # Concatenate the clips into a single video
    condensed_video = concatenate_videoclips(clips)
    condensed_video.write_videofile(output_path, codec='libx264')

def create_summary_video(video_path, webvtt_captions, summary_text, output_path):
    """
    Create a summary video by trimming unimportant parts, condensing the video,
    and overlaying the summary text.
    
    Args:
        video_path (str): Path to the original video file.
        transcript_path (str): Path to the WEBVTT transcript file.
        summary_text (str): The summarized text.
        output_path (str): Path to save the summarized video.
    """

    # Extract important parts of the video using WEBVTT timestamps
    important_clips = extract_important_clips(video_path, webvtt_captions)

    #Create a condensed video from the important clips
    condensed_video_path = "condensed_video.mp4"
    create_condensed_video(important_clips, condensed_video_path)

    # Step 4: Load the condensed video
    condensed_video = VideoFileClip(condensed_video_path)

    # Step 5: Create text clip for summary
    text_clip = TextClip(
        summary_text,
        fontsize=24,
        color='white',
        bg_color='black',
        font='Arial',
        size=(condensed_video.size[0], None)  # Match width of the video
    )
    text_clip = text_clip.set_position('center').set_duration(condensed_video.duration)

    #Overlay text on the condensed video
    final_clip = CompositeVideoClip([condensed_video, text_clip])
    final_clip.write_videofile(output_path, codec='libx264')

    #Clean up temporary files
    os.remove(condensed_video_path)