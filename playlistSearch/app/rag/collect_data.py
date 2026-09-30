import sys
from typing import List, Dict, Any
import yt_dlp
from youtube_transcript_api import YouTubeTranscriptApi


def format_timestamp(seconds: float) -> str:
    """
    Converts seconds into HH:MM:SS format.
    """
    total_seconds = int(round(seconds))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def extract_snippet_data(snippet: Any) -> tuple[str, float, float]:
    """
    Safely extracts text, start timestamp, and duration from a transcript snippet,
    supporting both dictionary items and FetchedTranscriptSnippet objects.
    """
    if isinstance(snippet, dict):
        text = snippet.get("text", "")
        start = float(snippet.get("start", 0.0))
        duration = float(snippet.get("duration", 0.0))
    else:
        text = getattr(snippet, "text", "")
        start = float(getattr(snippet, "start", 0.0))
        duration = float(getattr(snippet, "duration", 0.0))
    return text, start, duration


def chunk_transcript(snippets: List[Any], chunk_duration: float = 60.0) -> List[Dict[str, str]]:
    """
    Groups transcript snippets into chunks of roughly `chunk_duration` seconds (default 60s).
    Returns a list of dicts: [{'text': str, 'timestamp': 'HH:MM:SS'}]
    """
    chunks = []
    if not snippets:
        return chunks

    current_texts = []
    current_start = None

    for item in snippets:
        text, start, duration = extract_snippet_data(item)
        cleaned_text = " ".join(text.split())
        if not cleaned_text:
            continue

        if current_start is None:
            current_start = start
            current_texts.append(cleaned_text)
        else:
            # When the time difference from current chunk's start reaches chunk_duration, finalize chunk
            if (start - current_start) >= chunk_duration and current_texts:
                chunks.append({
                    "text": " ".join(current_texts),
                    "timestamp": format_timestamp(current_start)
                })
                current_start = start
                current_texts = [cleaned_text]
            else:
                current_texts.append(cleaned_text)

    # Add the remaining snippets as the last chunk
    if current_texts and current_start is not None:
        chunks.append({
            "text": " ".join(current_texts),
            "timestamp": format_timestamp(current_start)
        })

    return chunks


def fetch_video_transcript(video_id: str) -> List[Any]:
    """
    Fetches transcript snippets for a given video ID using YouTubeTranscriptApi.
    Supports both modern instance-based API (v1.x+) and legacy static methods (v0.6.x).
    Tries English first, then falls back to any available manual or auto-generated transcript.
    """
    # 1. Try instance-based API (youtube-transcript-api >= 1.0)
    try:
        api = YouTubeTranscriptApi()
        if hasattr(api, "fetch"):
            try:
                fetched = api.fetch(video_id)
                if hasattr(fetched, "to_raw_data"):
                    return fetched.to_raw_data()
                return list(fetched)
            except Exception:
                # If default fetch fails, try inspecting available transcripts via list()
                if hasattr(api, "list"):
                    transcript_list = api.list(video_id)
                    try:
                        transcript = transcript_list.find_transcript(["en", "en-US", "en-GB"])
                    except Exception:
                        transcript = next(iter(transcript_list))
                    fetched = transcript.fetch()
                    if hasattr(fetched, "to_raw_data"):
                        return fetched.to_raw_data()
                    return list(fetched)
                raise
    except (TypeError, AttributeError):
        pass

    # 2. Try static methods (youtube-transcript-api < 1.0)
    if hasattr(YouTubeTranscriptApi, "get_transcript"):
        return YouTubeTranscriptApi.get_transcript(video_id)
    elif hasattr(YouTubeTranscriptApi, "list_transcripts"):
        transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)
        try:
            transcript = transcript_list.find_transcript(["en", "en-US", "en-GB"])
        except Exception:
            transcript = next(iter(transcript_list))
        return transcript.fetch()

    raise RuntimeError("No compatible transcript fetching method found in YouTubeTranscriptApi.")


def extract_playlist_info(playlist_url: str) -> Dict[str, Any]:
    """
    Extracts playlist metadata and video entries using yt-dlp flat extraction.
    """
    ydl_opts = {
        "extract_flat": True,
        "skip_download": True,
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(playlist_url, download=False)

    if not info:
        raise ValueError(f"Could not retrieve details for playlist URL: {playlist_url}")

    playlist_name = info.get("title") or "Untitled Playlist"
    raw_entries = info.get("entries") or []

    videos = []
    for entry in raw_entries:
        if not entry:
            continue
        vid_id = entry.get("id")
        if not vid_id and entry.get("url"):
            vid_id = entry.get("url")

        if not vid_id:
            continue

        if not vid_id.startswith("http"):
            vid_url = f"https://www.youtube.com/watch?v={vid_id}"
        else:
            vid_url = entry.get("url") or entry.get("webpage_url") or vid_id

        vid_title = entry.get("title") or f"Video {vid_id}"

        videos.append({
            "id": vid_id,
            "title": vid_title,
            "url": vid_url
        })

    return {
        "title": playlist_name,
        "url": playlist_url,
        "videos": videos
    }


def collect_playlist_transcriptions(
    playlist_url: str,
    chunk_duration: float = 60.0
) -> Dict[str, Any]:
    """
    Iterates over all videos in the playlist, extracts and chunks transcriptions,
    and returns the structured dictionary conforming to the required format.
    """
    print(f"[*] Extracting playlist metadata from: {playlist_url}")
    playlist_info = extract_playlist_info(playlist_url)

    playlist_name = playlist_info["title"]
    videos = playlist_info["videos"]
    print(f"[*] Playlist Title: {playlist_name}")
    print(f"[*] Total videos found: {len(videos)}")

    all_chunks = []

    for idx, video in enumerate(videos, start=1):
        vid_id = video["id"]
        vid_title = video["title"]
        vid_url = video["url"]

        print(f"[{idx}/{len(videos)}] Processing: '{vid_title}' ({vid_id})...")

        try:
            snippets = fetch_video_transcript(vid_id)
            chunks = chunk_transcript(snippets, chunk_duration=chunk_duration)

            for chunk in chunks:
                all_chunks.append({
                    "videourl": vid_url,
                    "videotitle": vid_title,
                    "text": chunk["text"],
                    "timestamp": chunk["timestamp"]
                })
            print(f"    -> Extracted {len(chunks)} chunks.")
        except Exception as e:
            print(f"    [!] Transcript unavailable or failed for '{vid_title}': {e}")
            continue

    return {
        "playlist-name": playlist_name,
        "playlist-url": playlist_url,
        "transcription": all_chunks
    }



def get_transcriptions(playlist_url: str, chunk_duration: float = 60.0) -> Dict[str, Any]:

    if not playlist_url:
        playlist_url = input("Enter YouTube playlist link: ").strip()

    if not playlist_url:
        print("[!] No playlist link provided. Exiting.")
        sys.exit(1)

    result = collect_playlist_transcriptions(
        playlist_url=playlist_url,
        chunk_duration=chunk_duration
    )

    return result