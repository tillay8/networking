from Crypto.Cipher import AES  # sudo pacman -S python-pycryptodome
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import subprocess, base64, os, sys
password_file_path = "./password.txt"
password = (
    sys.argv[1] if len(sys.argv) > 1 
    else open(password_file_path).read().strip() if os.path.isfile(password_file_path)
    else input("Input password: ")
)
def copy_to_clipboard(text):
        if os.environ.get("XDG_SESSION_TYPE") == "wayland" and subprocess.check_output(["which", "wl-copy"]):
            subprocess.run(["wl-copy"], input=text.encode())
        elif os.environ.get("XDG_SESSION_TYPE") == "x11" and subprocess.check_output(["which", "xclip"]):
            subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode())
def process_clipboard_content(content, password, copy=False):
    if content.startswith("&&"):
        decrypted_text = decrypt(content[2:], password)
        if decrypted_text is None:
            print("Incorrect password.")
        else:
            print(f"Decrypted text: {decrypted_text}")
        if copy:
            copy_to_clipboard("")
    else:
        encrypted_text = encrypt(input("Text Input: "), password)
        if copy:
            copy_to_clipboard("&&" + encrypted_text)
            print("Encrypted text copied to clipboard.")
        else:
            print("&&" + encrypted_text)
def encrypt(plaintext, passphrase):
    key, iv = sha256(passphrase.encode()).digest(), os.urandom(AES.block_size)
    ciphertext = iv + AES.new(key, AES.MODE_CBC, iv).encrypt(pad(plaintext.encode(), AES.block_size))
    return base64.b64encode(ciphertext).decode()

def decrypt(ciphertext, passphrase):
    try:
        key, ciphertext = sha256(passphrase.encode()).digest(), base64.b64decode(ciphertext)
        iv, ciphertext = ciphertext[:AES.block_size], ciphertext[AES.block_size:]
        return unpad(AES.new(key, AES.MODE_CBC, iv).decrypt(ciphertext), AES.block_size).decode()
    except (ValueError, KeyError):
        return None

try:
    if os.environ.get("XDG_SESSION_TYPE") == "wayland" and subprocess.check_output(["which", "wl-copy"]):
        clipboard_content = subprocess.getoutput("wl-paste")
    elif os.environ.get("XDG_SESSION_TYPE") == "x11" and subprocess.check_output(["which", "xclip"]):
        clipboard_content = subprocess.getoutput("xclip -o -selection clipboard")
    process_clipboard_content(clipboard_content, password, copy=True)
except subprocess.CalledProcessError:
    print("Warning: linux/DE/xclip/wl-copy missing")
    clipboard_content = input("input text manually: ")
    process_clipboard_content(clipboard_content, password)
