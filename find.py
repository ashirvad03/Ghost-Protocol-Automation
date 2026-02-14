import os
import sys
import time
import requests
import phonenumbers
import webbrowser
from phonenumbers import geocoder, carrier, timezone

# --- COLORS ---
R = "\033[91m" 
G = "\033[92m" 
Y = "\033[93m" 
C = "\033[96m" 
W = "\033[97m" 

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear_screen()
    print(f"{C}========================================")
    print(f"{Y}      DIGITAL DETECTIVE (PRO)      ")
    print(f"{C}========================================{W}")

# --- 1. PHONE SCANNER (BASIC) ---
def phone_tracker():
    banner()
    print(f"{Y}[ PHONE NUMBER INFORMATION ]{W}\n")
    print("Format: +919876543210")
    number = input(f"{C}Target Number: {W}")

    if not number: return

    try:
        parsed_num = phonenumbers.parse(number)
        print(f"\n{G}[+] Fetching Tower Info...{W}")
        time.sleep(1)
        
        print("-" * 40)
        print(f"📍 Region   : {geocoder.description_for_number(parsed_num, 'en')}")
        print(f"📡 Carrier  : {carrier.name_for_number(parsed_num, 'en')}")
        print(f"⏰ Timezone : {timezone.time_zones_for_number(parsed_num)}")
        print("-" * 40)
        
        print(f"\n{Y}[TIP]{W} Iska Naam/IP janne ke liye Main Menu se Option 4 use karein.")
        
    except Exception:
        print(f"\n{R}[!] Invalid Number.{W}")
    
    input("\nPress Enter to go back...")

# --- 2. USERNAME HUNTER ---
def username_hunter():
    banner()
    print(f"{Y}[ USERNAME RECON ]{W}\n")
    username = input(f"{C}Target Username: {W}")
    if not username: return

    sites = {
        "Instagram": "https://www.instagram.com/{}",
        "Facebook": "https://www.facebook.com/{}",
        "Twitter": "https://twitter.com/{}",
        "GitHub": "https://github.com/{}",
        "Telegram": "https://t.me/{}"
    }

    print(f"\n{G}[+] Searching...{W}\n")
    for site, url in sites.items():
        try:
            r = requests.get(url.format(username), timeout=3)
            if r.status_code == 200:
                print(f"{G}[FOUND] {site}{W}")
        except:
            pass
    input("\nPress Enter to go back...")

# --- 3. IP TRACKER ---
def ip_tracker():
    banner()
    print(f"{Y}[ IP INFO ]{W}\n")
    ip = input("Enter IP Address: ")
    try:
        data = requests.get(f"http://ip-api.com/json/{ip}").json()
        print("-" * 40)
        print(f"City: {data.get('city')} | ISP: {data.get('isp')}")
        print(f"Map: http://maps.google.com/?q={data.get('lat')},{data.get('lon')}")
        print("-" * 40)
    except:
        print("Error fetching data.")
    input("\nPress Enter...")

# --- 4. ADVANCED TRACING (NAME & IP TRICK) ---
def advanced_trace():
    banner()
    print(f"{Y}[ ADVANCED TRACING & IP TRAP ]{W}\n")
    print("Yahan hum 'Social Engineering' aur 'OSINT' use karenge.")
    print("1. Find SIM Owner NAME (via Truecaller/Google)")
    print("2. How to get IP Address (IP Logger Method)")
    
    opt = input(f"\n{C}Option: {W}")

    if opt == '1':
        num = input("\nEnter Number (bina +91 ke): ")
        print(f"\n{G}[+] Opening Browser for Deep Search...{W}")
        # Ye direct browser open karega jahan data hone ke chance hain
        webbrowser.open(f"https://www.truecaller.com/search/in/{num}")
        webbrowser.open(f"https://www.google.com/search?q={num}")
        webbrowser.open(f"https://api.whatsapp.com/send?phone=91{num}")
        print("\nCheck your Browser tabs. Agar wahan naam dikha, to wahi asli hai.")

    elif opt == '2':
        print(f"\n{R}[ SECRET TECHNIQUE: IP LOGGING ]{W}")
        print("-" * 40)
        print("Phone Number se IP nahi nikalta. IP nikalne ke liye:")
        print("1. 'Grabify.link' website par jao.")
        print("2. Koi bhi YouTube video ka link wahan paste karo.")
        print("3. Wo aapko ek 'Tracking Link' dega.")
        print("4. Wo link Target (victim) ko bhejo.")
        print("5. Jaise hi wo click karega, uska IP aapko Grabify par dikh jayega.")
        print("-" * 40)
        print("Yehi ekmaatra tarika hai IP nikalne ka.")

    input("\nPress Enter to go back...")


# --- MAIN MENU ---
while True:
    banner()
    print("[1] Phone Number Info (Region/Sim)")
    print("[2] Username Hunter")
    print("[3] IP Geolocation")
    print(f"{R}[4] Advanced Trace (Find Name/IP Trick){W}")
    print("[5] Exit")
    print("-" * 40)
    
    choice = input(f"{C}Select > {W}")

    if choice == '1': phone_tracker()
    elif choice == '2': username_hunter()
    elif choice == '3': ip_tracker()
    elif choice == '4': advanced_trace()
    elif choice == '5': break