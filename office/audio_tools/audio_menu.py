import os
import sys
import subprocess

# --- UTILS IMPORT SETUP ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clear, header, get_path

# ==========================================
# 🧠 HELPER FUNCTIONS (FFmpeg Engine)
# ==========================================

def run_ffmpeg(cmd):
    """FFmpeg command run karta hai aur error handle karta hai"""
    try:
        # shell=True zaruri hai taaki Windows command ko samajh sake
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Error: Process fail ho gaya.")
        print("Tip: Check karo file sahi hai ya nahi.")
        return False

def get_audio_duration(file_path):
    """Audio ki length pata lagane ke liye (Optional logic)"""
    # Filhal hum user se manual input lenge trim ke liye
    pass

# ==========================================
# 🎵 AUDIO ACTIONS
# ==========================================

def convert_format(input_path):
    print("\n🔄 Convert Audio Format")
    print("Available: mp3, wav, m4a, flac, ogg")
    fmt = input("Target Format (e.g. mp3): ").lower()
    
    out_path = input_path.rsplit('.', 1)[0] + f".{fmt}"
    
    print(f"Converting to {fmt}...")
    # FFmpeg command: -i input -y (overwrite) output
    cmd = f'ffmpeg -i "{input_path}" -y "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Converted: {out_path}")

def compress_audio(input_path):
    print("\n🗜️ Compress Audio (Bitrate)")
    print("Standard Bitrates: 320k (High), 192k (Good), 128k (Radio), 64k (Small)")
    bitrate = input("Enter Bitrate (e.g. 128k): ")
    
    out_path = input_path.rsplit('.', 1)[0] + f"_{bitrate}.mp3"
    
    print(f"Compressing to {bitrate}...")
    # -b:a sets audio bitrate
    cmd = f'ffmpeg -i "{input_path}" -b:a {bitrate} "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Compressed: {out_path}")

def trim_audio(input_path):
    print("\n✂️ Trim/Cut Audio")
    print("Format: HH:MM:SS (Example: 00:00:30 for 30 seconds)")
    
    start = input("Start Time (00:00:00): ")
    end = input("End Time   (00:01:00): ")
    
    out_path = input_path.rsplit('.', 1)[0] + "_trimmed.mp3"
    
    # -ss (Start) -to (End) -c copy (Fast cut without re-encoding)
    cmd = f'ffmpeg -i "{input_path}" -ss {start} -to {end} -c copy "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Trimmed File: {out_path}")

def change_volume(input_path):
    print("\n🔊 Volume Booster")
    print("1.0 = Original, 0.5 = Half, 2.0 = Double volume")
    vol = input("Volume Multiplier (e.g. 2.0): ")
    
    out_path = input_path.rsplit('.', 1)[0] + "_boosted.mp3"
    
    # filter: volume=2.0
    cmd = f'ffmpeg -i "{input_path}" -filter:a "volume={vol}" "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Volume Changed!")

def change_speed(input_path):
    print("\n⏩ Change Speed (Tempo)")
    print("0.5 = Slow Motion, 1.0 = Normal, 1.5 = Fast, 2.0 = Double Speed")
    speed = input("Speed Factor (e.g. 1.5): ")
    
    out_path = input_path.rsplit('.', 1)[0] + f"_speed_{speed}.mp3"
    
    # atempo filter (0.5 se 2.0 tak support karta hai ek baar me)
    cmd = f'ffmpeg -i "{input_path}" -filter:a "atempo={speed}" "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Speed Changed!")

def merge_audios(folder_path):
    print("\n🔗 Merge Multiple Audio Files")
    # Folder se sari audio files uthayenge
    files = [f for f in os.listdir(folder_path) if f.endswith(('.mp3', '.wav', '.m4a'))]
    files.sort()
    
    if len(files) < 2:
        print("❌ Need at least 2 audio files to merge.")
        return

    print(f"Found {len(files)} files. Creating list...")
    
    # FFmpeg ko merge karne ke liye ek text list chahiye hoti hai
    list_file = os.path.join(folder_path, "files_to_merge.txt")
    with open(list_file, "w", encoding="utf-8") as f:
        for file_name in files:
            # Format: file 'song1.mp3'
            f.write(f"file '{file_name}'\n")
            
    out_path = os.path.join(folder_path, "Merged_Audio.mp3")
    
    print("Merging... (This might take time)")
    # concat demuxer use karenge (Fastest method)
    cmd = f'ffmpeg -f concat -safe 0 -i "{list_file}" -c copy "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Merged Successfully: {out_path}")
        os.remove(list_file) # Clean up temp file

def video_to_audio(video_path):
    print("\n🎥 Extract Audio from Video")
    out_path = video_path.rsplit('.', 1)[0] + ".mp3"
    
    # -vn means "No Video", -q:a 0 means "Best Audio Quality"
    cmd = f'ffmpeg -i "{video_path}" -vn -q:a 0 -map a "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Audio Extracted: {out_path}")

# ==========================================
# 📋 MAIN MENU
# ==========================================

def run_menu():
    while True:
        header("🎵 AUDIO TOOLS - THE OFFICE HQ")
        print("==========================================")
        
        print(" 🔄 CONVERT & OPTIMIZE:")
        print(" [1] Convert Format   (mp3/wav/m4a/flac)")
        print(" [2] Compress Audio   (Change Bitrate)")
        print("------------------------------------------")
        
        print(" 🛠️ MODIFY:")
        print(" [3] Trim/Cut Audio   (Start & End time)")
        print(" [4] Volume Booster   (Increase sound)")
        print(" [5] Change Speed     (Fast/Slow)")
        print("------------------------------------------")
        
        print(" 🔗 ORGANIZE:")
        print(" [6] Merge Audios     (Join folder files)")
        print("------------------------------------------")
        
        print(" ⚡ SPECIAL:")
        print(" [7] Video to Audio   (Extract MP3)")
        print("------------------------------------------")
        
        print(" [0] Back")
        print("==========================================")
        
        c = input("\nSelect Option (0-7): ")
        if c == '0': break

        # --- ACTIONS ---
        if c == '1':
            path = get_path("Audio File Path")
            if path: convert_format(path)
            
        elif c == '2':
            path = get_path("Audio File Path")
            if path: compress_audio(path)
            
        elif c == '3':
            path = get_path("Audio File Path")
            if path: trim_audio(path)
            
        elif c == '4':
            path = get_path("Audio File Path")
            if path: change_volume(path)
            
        elif c == '5':
            path = get_path("Audio File Path")
            if path: change_speed(path)
            
        elif c == '6':
            path = get_path("Folder with Audio files")
            if path: merge_audios(path)
            
        elif c == '7':
            path = get_path("Video File Path")
            if path: video_to_audio(path)

        if c != '0':
            input("\nPress Enter to continue...")