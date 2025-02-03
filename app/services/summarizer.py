import webvtt
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from transformers import pipeline


try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

def _split_text_into_chunks(text, max_tokens=1000):
    """
    Split the text into chunks of a maximum token length.
    
    Args:
        text (str): The input text.
        max_tokens (int): Maximum number of tokens per chunk.
    
    Returns:
        list: List of text chunks.
    """
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    current_token_count = 0

    for sentence in sentences:
        sentence_tokens = word_tokenize(sentence)
        sentence_token_count = len(sentence_tokens)

        # Check if adding the next sentence exceeds the max token limit
        if current_token_count + sentence_token_count <= max_tokens:
            current_chunk += " " + sentence
            current_token_count += sentence_token_count
        else:
            # If the current chunk is not empty, add it to the chunks list
            if current_chunk.strip():
                chunks.append(current_chunk.strip())
            # Start a new chunk with the current sentence
            current_chunk = sentence
            current_token_count = sentence_token_count

    # Add the last chunk if it's not empty
    if current_chunk.strip():
        chunks.append(current_chunk.strip())

    return chunks

def summarize_transcript(transcript_path, max_length=200):
    """
    Summarize the transcript using a pre-trained NLP model.
    
    Args:
        captions (list): List of tuples containing (start_time, end_time, text).
        max_length (int): Maximum length of the summary.
    
    Returns:
        list: List of tuples containing (start_time, end_time, summarized_text).
    """
    # Initialize the summarization pipeline
    summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

    captions = _parse_webvtt(transcript_path)

    # Extract text from captions and split into chunks
    transcript = " ".join([caption[2] for caption in captions])
    chunks = _split_text_into_chunks(transcript, max_tokens=1000)

    # Summarize each chunk
    summaries = []
    for chunk in chunks:
        try:
            summary = summarizer(chunk, max_length=max_length, min_length=30, do_sample=False)
            summaries.append(summary[0]['summary_text'])
        except Exception as e:
            print(f"Error summarizing chunk: {e}")
            continue

    # Combine the summaries
    final_summary = " ".join(summaries)

    # Filter captions to keep only those that are in the summary
    important_captions = []
    for caption in captions:
        if any(sentence in final_summary for sentence in sent_tokenize(caption[2])):
            important_captions.append(caption)

    return important_captions, final_summary

def _parse_webvtt(webvtt_path):
    """
    Parse a WEBVTT file and extract the text content with timestamps.
    
    Args:
        webvtt_path (str): Path to the WEBVTT file.
    
    Returns:
        list: List of tuples containing (start_time, end_time, text).
    """
    captions = []
    for caption in webvtt.read(webvtt_path):
        captions.append((caption.start, caption.end, caption.text))
    return captions
