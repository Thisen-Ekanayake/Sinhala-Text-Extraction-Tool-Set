import os
import re
import json
from googleapiclient.discovery import build
from dotenv import load_dotenv
from tkinter import Tk, filedialog

# === Load API Key from .env ===
load_dotenv()
API_KEY = os.getenv("YOUTUBE_API_KEY")

# === Sinhala Cleaner ===
def clean_sinhala_text(text):
    cleaned = re.sub(r'[^ \u0D80-\u0DFF\.\,\!\(\)]', '', text)
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned

def get_word_count(text):
    return len(text.split())

# === YouTube Helper Functions ===
def get_channel_id(youtube, url):
    if "/channel/" in url:
        return url.split("/channel/")[1].split("/")[0]
    elif "/user/" in url:
        username = url.split("/user/")[1].split("/")[0]
        res = youtube.channels().list(forUsername=username, part="id").execute()
        return res["items"][0]["id"]
    elif "/@" in url:
        custom_url = url.split("/@")[1].split("/")[0]
        res = youtube.search().list(q=custom_url, part="snippet", type="channel").execute()
        return res["items"][0]["snippet"]["channelId"]
    else:
        raise ValueError("Invalid channel URL format")

def get_uploads_playlist_id(youtube, channel_id):
    res = youtube.channels().list(part="contentDetails", id=channel_id).execute()
    return res["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

def get_video_ids_from_playlist(youtube, uploads_playlist_id, limit=100):
    video_ids = []
    next_page_token = None
    while len(video_ids) < limit:
        res = youtube.playlistItems().list(
            part="snippet",
            playlistId=uploads_playlist_id,
            maxResults=50,
            pageToken=next_page_token
        ).execute()

        for item in res["items"]:
            video_ids.append(item["snippet"]["resourceId"]["videoId"])
            if len(video_ids) >= limit:
                break

        next_page_token = res.get("nextPageToken")
        if not next_page_token:
            break
    return video_ids

def get_comments(youtube, video_id, max_comments=100):
    comments = []
    next_page_token = None
    while len(comments) < max_comments:
        res = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,
            textFormat="plainText",
            pageToken=next_page_token
        ).execute()

        for item in res["items"]:
            top_comment = item["snippet"]["topLevelComment"]["snippet"]
            author = top_comment.get("authorDisplayName", "unknown")
            text = top_comment.get("textDisplay", "")
            comments.append(f"@{author}: {text}")
            if len(comments) >= max_comments:
                break

        next_page_token = res.get("nextPageToken")
        if not next_page_token:
            break
    return comments

# === Main Processing Function ===
def process_channel(youtube, url, index):
    try:
        channel_id = get_channel_id(youtube, url)
    except Exception as e:
        print(f"[!] Skipping invalid URL: {url}\n    ↳ Error: {e}")
        return

    uploads_playlist_id = get_uploads_playlist_id(youtube, channel_id)
    video_ids = get_video_ids_from_playlist(youtube, uploads_playlist_id, limit=100)

    print(f"[{index:02d}] Extracting from channel: {url} → {len(video_ids)} videos")

    all_comments = []
    for vid in video_ids:
        comments = get_comments(youtube, vid, max_comments=100)
        all_comments.extend(comments)

    # Clean
    cleaned_comments = [clean_sinhala_text(c) for c in all_comments if clean_sinhala_text(c)]
    cleaned_text = "\n".join(cleaned_comments)
    word_count = get_word_count(cleaned_text)

    # Save
    txt_filename = f"{index:02d}_txt_word_count_{word_count}.txt"
    json_filename = f"{index:02d}_json_word_count_{word_count}.json"

    with open(txt_filename, "w", encoding="utf-8") as f:
        f.write(cleaned_text)

    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(cleaned_comments, f, ensure_ascii=False, indent=2)

    print(f"    ↳ Saved: {txt_filename}, {json_filename}")

# === Entry Point ===
def main():
    # File picker for channel list
    Tk().withdraw()
    file_path = filedialog.askopenfilename(title="Select .txt file with channel links",
                                           filetypes=[("Text files", "*.txt")])
    if not file_path:
        print("No file selected.")
        return

    with open(file_path, 'r', encoding='utf-8') as f:
        channel_urls = [line.strip() for line in f if line.strip()]

    youtube = build("youtube", "v3", developerKey=API_KEY)

    for idx, url in enumerate(channel_urls, start=1):
        process_channel(youtube, url, idx)

if __name__ == "__main__":
    main()
