import os
import sys
import img2pdf
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
import fitz  # PyMuPDF
import pytesseract
from PIL import Image
from docx2pdf import convert as word_to_pdf_convert

# --- UTILS IMPORT SETUP ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clear, header, get_path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# --- HELPER: INPUT PARSER (Smart List) ---
def parse_page_input(input_str, total_pages):
    """
    User agar bole "1,3,5" ya "1-3", to use machine ke samajhne layak banata hai.
    Returns: A set of valid page indices (0-based).
    """
    selected_pages = set()
    parts = input_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            try:
                start, end = map(int, part.split('-'))
                # Validation
                if 1 <= start <= end <= total_pages:
                    for p in range(start, end + 1):
                        selected_pages.add(p - 1) # 0-based index
            except ValueError:
                continue
        else:
            try:
                page = int(part)
                if 1 <= page <= total_pages:
                    selected_pages.add(page - 1)
            except ValueError:
                continue
    return sorted(list(selected_pages))

# --- MAIN MENU ---
def run_menu():
    while True:
        header("📁 FILE TOOLS - ORGANIZE SPECIAL")
        print("==========================================")
        print(" 📌 ORGANIZE PDF:")
        print(" [1] Merge PDF       (Jodna)")
        print(" [2] Split PDF       (Todna)")
        print(" [3] Remove Pages    (Delete specific pages)")
        print(" [4] Extract Pages   (Save specific pages)")
        print(" [5] Organize PDF    (Re-order pages)")
        print(" [6] Scan to PDF     (Images -> PDF)")
        print("------------------------------------------")
        print(" 🚀 OPTIMIZE PDF:")
        print(" [7] Compress PDF    (Size kam karna)")
        print(" [8] Repair PDF      (Fix corrupt file)")
        print(" [9] OCR PDF         (Image se Text nikalna)")
        print("------------------------------------------")
        print(" 🔄 CONVERT TO PDF:")
        print(" [10] JPG to PDF")
        print(" [11] Word to PDF")
        print(" [12] PowerPoint to PDF")
        print(" [13] Excel to PDF")
        print(" [14] HTML to PDF")
        print("------------------------------------------")
        print(" 🔙 CONVERT FROM PDF:")
        print(" [15] PDF to JPG")
        print(" [16] PDF to Word")
        print(" [17] PDF to PowerPoint")
        print(" [18] PDF to Excel")
        print(" [19] PDF to PDF/A")
        print("------------------------------------------")
        print(" ✏️ EDIT PDF:")
        print(" [20] Rotate PDF     [21] Add Page Numbers")
        print(" [22] Add Watermark  [23] Crop PDF")
        print(" [24] Edit PDF (Text)[25] Remove Watermark")
        print("------------------------------------------")
        print(" 🔒 PDF SECURITY:")
        print(" [26] Unlock PDF     [27] Protect PDF")
        print(" [28] Sign PDF       [29] Redact PDF")
        print(" [30] Compare PDF")
        print("------------------------------------------")
        print(" [0] Back")
        print("==========================================")
        
        c = input("\nSelect Option (0-6): ")
        
        if c == '0': break

        # ==========================================
        # 1. MERGE PDF
        # ==========================================
        if c == '1':
            folder = get_path("Folder Path jahan PDFs hain")
            if folder:
                merger = PdfMerger()
                files = [f for f in os.listdir(folder) if f.lower().endswith('.pdf')]
                files.sort()
                
                if len(files) < 2:
                    print("❌ Error: Merge karne ke liye kam se kam 2 PDF honi chahiye.")
                else:
                    print(f"ℹ️ Found {len(files)} files. Merging...")
                    for f in files:
                        merger.append(os.path.join(folder, f))
                    
                    out_path = os.path.join(folder, "Merged_Result.pdf")
                    merger.write(out_path)
                    merger.close()
                    print(f"✅ Success! File saved: {out_path}")
                input("Press Enter...")

        # ==========================================
        # 2. SPLIT PDF
        # ==========================================
        elif c == '2':
            pdf = get_path("PDF File Path")
            if pdf:
                reader = PdfReader(pdf)
                folder = os.path.dirname(pdf)
                name = os.path.splitext(os.path.basename(pdf))[0]
                
                # New folder create karo
                split_dir = os.path.join(folder, f"{name}_Split")
                if not os.path.exists(split_dir): os.makedirs(split_dir)
                
                print(f"ℹ️ Splitting {len(reader.pages)} pages...")
                for i, page in enumerate(reader.pages):
                    writer = PdfWriter()
                    writer.add_page(page)
                    output_filename = os.path.join(split_dir, f"Page_{i+1}.pdf")
                    with open(output_filename, "wb") as f:
                        writer.write(f)
                
                print(f"✅ Success! Saare pages yahan hain:\n{split_dir}")
                input("Press Enter...")

        # ==========================================
        # 3. REMOVE PAGES
        # ==========================================
        elif c == '3':
            pdf = get_path("PDF File Path")
            if pdf:
                reader = PdfReader(pdf)
                total = len(reader.pages)
                print(f"ℹ️ Total Pages: {total}")
                print("Kaunse pages hatane hain? (Example: 2,4 ya 1-3)")
                
                user_input = input("Page Numbers: ")
                pages_to_remove = parse_page_input(user_input, total)
                
                if not pages_to_remove:
                    print("❌ Error: Valid page number nahi mila.")
                else:
                    writer = PdfWriter()
                    removed_count = 0
                    for i in range(total):
                        if i not in pages_to_remove:
                            writer.add_page(reader.pages[i])
                        else:
                            removed_count += 1
                    
                    out_path = pdf.replace(".pdf", "_PagesRemoved.pdf")
                    with open(out_path, "wb") as f: writer.write(f)
                    print(f"✅ Done! {removed_count} pages hata diye gaye.")
                    print(f"📂 Saved as: {out_path}")
                input("Press Enter...")

        # ==========================================
        # 4. EXTRACT PAGES
        # ==========================================
        elif c == '4':
            pdf = get_path("PDF File Path")
            if pdf:
                reader = PdfReader(pdf)
                total = len(reader.pages)
                print(f"ℹ️ Total Pages: {total}")
                print("Kaunse pages nikalne hain? (Example: 1,5,10)")
                
                user_input = input("Page Numbers: ")
                pages_to_extract = parse_page_input(user_input, total)
                
                if not pages_to_extract:
                    print("❌ Error: Koi valid page select nahi kiya.")
                else:
                    writer = PdfWriter()
                    for idx in pages_to_extract:
                        writer.add_page(reader.pages[idx])
                    
                    out_path = pdf.replace(".pdf", "_Extracted.pdf")
                    with open(out_path, "wb") as f: writer.write(f)
                    print(f"✅ Success! {len(pages_to_extract)} pages extract ho gaye.")
                    print(f"📂 Saved as: {out_path}")
                input("Press Enter...")

        # ==========================================
        # 5. ORGANIZE PDF (Re-Order)
        # ==========================================
        elif c == '5':
            pdf = get_path("PDF File Path")
            if pdf:
                reader = PdfReader(pdf)
                total = len(reader.pages)
                print(f"ℹ️ Total Pages: {total}")
                print("Example Order: 3,1,2 (Page 3 pehle aayega, phir 1, phir 2)")
                print("⚠️ Dhyan rahe: Jo page number nahi likhoge, wo gayab ho jayega.")
                
                order_input = input("New Order (Comma separated): ")
                # Simple parsing for order
                try:
                    # User input: "3, 1, 2" -> List: [2, 0, 1] (Indices)
                    new_order_indices = []
                    parts = order_input.split(',')
                    for p in parts:
                        idx = int(p.strip()) - 1
                        if 0 <= idx < total:
                            new_order_indices.append(idx)
                        else:
                            print(f"⚠️ Page {p} exist nahi karta, skip kar raha hu.")

                    if not new_order_indices:
                        print("❌ Error: Koi valid order nahi mila.")
                    else:
                        writer = PdfWriter()
                        for idx in new_order_indices:
                            writer.add_page(reader.pages[idx])
                        
                        out_path = pdf.replace(".pdf", "_Reorganized.pdf")
                        with open(out_path, "wb") as f: writer.write(f)
                        print("✅ PDF Re-organized successfully!")
                        print(f"📂 Saved as: {out_path}")
                        
                except ValueError:
                    print("❌ Error: Sirf numbers comma laga kar likho.")
                input("Press Enter...")

        # ==========================================
        # 6. SCAN TO PDF
        # ==========================================
        elif c == '6':
            folder = get_path("Images wala Folder Path")
            if folder:
                # Sirf images uthayenge
                valid_exts = ('.jpg', '.jpeg', '.png')
                imgs = [i for i in os.listdir(folder) if i.lower().endswith(valid_exts)]
                imgs.sort() # Name ke hisaab se line me lagana
                
                if not imgs:
                    print("❌ Error: Is folder me koi Image nahi mili.")
                else:
                    print(f"ℹ️ Found {len(imgs)} images. Creating PDF...")
                    full_paths = [os.path.join(folder, i) for i in imgs]
                    
                    out_path = os.path.join(folder, "Scanned_Doc.pdf")
                    try:
                        with open(out_path, "wb") as f:
                            f.write(img2pdf.convert(full_paths))
                        print("✅ Success! Images ki PDF ban gayi.")
                        print(f"📂 Saved as: {out_path}")
                    except Exception as e:
                        print(f"❌ Error: {e}")
                input("Press Enter...")
        
        # --- OPTIMIZE SECTION (7-9) ---
        elif c == '7': # Compress
            pdf = get_path("PDF Path")
            if pdf:
                try:
                    kb = float(input("Target Size (KB): "))
                    smart_compress_pdf(pdf, kb)
                except ValueError: print("❌ Number only.")
                input("Enter...")

        elif c == '8': # Repair
            pdf = get_path("Corrupt PDF Path")
            if pdf:
                repair_pdf_file(pdf)
                input("Enter...")

        elif c == '9': # OCR
            pdf = get_path("PDF Path")
            if pdf:
                if os.path.exists(pytesseract.pytesseract.tesseract_cmd):
                    ocr_pdf_processing(pdf)
                else:
                    print("❌ Error: Tesseract install nahi hai ya path galat hai.")
                input("Enter...")
        
        # --- CONVERT TO PDF (10-14) ---
        elif c == '10': # JPG to PDF
            img = get_path("JPG Image")
            if img:
                with open(img.rsplit('.', 1)[0] + ".pdf", "wb") as f:
                    f.write(img2pdf.convert(img))
                print("✅ Converted!")
                input("Enter...")

        elif c == '11': # Word to PDF
            doc = get_path("Word File (.docx)")
            if doc:
                try:
                    word_to_pdf_convert(doc)
                    print("✅ Converted!")
                except: print("❌ MS Word needed or file error.")
                input("Enter...")

        elif c == '12': # PPT to PDF
            ppt = get_path("PowerPoint File (.pptx)")
            if ppt: ppt_to_pdf(ppt); input("Enter...")

        elif c == '13': # Excel to PDF
            xls = get_path("Excel File (.xlsx)")
            if xls: excel_to_pdf(xls); input("Enter...")

        elif c == '14': # HTML to PDF
            html_file = get_path("HTML File")
            if html_file:
                print("\n⚠️ Note: Best result ke liye Browser me open karke 'Print to PDF' karo.")
                print("Attempting basic conversion...")
                try:
                    # Basic approach without heavy wkhtmltopdf dependency
                    import win32api
                    win32api.ShellExecute(0, "print", html_file, None, ".", 0)
                    print("✅ Sent to Printer (Select 'Microsoft Print to PDF')")
                except:
                    print("❌ Error: Auto-print failed. Manually print karo.")
                input("Enter...")
        # --- CONVERT FROM PDF (15-19) ---
        elif c == '15': # PDF to JPG
            pdf = get_path("PDF Path")
            if pdf:
                doc = fitz.open(pdf)
                base = pdf.rsplit('.', 1)[0]
                for i, p in enumerate(doc):
                    p.get_pixmap(dpi=200).save(f"{base}_pg{i+1}.jpg")
                print("✅ Saved as JPGs!")
                input("Enter...")

        elif c == '16': # PDF to Word
            pdf = get_path("PDF Path")
            if pdf:
                from pdf2docx import Converter
                cv = Converter(pdf)
                cv.convert(pdf.replace(".pdf", ".docx"))
                cv.close()
                print("✅ Converted to Word!")
                input("Enter...")

        elif c == '17': # PDF to PPT
            pdf = get_path("PDF Path")
            if pdf: pdf_to_ppt_images(pdf); input("Enter...")

        elif c == '18': # PDF to Excel
            pdf = get_path("PDF Path")
            if pdf: pdf_to_excel_text(pdf); input("Enter...")

        elif c == '19': # PDF to PDF/A
            pdf = get_path("PDF Path")
            if pdf:
                print("Creating Archival Copy...")
                doc = fitz.open(pdf)
                # Deflate + Clean = Better compatibility
                doc.save(pdf.replace(".pdf", "_PDFA.pdf"), garbage=4, deflate=True)
                print("✅ Saved (Optimized for Storage)")
                input("Enter...")
        
        # --- EDIT PDF (20-25) ---
        elif c == '20': # Rotate
            pdf = get_path("PDF Path")
            if pdf:
                deg = int(input("Degrees (90/180/270): "))
                doc = fitz.open(pdf)
                for page in doc: page.set_rotation(deg)
                doc.save(pdf.replace(".pdf", "_Rot.pdf"))
                print("✅ Rotated!"); input("Enter...")

        elif c == '21': # Page Numbers
            pdf = get_path("PDF Path")
            if pdf:
                doc = fitz.open(pdf)
                for i, page in enumerate(doc):
                    # Insert at bottom center
                    page.insert_text((page.rect.width/2 - 10, page.rect.height - 20), f"{i+1}", fontsize=12)
                doc.save(pdf.replace(".pdf", "_Num.pdf"))
                print("✅ Page Numbers Added!"); input("Enter...")

        elif c == '22': # Watermark
            pdf = get_path("PDF Path")
            if pdf: add_watermark_func(pdf, input("Watermark Text: ")); input("Enter...")

        elif c == '23': # Crop
            pdf = get_path("PDF Path")
            if pdf:
                print("Enter Margins to cut (approx pixels, e.g. 50)")
                margin = float(input("Margin: "))
                doc = fitz.open(pdf)
                for page in doc:
                    page.set_cropbox(fitz.Rect(margin, margin, page.rect.width-margin, page.rect.height-margin))
                doc.save(pdf.replace(".pdf", "_Crop.pdf"))
                print("✅ Cropped!"); input("Enter...")

        elif c == '24': # Edit/Add Text
            pdf = get_path("PDF Path")
            if pdf:
                txt = input("Text to Add: ")
                print("Position: Top-Left=1, Center=2")
                pos = input("Select: ")
                doc = fitz.open(pdf)
                for page in doc:
                    pt = fitz.Point(50, 50) if pos == '1' else fitz.Point(page.rect.width/2, page.rect.height/2)
                    page.insert_text(pt, txt, fontsize=12, color=(0,0,1))
                doc.save(pdf.replace(".pdf", "_Edited.pdf"))
                print("✅ Text Added!"); input("Enter...")

        elif c == '25': # Remove Watermark
            pdf = get_path("PDF Path")
            if pdf:
                txt = input("Exact Text of Watermark to remove: ")
                remove_watermark_func(pdf, txt)
                input("Enter...")
        
        # --- SECURITY PDF (26-30) ---
        elif c == '26': # Unlock
            pdf = get_path("Locked PDF Path")
            if pdf: security_unlock_pdf(pdf); input("Enter...")

        elif c == '27': # Protect
            pdf = get_path("PDF Path")
            if pdf: security_protect_pdf(pdf); input("Enter...")

        elif c == '28': # Sign
            pdf = get_path("PDF Path")
            if pdf: security_sign_pdf(pdf); input("Enter...")

        elif c == '29': # Redact
            pdf = get_path("PDF Path")
            if pdf: security_redact_pdf(pdf); input("Enter...")

        elif c == '30': # Compare
            pdf = get_path("First PDF Path")
            if pdf: security_compare_pdf(pdf); input("Enter...")
        else:
            print("\n❌ Invalid Option!")
            input("Press Enter...")
    
    



