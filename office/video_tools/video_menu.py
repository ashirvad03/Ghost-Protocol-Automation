import os
import sys
import subprocess

# --- UTILS IMPORT SETUP ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clear, header, get_path

# ==========================================
# 🧠 HELPER FUNCTIONS
# ==========================================

def run_ffmpeg(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError:
        print("\n❌ Error: FFmpeg command fail ho gayi.")
        return False

# ==========================================
# 🎥 VIDEO ACTIONS
# ==========================================

def convert_video(input_path):
    print("\n🔄 Convert Video Format")
    print("Formats: mp4, mkv, avi, mov, gif")
    fmt = input("Target Format (e.g. mkv): ").lower()
    
    out_path = input_path.rsplit('.', 1)[0] + f".{fmt}"
    print(f"Converting to {fmt}...")
    
    # Basic conversion
    cmd = f'ffmpeg -i "{input_path}" -c:v libx264 -preset fast -c:a aac "{out_path}"'
    
    # GIF ke liye special command
    if fmt == 'gif':
        print("Creating GIF (Might take time)...")
        # fps=10, scale=480 (Width) - taaki size chota rahe
        cmd = f'ffmpeg -i "{input_path}" -vf "fps=10,scale=480:-1:flags=lanczos" "{out_path}"'
        
    if run_ffmpeg(cmd):
        print(f"✅ Converted: {out_path}")

def compress_video(input_path):
    print("\n🗜️ Smart Video Compress")
    print("CRF Value: 18 (Lossless) to 35 (Low Quality). Default is 28.")
    crf = input("Enter Compression Level (23-30 recommended): ") or "28"
    
    out_path = input_path.rsplit('.', 1)[0] + "_compressed.mp4"
    print("Compressing... (Wait, this uses CPU power)")
    
    # libx264 compression
    cmd = f'ffmpeg -i "{input_path}" -vcodec libx264 -crf {crf} "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Compressed: {out_path}")

def trim_video(input_path):
    print("\n✂️ Trim Video")
    start = input("Start Time (00:00:10): ")
    end = input("End Time   (00:00:20): ")
    
    out_path = input_path.rsplit('.', 1)[0] + "_trimmed.mp4"
    
    # Fast trim (No re-encoding)
    cmd = f'ffmpeg -i "{input_path}" -ss {start} -to {end} -c copy "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Trimmed: {out_path}")

def resize_video(input_path):
    print("\n📐 Resize Video (Scale)")
    width = input("Target Width (e.g. 1280, 1920): ")
    
    out_path = input_path.rsplit('.', 1)[0] + f"_resized_{width}p.mp4"
    
    # Scale width, height auto-calculate (-1)
    cmd = f'ffmpeg -i "{input_path}" -vf scale={width}:-1 "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Resized: {out_path}")

def remove_audio(input_path):
    print("\n🔇 Mute Video (Remove Audio)")
    out_path = input_path.rsplit('.', 1)[0] + "_muted.mp4"
    
    # -an means "Audio No"
    cmd = f'ffmpeg -i "{input_path}" -c copy -an "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Audio Removed: {out_path}")

def rotate_video(input_path):
    print("\n🔄 Rotate Video")
    print("1 = 90Clockwise, 2 = 90CounterClockwise")
    choice = input("Select: ")
    
    transpose = "transpose=1" if choice == '1' else "transpose=2"
    out_path = input_path.rsplit('.', 1)[0] + "_rotated.mp4"
    
    # Re-encoding required for rotation
    cmd = f'ffmpeg -i "{input_path}" -vf "{transpose}" -c:a copy "{out_path}"'
    
    if run_ffmpeg(cmd):
        print(f"✅ Rotated: {out_path}")

def change_speed(input_path):
    print("\n⏩ Change Speed (Slo-Mo / Fast)")
    print("0.5 = Slow (2x), 2.0 = Fast (2x)")
    pts = input("Speed Factor (e.g. 2.0): ")
    
    out_path = input_path.rsplit('.', 1)[0] + f"_speed_{pts}x.mp4"
    
    # Video PTS modify + Audio Tempo modify
    # Note: 1/pts logic for video
    try:
        val = float(pts)
        setpts = 1 / val
        cmd = f'ffmpeg -i "{input_path}" -filter_complex "[0:v]setpts={setpts}*PTS[v];[0:a]atempo={val}[a]" -map "[v]" -map "[a]" "{out_path}"'
        
        if run_ffmpeg(cmd):
            print(f"✅ Speed Changed: {out_path}")
    except:
        print("❌ Invalid Number")

# ==========================================
# 📋 MAIN MENU
# ==========================================

def run_menu():
    while True:
        header("🎥 VIDEO TOOLS - THE OFFICE HQ")
        print("==========================================")
        
        print(" 🔄 CONVERT:")
        print(" [1] Convert Format   (MP4/MKV/AVI/GIF)")
        print(" [2] Video to Audio   (Extract MP3)")
        print("------------------------------------------")
        
        print(" 🚀 OPTIMIZE:")
        print(" [3] Compress Video   (Reduce Size)")
        print(" [4] Mute Video       (Remove Audio)")
        print("------------------------------------------")
        
        print(" 🛠️ MODIFY:")
        print(" [5] Trim/Cut Video   (Start - End)")
        print(" [6] Resize Video     (Change Resolution)")
        print(" [7] Rotate Video     (90 Degrees)")
        print(" [8] Change Speed     (Fast/Slow)")
        print("------------------------------------------")
        
        print(" [0] Back")
        print("==========================================")
        
        c = input("\nSelect Option (0-8): ")
        if c == '0': break

        # --- ACTIONS ---
        if c == '1':
            path = get_path("Video Path")
            if path: convert_video(path)
            
        elif c == '2':
            # Audio Menu wala function use kar sakte hain ya direct command
            path = get_path("Video Path")
            if path:
                out = path.rsplit('.', 1)[0] + ".mp3"
                run_ffmpeg(f'ffmpeg -i "{path}" -vn -q:a 0 -map a "{out}"')
                print(f"✅ Audio Extracted: {out}")

        elif c == '3':
            path = get_path("Video Path")
            if path: compress_video(path)

        elif c == '4':
            path = get_path("Video Path")
            if path: remove_audio(path)

        elif c == '5':
            path = get_path("Video Path")
            if path: trim_video(path)
            
        elif c == '6':
            path = get_path("Video Path")
            if path: resize_video(path)
            
        elif c == '7':
            path = get_path("Video Path")
            if path: rotate_video(path)

        elif c == '8':
            path = get_path("Video Path")
            if path: change_speed(path)

        if c != '0':
            input("\nPress Enter to continue...")