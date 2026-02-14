import os
import sys
from PIL import Image, ImageFilter, ImageOps, ImageDraw, ImageFont

# --- UTILS IMPORT SETUP ---
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import clear, header, get_path

# ==========================================
# 🧠 HELPER FUNCTIONS
# ==========================================

def compress_image(img_path):
    print("\n🗜️ Compress Image")
    try:
        quality = int(input("Quality (1-100, lower is smaller): ") or "50")
        img = Image.open(img_path)
        out = img_path.rsplit('.', 1)[0] + "_compressed.jpg"
        # JPG format required for compression quality
        img = img.convert("RGB")
        img.save(out, optimize=True, quality=quality)
        print(f"✅ Saved: {out}")
    except Exception as e: print(f"❌ Error: {e}")

def upscale_image(img_path):
    print("\n📈 Upscale Image (2x, 4x)")
    try:
        factor = int(input("Upscale Factor (2 or 4): ") or "2")
        img = Image.open(img_path)
        new_size = (int(img.width * factor), int(img.height * factor))
        # High Quality Resampling (LANCZOS)
        img = img.resize(new_size, Image.Resampling.LANCZOS)
        out = img_path.rsplit('.', 1)[0] + f"_upscaled_{factor}x.png"
        img.save(out)
        print(f"✅ Saved: {out}")
    except Exception as e: print(f"❌ Error: {e}")

def remove_background(img_path):
    print("\n👻 Removing Background (AI Magic)...")
    print("⏳ First time will take time to download AI model. Please wait...")
    try:
        from rembg import remove
        img = Image.open(img_path)
        output = remove(img)
        out = img_path.rsplit('.', 1)[0] + "_no_bg.png"
        output.save(out)
        print(f"✅ Background Removed! Saved: {out}")
    except ImportError:
        print("❌ Error: 'rembg' installed nahi hai.")
        print("Run: pip install rembg")
    except Exception as e:
        print(f"❌ Error: {e}")

def resize_image(img_path):
    print("\n📐 Resize Image")
    try:
        img = Image.open(img_path)
        print(f"Current Size: {img.width}x{img.height}")
        w = int(input("New Width: "))
        h = int(input("New Height: "))
        img = img.resize((w, h), Image.Resampling.LANCZOS)
        img.save(img_path.rsplit('.', 1)[0] + f"_resized_{w}x{h}.jpg")
        print("✅ Done!")
    except: print("❌ Error")

def crop_image(img_path):
    print("\n✂️ Crop Image")
    try:
        img = Image.open(img_path)
        print(f"Size: {img.width}x{img.height}")
        print("Enter coords (Left, Top, Right, Bottom)")
        left = int(input("Left: "))
        top = int(input("Top: "))
        right = int(input("Right: "))
        bottom = int(input("Bottom: "))
        img = img.crop((left, top, right, bottom))
        img.save(img_path.rsplit('.', 1)[0] + "_cropped.jpg")
        print("✅ Done!")
    except: print("❌ Error")

def meme_generator(img_path):
    print("\n🤡 Meme Generator")
    top_text = input("Top Text: ")
    bottom_text = input("Bottom Text: ")
    try:
        img = Image.open(img_path)
        draw = ImageDraw.Draw(img)
        
        # Font setup (Default Windows Font)
        try:
            font_path = "arialbd.ttf" # Bold Arial
            font_size = int(img.width / 10)
            font = ImageFont.truetype(font_path, font_size)
        except:
            font = ImageFont.load_default()

        # Helper to draw text with outline
        def draw_text_outline(text, position, font):
            # Outline (Black)
            x, y = position
            fill_color = "white"
            outline_color = "black"
            thickness = 2
            
            # Draw outline
            draw.text((x-thickness, y-thickness), text, font=font, fill=outline_color)
            draw.text((x+thickness, y-thickness), text, font=font, fill=outline_color)
            draw.text((x-thickness, y+thickness), text, font=font, fill=outline_color)
            draw.text((x+thickness, y+thickness), text, font=font, fill=outline_color)
            
            # Draw Main Text
            draw.text(position, text, font=font, fill=fill_color)

        # Draw Top
        if top_text:
            text_width = draw.textlength(top_text, font=font)
            x = (img.width - text_width) / 2
            draw_text_outline(top_text, (x, 10), font)
            
        # Draw Bottom
        if bottom_text:
            text_width = draw.textlength(bottom_text, font=font)
            x = (img.width - text_width) / 2
            y = img.height - font_size - 20
            draw_text_outline(bottom_text, (x, y), font)
            
        img.save(img_path.rsplit('.', 1)[0] + "_meme.jpg")
        print("✅ Meme Saved!")
    except Exception as e: print(f"❌ Error: {e}")

