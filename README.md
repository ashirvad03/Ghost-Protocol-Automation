# 👻 Ghost Protocol

**Built out of laziness. Because organizing files manually is boring.**

I created **Ghost Protocol** because my `Downloads` folder was always a mess, and I hated manually zipping project files for backups. I needed a tool that just works—fast, secure, and without a GUI.

This isn't just a script; it's my daily system utility for Windows.

## 🛠️ What it actually does

### 1. Smart Organizer
You know how the Downloads folder gets cluttered with images, zips, and PDFs?
- This tool scans the folder.
- Detects file types.
- Moves them into neat folders (`/Images`, `/Docs`, `/Videos`) automatically.

### 2. Secure Compressor (The Best Part)
I didn't trust standard zip tools with my code backups, so I wrote my own logic:
- **Check 1:** Is there enough disk space?
- **Check 2:** Create the zip.
- **Check 3:** *Verify* the zip integrity.
- **Action:** Only delete the original folder IF the zip is 100% valid.
*Zero data loss.*

### 3. The Office HQ
A simple menu to handle media files (Video to Audio, Compression) using FFmpeg logic, so I don't have to use online converters.

## 💻 How to Run

You just need Python installed.

```bash
# Clone this repo
git clone [https://github.com/your-username/Ghost-Protocol-Automation](https://github.com/your-username/Ghost-Protocol-Automation)

# Run the script
python main.py