def smart_compress_pdf(input_path, target_kb):
    """PDF Size kam karne ka logic"""
    print(f"\n⚙️ Analyzing: {os.path.basename(input_path)}...")
    curr_size = os.path.getsize(input_path) / 1024
    
    if curr_size <= target_kb:
        print(f"✅ File pehle se target se choti hai ({int(curr_size)} KB).")
        return

    out_path = input_path.replace(".pdf", "_Compressed.pdf")
    print(f"🚀 Compressing... ({int(curr_size)} KB -> Target: {target_kb} KB)")
    
    try:
        doc = fitz.open(input_path)
        doc.save(out_path, garbage=4, deflate=True)
        doc.close()
        
        new_size = os.path.getsize(out_path) / 1024
        
        if new_size > target_kb:
            print(f"⚠️ Level 1 Result: {int(new_size)} KB. Aggressive Mode ON...")
            doc = fitz.open(out_path)
            doc.squeeze(out_path, garbage=4) # Heavy compression
            doc.close()
            final_size = os.path.getsize(out_path) / 1024
            print(f"✅ Final Size: {int(final_size)} KB")
        else:
            print(f"✅ Success! New Size: {int(new_size)} KB")
    except Exception as e:
        print(f"❌ Compression Error: {e}")

def repair_pdf_file(input_path):
    """Tooti hui PDF theek karna"""
    print("\n🛠️ Repairing PDF structure...")
    out_path = input_path.replace(".pdf", "_Repaired.pdf")
    try:
        doc = fitz.open(input_path)
        doc.save(out_path, garbage=3, deflate=True)
        doc.close()
        print(f"✅ Repaired & Saved: {out_path}")
    except Exception as e:
        print(f"❌ Repair Failed: {e}")

