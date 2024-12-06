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
def encrypt(plaintext, passphrase):
    key = sha256(passphrase.encode()).digest()
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    ciphertext = iv + cipher.encrypt(padded_plaintext)
    return base64.b64encode(ciphertext).decode()
def decrypt(ciphertext, passphrase):
    try:
        key = sha256(passphrase.encode()).digest()
        ciphertext = base64.b64decode(ciphertext)
        iv = ciphertext[:AES.block_size]
        ciphertext = ciphertext[AES.block_size:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
        return plaintext.decode()
    except (ValueError, KeyError):
        return None
if os.environ.get("XDG_SESSION_TYPE") == "wayland" and subprocess.check_output(["which", "wl-copy"]):
    clipboard_content = subprocess.getoutput("wl-paste")
elif os.environ.get("XDG_SESSION_TYPE") == "x11" and subprocess.check_output(["which", "xclip"]):
    clipboard_content = subprocess.getoutput("xclip -o -selection clipboard")
else:
    print("linux/DE/xclip/wl-copy missing")
if clipboard_content.startswith("&&"):
    decrypted_text = decrypt(clipboard_content[2:], password)
    if decrypted_text is None:
        print("Incorrect password.")
    else:
        print(f"Decrypted text: {decrypted_text}")
    copy_to_clipboard("")
else:
    encrypted_text = encrypt(input("Input Text: "), password)
    copy_to_clipboard("&&" + encrypted_text)
    print("Encrypted text copied to clipboard.")
