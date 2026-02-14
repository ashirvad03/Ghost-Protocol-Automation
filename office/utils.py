import os
import sys

# --- COMMON FUNCTIONS ---

def clear():
    """Screen ko saaf karne ke liye."""
    os.system('cls' if os.name == 'nt' else 'clear')

def get_path(prompt_text, check_exists=True):
    """
    User se file ya folder ka path maangta hai.
    check_exists=True: Check karega ki path sach me hai ya nahi.
    """
    path = input(f"\n📂 {prompt_text}: ").strip('"')
    if check_exists and not os.path.exists(path):
        print(f"❌ Error: Path nahi mila! ({path})")
        input("Press Enter to continue...")
        return None
    return path

def header(title):
    """Har menu ke upar ek standard header lagayega."""
    clear()
    print("==========================================")
    print(f"      {title.upper()}")
    print("==========================================")