def ocr_pdf_processing(input_path):
    """Image wali PDF se Text nikalna"""
    print("\n👁️ OCR Running... (Reading Text from Images)")
    try:
        doc = fitz.open(input_path)
        full_text = ""
        for i, page in enumerate(doc):
            print(f"   Scanning Page {i+1}...")
            pix = page.get_pixmap(dpi=300)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img)
            full_text += f"--- PAGE {i+1} ---\n{text}\n"
        
        doc.close()
        txt_path = input_path.replace(".pdf", "_OCR_Text.txt")
        with open(txt_path, "w", encoding="utf-8") as f: f.write(full_text)
        print(f"✅ Text extracted to: {txt_path}")
    except Exception as e:
        print(f"❌ OCR Error: {e}")


def ppt_to_pdf(input_path):
    """PowerPoint to PDF using Windows COM"""
    try:
        import win32com.client
        powerpoint = win32com.client.Dispatch("PowerPoint.Application")
        powerpoint.Visible = 1
        deck = powerpoint.Presentations.Open(input_path)
        deck.SaveAs(input_path.rsplit('.', 1)[0] + ".pdf", 32) # 32 = ppSaveAsPDF
        deck.Close()
        powerpoint.Quit()
        print("✅ PowerPoint converted to PDF!")
    except Exception as e:
        print(f"❌ Error: MS PowerPoint install hona chahiye.\nDetails: {e}")

