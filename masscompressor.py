import os
import zipfile
import shutil
import time
import sys

def print_status(msg, type="INFO"):
    """
    Console logs without emojis.
    Styles: [INFO], [OK], [ERR], [WARN], [?]
    """
    if type == "INFO":
        print(f"[#] {msg}")
    elif type == "OK":
        print(f"[+] {msg}")
    elif type == "ERR":
        print(f"[!] {msg}")
    elif type == "WARN":
        print(f"[-] {msg}")
    elif type == "ASK":
        print(f"[?] {msg}")
    else:
        print(msg)

def get_dir_size(path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            if not os.path.islink(fp):
                total_size += os.path.getsize(fp)
    return total_size

def get_free_space(path):
    total, used, free = shutil.disk_usage(path)
    return free

def get_user_permission(prompt_text):
    """
    User se permission lene ka function.
    Returns True if 'y', False if 'n'
    """
    while True:
        choice = input(f">>> {prompt_text} (y/n): ").strip().lower()
        if choice == 'y':
            return True
        elif choice == 'n':
            return False
        else:
            print("    [!] Invalid input. Type 'y' or 'n'.")

# --- MODULE 1: CLEANUP (Corrupt Zips) ---
def cleanup_module(target_dir):
    print_status("SYSTEM CHECK: Scanning for incomplete/corrupt archives...", "INFO")
    files = [f for f in os.listdir(target_dir) if f.endswith('.zip')]
    
    if not files:
        print_status("No existing ZIP archives found.", "OK")
        return

    for filename in files:
        file_path = os.path.join(target_dir, filename)
        is_corrupt = False
        
        try:
            with zipfile.ZipFile(file_path, 'r') as zipf:
                if zipf.testzip() is not None:
                    is_corrupt = True
        except:
            is_corrupt = True

        if is_corrupt:
            print_status(f"DETECTED CORRUPT FILE: {filename}", "ERR")
            # --- PERMISSION BLOCK ---
            if get_user_permission("Permission to DELETE this corrupt file to free space?"):
                try:
                    os.remove(file_path)
                    print_status(f"File Deleted: {filename}", "OK")
                except Exception as e:
                    print_status(f"Deletion Failed: {e}", "ERR")
            else:
                print_status("Skipped deletion. Corrupt file remains.", "WARN")
            # ------------------------
    
    print("-" * 50)

# --- MODULE 2: COMPRESSION (Main Logic) ---
def compression_module(target_dir):
    print_status("INITIATING COMPRESSION SEQUENCE...", "INFO")
    
    # 1. Analyze Folders
    all_items = os.listdir(target_dir)
    folders = []
    
    print_status("Analyzing directory sizes...", "INFO")
    
    for item in all_items:
        full_path = os.path.join(target_dir, item)
        if os.path.isdir(full_path):
            size = get_dir_size(full_path)
            folders.append((item, size, full_path))

    # Sort: Smallest first
    folders.sort(key=lambda x: x[1])
    
    print_status(f"Queue Loaded: {len(folders)} directories.", "OK")
    print("-" * 50)

    for name, size_bytes, path in folders:
        zip_filename = os.path.join(target_dir, f"{name}.zip")
        size_mb = round(size_bytes / (1024 * 1024), 2)

        # Skip if zip exists
        if os.path.exists(zip_filename):
            print_status(f"Skipping {name} (Archive already exists)", "WARN")
            continue

        free_space = get_free_space(target_dir)
        
        # Space Warning
        if free_space < size_bytes:
            print_status(f"LOW DISK SPACE WARNING for {name}", "WARN")
            print_status(f"Needed: {size_mb} MB | Available: {round(free_space/(1024*1024),2)} MB", "INFO")
            if not get_user_permission("Risk of failure due to low space. Continue anyway?"):
                print_status(f"Skipped {name} by user request.", "WARN")
                continue

        print_status(f"Compressing Target: {name} ({size_mb} MB)...", "INFO")
        
        try:
            # A. Compress
            with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED, allowZip64=True) as zipf:
                for root, dirs, files in os.walk(path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, os.path.dirname(path))
                        zipf.write(file_path, arcname)
            
            # B. Verify
            print_status("Verifying archive integrity...", "INFO")
            is_valid = False
            try:
                with zipfile.ZipFile(zip_filename, 'r') as zipf:
                    if zipf.testzip() is None:
                        is_valid = True
            except:
                pass

            if is_valid:
                print_status("Integrity Check: PASSED", "OK")
                
                # --- PERMISSION BLOCK (CRITICAL) ---
                print_status(f"Original Folder Size: {size_mb} MB", "INFO")
                if get_user_permission(f"SUCCESS! Delete original folder '{name}' now?"):
                    try:
                        shutil.rmtree(path)
                        print_status(f"Original folder removed. Space recovered.", "OK")
                    except Exception as e:
                        print_status(f"Error deleting folder: {e}", "ERR")
                else:
                    print_status("Folder kept. No space recovered.", "WARN")
                # -----------------------------------
            
            else:
                print_status("Integrity Check: FAILED. Archive is corrupt.", "ERR")
                os.remove(zip_filename) # Bad zip remove karne me risk nahi hai, wo user ke kaam ka nahi
                print_status("Corrupt archive removed automatically.", "WARN")

        except Exception as e:
            print_status(f"System Exception: {e}", "ERR")
            if os.path.exists(zip_filename):
                os.remove(zip_filename)
        
        print("-" * 30)

def main():
    print("\n" + "="*50)
    print("   SECURE COMPRESSOR TOOL v2.0   ")
    print("   [!] USER PERMISSION REQUIRED MODE")
    print("="*50)

    target_dir = input("ENTER TARGET DIRECTORY PATH: ").strip().strip('"')

    if not os.path.exists(target_dir):
        print_status("Directory not found.", "ERR")
        input("Press ENTER to exit...")
        return

    # Phase 1
    cleanup_module(target_dir)
    
    # Phase 2
    compression_module(target_dir)

    print("\n" + "="*50)
    print_status("SESSION TERMINATED.", "OK")
    input("Press ENTER to close...")

if __name__ == "__main__":
    main()