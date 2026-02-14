import os
import sys
import yt_dlp

DOWNLOAD_DIR = os.path.join(os.path.expanduser('~'), 'Downloads')

# --- SETUP ---
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def header(text):
    clear()
    print("\033[1;31m") # YouTube Red Color
    print("=" * 50)
    print(f"   📺  YOUTUBE COMMAND CENTER - {text}")
    print("=" * 50)
    print("\033[0m") # Reset Color

def get_url():
    print("\n🔗 Paste YouTube Link (Right Click to Paste):")
    url = input(" >> ").strip()
    return url

# ==========================================
# ⚙️ CORE FUNCTIONS
# ==========================================

def download_video_best():
    header("BEST QUALITY VIDEO (1080p/4K)")
    url = get_url()
    if not url: return

    save_path = os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')

    # Options: Best Video + Best Audio merged
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': save_path, # File name = Video Title
        'merge_output_format': 'mp4',
    }
    
    print(f"\n⏳ Downloading to: {DOWNLOAD_DIR}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Download Complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    input("\nPress Enter...")

def download_audio_only():
    header("AUDIO EXTRACTOR (MP3 Studio)")
    url = get_url()
    if not url: return

    save_path = os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')

    # Options: Convert to MP3, Best Quality (192k+)
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': save_path,
    }
    
    print(f"\n🎵 Extracting to: {DOWNLOAD_DIR}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Saved as MP3!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    input("\nPress Enter...")

def download_playlist():
    header("BULK PLAYLIST DOWNLOADER")
    print("⚠️ Warning: Poori Playlist download hogi.")
    url = get_url()
    if not url: return

    print("\n[1] Video Playlist")
    print("[2] Audio Only Playlist")
    choice = input("Select Type: ")

    playlist_dir = os.path.join(DOWNLOAD_DIR, 'YT_Playlist_Downloads')
    if not os.path.exists(playlist_dir):
        os.makedirs(playlist_dir)

    save_path = os.path.join(playlist_dir, '%(playlist_index)s - %(title)s.%(ext)s')

    ydl_opts = {
        'outtmpl': save_path, # Numbering 01, 02...
        'ignoreerrors': True, # Agar ek video fail ho to ruke nahi
    }

    if choice == '2':
        ydl_opts['format'] = 'bestaudio/best'
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    else:
        ydl_opts['format'] = 'bestvideo+bestaudio/best'
        ydl_opts['merge_output_format'] = 'mp4'

    print(f"\n🚀 Downloading Playlist to: {playlist_dir}...")
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n✅ Playlist Complete!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    input("\nPress Enter...")

def get_thumbnail_info():
    header("SPY MODE (Info & Thumbnail)")
    url = get_url()
    if not url: return

    save_path = os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s')

    ydl_opts = {
        'writethumbnail': True,
        'skip_download': True, # Video download mat karo
        'outtmpl': save_path,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            print("\n" + "!"*40)
            print(f" [!] Title      : {info.get('title')}")
            print(f" [!] Channel    : {info.get('uploader')}")
            print(f" [!] Uploaded   : {info.get('upload_date')}")
            print(f" [!] View Count : {info.get('view_count')}")
            print(f" [!] Duration   : {info.get('duration')} seconds")
            
            # Hidden Tags extraction
            tags = info.get('tags')
            if tags:
                print(f" [!] Hidden Tags: {', '.join(tags[:10])}...") # Top 10 tags
            
            print("!"*40)
            print(f"\n✅ High-Res Thumbnail saved in: {DOWNLOAD_DIR}")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    input("\nPress Enter...")

# ==========================================
# 📋 MAIN MENU
# ==========================================

while True:
    header("MAIN DASHBOARD")
    print(" [1] 🎥 Download High Quality Video (MP4)")
    print(" [2] 🎵 Download Audio Only (MP3)")
    print(" [3] 📦 Download Whole Playlist (Bulk)")
    print(" [4] 🕵️ Get Video Info & Thumbnail")
    print(" [0] 🔙 Back to Launcher")
    print("=" * 50)

    c = input("\nSelect Action (0-4): ")

    if c == '1': download_video_best()
    elif c == '2': download_audio_only()
    elif c == '3': download_playlist()
    elif c == '4': get_thumbnail_info()
    elif c == '0': break