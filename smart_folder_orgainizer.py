import os
import shutil

# Screen saaf karne ke liye
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Colors
G = "\033[92m" # Green
Y = "\033[93m" # Yellow
R = "\033[91m" # Red
W = "\033[97m" # White

def organize_folder():
    clear_screen()
    print(f"{Y}========================================")
    print(f"      SMART FOLDER ORGANIZER 🧹")
    print(f"========================================{W}")
    
    print("Kis folder ko organize karna hai?")
    print("1. Current Folder (Jahan ye script hai)")
    print("2. Downloads Folder (Automatic Detect)")
    print("3. Custom Path (Manually paste karo)")
    
    choice = input(f"\n{Y}Option: {W}")
    
    folder_path = ""
    
    if choice == '1':
        folder_path = os.getcwd()
    elif choice == '2':
        # User ka Downloads folder automatic dhund raha hu
        folder_path = os.path.join(os.path.expanduser("~"), "Downloads")
    elif choice == '3':
        folder_path = input("Path paste karein: ")
    else:
        return

    # Check agar folder exist karta hai
    if not os.path.exists(folder_path):
        print(f"\n{R}Error: Folder nahi mila!{W}")
        input("Enter dabayein...")
        return

    print(f"\n{G}Scanning: {folder_path}{W}")
    
    # Extensions ki Dictionary (Rules)
    file_types = {
        "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
        "Videos": [".mp4", ".mkv", ".mov", ".avi", ".webm"],
        "Music": [".mp3", ".wav", ".aac", ".flac"],
        "Documents": [".pdf", ".docx", ".txt", ".xlsx", ".pptx", ".doc"],
        "Softwares": [".exe", ".msi", ".bat", ".apk", ".iso"],
        "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"]
    }
    
    moved_count = 0
    
    # Saari files ki list lo
    all_files = os.listdir(folder_path)
    
    for file in all_files:
        # File ka extension nikalo (name aur .jpg alag karo)
        filename, extension = os.path.splitext(file)
        extension = extension.lower() # Chota bada letter same samjho
        
        # Folder ko khud apne aap ko move nahi karna
        if file == "cleaner.py" or file == "Launcher.bat":
            continue
            
        # Check karo file kis category ki hai
        found_category = False
        for category, extensions_list in file_types.items():
            if extension in extensions_list:
                # Target folder ka path (e.g., Downloads/Images)
                target_folder = os.path.join(folder_path, category)
                
                # Agar folder nahi hai to banao
                if not os.path.exists(target_folder):
                    os.makedirs(target_folder)
                
                # File Move karo
                src = os.path.join(folder_path, file)
                dst = os.path.join(target_folder, file)
                
                try:
                    shutil.move(src, dst)
                    print(f"{G}Moved: {file} -> {category}{W}")
                    moved_count += 1
                    found_category = True
                    break # Ek baar move ho gaya to loop roko
                except:
                    print(f"{R}Error moving {file}{W}")

    print(f"\n{Y}----------------------------------------")
    print(f"COMPLETE! Total {moved_count} files organized.")
    print(f"----------------------------------------{W}")
    input("\nMenu par wapas jane ke liye Enter dabayein...")

if __name__ == "__main__":
    organize_folder()