def blur_image(img_path):
    print("\n💧 Blur Image (Privacy)")
    try:
        img = Image.open(img_path)
        radius = int(input("Blur Intensity (e.g., 5, 10, 20): "))
        img = img.filter(ImageFilter.GaussianBlur(radius))
        img.save(img_path.rsplit('.', 1)[0] + "_blurred.jpg")
        print("✅ Done!")
    except: print("❌ Error")

# ==========================================
# 📋 MAIN MENU
# ==========================================

def run_menu():
    while True:
        header("🖼️ IMAGE TOOLS - THE OFFICE HQ")
        print("==========================================")
        
        print(" 🚀 OPTIMIZE:")
        print(" [1] Compress IMAGE   (Size kam karo)")
        print(" [2] Upscale IMAGE    (Resolution badhao)")
        print(" [3] Remove Background(AI powered)")
        print("------------------------------------------")
        
        print(" 🛠️ MODIFY:")
        print(" [4] Resize IMAGE     (Dimensions change)")
        print(" [5] Crop IMAGE       (Kaatna)")
        print(" [6] Rotate IMAGE     (Ghumana)")
        print("------------------------------------------")
        
        print(" 🔄 CONVERT:")
        print(" [7] Convert to JPG")
        print(" [8] Convert from JPG (to PNG/WebP)")
        print("------------------------------------------")
        
        print(" 🎨 CREATE & EDIT:")
        print(" [9] Photo Editor     (Filters: B&W, etc.)")
        print(" [10] Meme Generator  (Add Text)")
        print("------------------------------------------")
        
        print(" 🔒 SECURITY:")
        print(" [11] Watermark IMAGE")
        print(" [12] Blur Image      (Hide details)")
        print("------------------------------------------")
        
        print(" [0] Back")
        print("==========================================")
        
        c = input("\nSelect Option (0-12): ")
        if c == '0': break

        img_path = ""
        if c in [str(i) for i in range(1, 13)]:
            img_path = get_path("Image Path")
            if not img_path: continue

        # --- ACTIONS ---
        if c == '1': compress_image(img_path)
        
        elif c == '2': upscale_image(img_path)
        
        elif c == '3': remove_background(img_path)
        
        elif c == '4': resize_image(img_path)
        
        elif c == '5': crop_image(img_path)
        
        elif c == '6': # Rotate
            deg = int(input("Degrees (90/180): "))
            Image.open(img_path).rotate(-deg, expand=True).save(img_path.rsplit('.',1)[0]+"_rot.jpg")
            print("✅ Done!")

        elif c == '7': # To JPG
            Image.open(img_path).convert("RGB").save(img_path.rsplit('.',1)[0]+".jpg")
            print("✅ Converted to JPG")

        elif c == '8': # From JPG
            fmt = input("Format (png/webp): ").lower()
            Image.open(img_path).save(img_path.rsplit('.',1)[0]+f".{fmt}")
            print(f"✅ Converted to {fmt}")

        elif c == '9': # Photo Editor (Filters)
            print("Filters: [1] Grayscale [2] Contour [3] Sharpen")
            f = input("Select: ")
            img = Image.open(img_path)
            if f=='1': img = ImageOps.grayscale(img)
            elif f=='2': img = img.filter(ImageFilter.CONTOUR)
            elif f=='3': img = img.filter(ImageFilter.SHARPEN)
            img.save(img_path.rsplit('.',1)[0]+"_edited.jpg")
            print("✅ Filter Applied")

        elif c == '10': meme_generator(img_path)

        elif c == '11': # Watermark
            txt = input("Watermark Text: ")
            img = Image.open(img_path)
            draw = ImageDraw.Draw(img)
            font = ImageFont.load_default()
            draw.text((10, 10), txt, fill=(255,255,255), font=font)
            img.save(img_path.rsplit('.',1)[0]+"_wm.jpg")
            print("✅ Added")

        elif c == '12': blur_image(img_path)

        input("\nPress Enter to continue...")