def excel_to_pdf(input_path):
    """Excel to PDF using Windows COM"""
    try:
        import win32com.client
        excel = win32com.client.Dispatch("Excel.Application")
        excel.Visible = False
        wb = excel.Workbooks.Open(input_path)
        # 0 = xlTypePDF
        wb.ExportAsFixedFormat(0, input_path.rsplit('.', 1)[0] + ".pdf")
        wb.Close()
        excel.Quit()
        print("✅ Excel converted to PDF!")
    except Exception as e:
        print(f"❌ Error: MS Excel install hona chahiye.\nDetails: {e}")
    
# --- MS OFFICE AUTOMATION HELPER ---
def office_to_pdf(input_path, app_name, save_code):
    try:
        import win32com.client
        app = win32com.client.Dispatch(app_name)
        app.Visible = 0
        if app_name == "PowerPoint.Application":
            doc = app.Presentations.Open(input_path)
            doc.SaveAs(input_path.rsplit('.', 1)[0] + ".pdf", save_code)
            doc.Close()
        elif app_name == "Excel.Application":
            doc = app.Workbooks.Open(input_path)
            doc.ExportAsFixedFormat(0, input_path.rsplit('.', 1)[0] + ".pdf")
            doc.Close()
        app.Quit()
        print("✅ Converted to PDF!")
    except Exception as e:
        print(f"❌ MS Office Error: {e}")

