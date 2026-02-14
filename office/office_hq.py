import sys
import os
from utils import clear, header

# --- IMPORT SUB-MENUS ---
# Hum sub-folders se unke menu scripts ko import karenge
sys.path.append(os.path.join(os.path.dirname(__file__), 'file_tools'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'image_tools'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'video_tools'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'audio_tools'))

try:
    import file_menu
    import image_menu
    import video_menu
    import audio_menu
except ImportError as e:
    print(f"Error importing sub-menus: {e}")
    print("Make sure you have created all the __init__.py files in subfolders.")
    input("Press Enter to exit...")
    sys.exit()

# --- MAIN OFFICE MENU ---
while True:
    header("🏢 THE OFFICE HQ 🏢")
    print("  Choose Your Department:")
    print("==========================================")
    print(" [1] 📁 FILE Tools  (PDF, Word, Excel, etc.)")
    print(" [2] 🖼️ IMAGE Tools (Resize, Edit, Convert)")
    print(" [3] 🎥 VIDEO Tools (Compress, Trim, Convert)")
    print(" [4] 🎵 AUDIO Tools (Convert, Compress)")
    print("------------------------------------------")
    print(" [5] Exit to Main Launcher")
    print("==========================================")
    
    opt = input("\nSelect Option (1-5): ")
    
    if opt == '1':
        file_menu.run_menu()
    elif opt == '2':
        image_menu.run_menu()
    elif opt == '3':
        video_menu.run_menu()
    elif opt == '4':
        audio_menu.run_menu()
    elif opt == '5':
        break # Loop todega aur script band hogi, wapas joker.bat me jayega