# --- NEW: PDF TO POWERPOINT (Images -> Slides) ---
def pdf_to_ppt_images(input_path):
    print("⏳ Converting PDF pages to Slides (via Images)...")
    try:
        import win32com.client
        ppt_app = win32com.client.Dispatch("PowerPoint.Application")
        ppt_app.Visible = 1
        pres = ppt_app.Presentations.Add()
        
        doc = fitz.open(input_path)
        temp_images = []
        
        for i, page in enumerate(doc):
            # 1. Convert Page to Image
            pix = page.get_pixmap(dpi=150)
            img_path = os.path.join(os.path.dirname(input_path), f"temp_slide_{i}.jpg")
            pix.save(img_path)
            temp_images.append(img_path)
            
            # 2. Add Slide & Insert Image
            slide = pres.Slides.Add(i + 1, 12) # 12 = ppLayoutBlank
            slide.Shapes.AddPicture(FileName=img_path, LinkToFile=False, SaveWithDocument=True, Left=0, Top=0, Width=720, Height=540)
        
        save_path = input_path.replace(".pdf", ".pptx")
        pres.SaveAs(save_path)
        pres.Close()
        ppt_app.Quit()
        
        # Cleanup temp images
        for img in temp_images:
            if os.path.exists(img): os.remove(img)
            
        print(f"✅ PPTX Saved: {save_path}")
    except Exception as e:
        print(f"❌ PPT Error: MS PowerPoint required.\n{e}")

# --- NEW: PDF TO EXCEL (Text -> CSV) ---
def pdf_to_excel_text(input_path):
    print("⏳ Extracting Text to CSV (Excel readable)...")
    try:
        import csv
        doc = fitz.open(input_path)
        csv_path = input_path.replace(".pdf", ".csv")
        
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            for page in doc:
                text = page.get_text("text")
                # Split lines and write as rows
                lines = text.split('\n')
                for line in lines:
                    if line.strip():
                        writer.writerow([line.strip()])
        
        print(f"✅ CSV Saved (Open in Excel): {csv_path}")
    except Exception as e:
        print(f"❌ Excel Error: {e}")


def add_watermark_func(input_path, text):
    print("⏳ Adding Watermark...")
    out = input_path.replace(".pdf", "_Watermarked.pdf")
    doc = fitz.open(input_path)
    for page in doc:
        # Center of page
        p_center = fitz.Point(page.rect.width / 2, page.rect.height / 2)
        # Text insert (Rotate 45 deg, Grey color)
        page.insert_text(p_center, text, fontsize=50, rotate=45, color=(0.7, 0.7, 0.7), align=1)
    doc.save(out)
    print(f"✅ Saved: {out}")

def remove_watermark_func(input_path, text_to_remove):
    print("⏳ Attempting to remove text...")
    out = input_path.replace(".pdf", "_Cleaned.pdf")
    doc = fitz.open(input_path)
    count = 0
    for page in doc:
        # Search for text
        text_instances = page.search_for(text_to_remove)
        for inst in text_instances:
            page.add_redact_annot(inst, fill=(1, 1, 1)) # White fill
            count += 1
        page.apply_redactions()
    doc.save(out)
    if count > 0: print(f"✅ Removed {count} instances. Saved: {out}")
    else: print("❌ Text match nahi mila.")


# ==========================================
# 🔒 SECURITY FUNCTIONS (NEW)
# ==========================================

def security_unlock_pdf(input_path):
    print("\n🔓 Unlocking PDF...")
    try:
        # PyMuPDF se file kholo
        doc = fitz.open(input_path)
        
        # Check karo agar encrypted hai
        if doc.is_encrypted:
            pwd = input("Enter Password: ")
            if not doc.authenticate(pwd):
                print("❌ Galat Password! Unlock nahi hua.")
                return
        
        # Bina encryption ke save karo
        out_path = input_path.replace(".pdf", "_UNLOCKED.pdf")
        doc.save(out_path)
        print(f"✅ Success! Unlocked file: {out_path}")
    except Exception as e:
        print(f"❌ Error: {e}")

def security_protect_pdf(input_path):
    print("\n🛡️ Protecting PDF...")
    pwd = input("Set New Password: ")
    out_path = input_path.replace(".pdf", "_PROTECTED.pdf")
    
    try:
        doc = fitz.open(input_path)
        # encryption=fitz.PDF_ENCRYPT_AES_256 sabse strong hai
        doc.save(out_path, encryption=fitz.PDF_ENCRYPT_AES_256, owner_pw=pwd, user_pw=pwd)
        print(f"✅ Success! Password set on: {out_path}")
    except Exception as e:
        print(f"❌ Error: {e}")

def security_sign_pdf(input_path):
    print("\n✍️ Sign PDF (Visual Signature)")
    sig_img = get_path("Signature Image Path (.png/.jpg)")
    if not sig_img: return

    try:
        doc = fitz.open(input_path)
        print(f"PDF has {len(doc)} pages.")
        pg_num = int(input("Page Number for Signature: ")) - 1
        
        if 0 <= pg_num < len(doc):
            page = doc[pg_num]
            # Signature ko bottom-right corner me lagayenge (Customizable)
            rect = fitz.Rect(page.rect.width - 200, page.rect.height - 100, page.rect.width - 50, page.rect.height - 50)
            page.insert_image(rect, filename=sig_img)
            
            out_path = input_path.replace(".pdf", "_SIGNED.pdf")
            doc.save(out_path)
            print(f"✅ Signed File Saved: {out_path}")
        else:
            print("❌ Invalid Page Number.")
    except Exception as e:
        print(f"❌ Error: {e}")

def security_redact_pdf(input_path):
    print("\n██ Redacting PDF (Hiding Sensitive Text)")
    sensitive_text = input("Word/Text to Hide (Case Sensitive): ")
    out_path = input_path.replace(".pdf", "_REDACTED.pdf")
    
    try:
        doc = fitz.open(input_path)
        count = 0
        for page in doc:
            # Text dhoondho
            areas = page.search_for(sensitive_text)
            for area in areas:
                # Black box banao (Redaction)
                page.add_redact_annot(area, fill=(0, 0, 0))
                count += 1
            # Redaction apply karo (Permanent delete)
            page.apply_redactions()
            
        if count > 0:
            doc.save(out_path)
            print(f"✅ Hidden {count} instances of '{sensitive_text}'.")
            print(f"📂 Saved: {out_path}")
        else:
            print("❌ Wo text nahi mila file mein.")
    except Exception as e:
        print(f"❌ Error: {e}")

def security_compare_pdf(path_a):
    print("\n⚖️ Compare PDFs (Text Mode)")
    path_b = get_path("Second PDF Path to Compare")
    if not path_b: return

    try:
        import difflib
        # Text extract karo dono files se
        txt_a = ""
        with fitz.open(path_a) as doc:
            for page in doc: txt_a += page.get_text()
            
        txt_b = ""
        with fitz.open(path_b) as doc:
            for page in doc: txt_b += page.get_text()
            
        # Compare karo
        diff = difflib.unified_diff(txt_a.splitlines(), txt_b.splitlines(), lineterm='')
        diff_list = list(diff)
        
        if not diff_list:
            print("✅ Both PDFs have EXACTLY same text.")
        else:
            print("⚠️ Differences Found!")
            out_txt = path_a.replace(".pdf", "_COMPARE_RESULT.txt")
            with open(out_txt, "w", encoding="utf-8") as f:
                f.write("\n".join(diff_list))
            print(f"📂 Differences saved to: {out_txt}")
            
    except Exception as e:
        print(f"❌ Error: {e}")