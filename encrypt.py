from Crypto.Cipher import AES # sudo pacman -S python-pycryptodome
from Crypto.Util.Padding import pad, unpad
from hashlib import sha256
import subprocess, base64, os, platform

password = "carter_is_the_best_fr_fr"

def copy_to_clipboard(text):
    if subprocess.check_output(["which", "wl-copy"]):
        subprocess.run(["wl-copy"], input=text.encode())
    elif subprocess.check_output(["which", "xclip"]):
        subprocess.run(["xclip", "-selection", "clipboard"], input=text.encode())

def encrypt(plaintext, passphrase):
    key = sha256(passphrase.encode()).digest()
    iv = os.urandom(AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    padded_plaintext = pad(plaintext.encode(), AES.block_size)
    ciphertext = iv + cipher.encrypt(padded_plaintext)
    return base64.b64encode(ciphertext).decode()

def decrypt(ciphertext, passphrase):
    key = sha256(passphrase.encode()).digest()
    ciphertext = base64.b64decode(ciphertext)
    iv = ciphertext[:AES.block_size]
    ciphertext = ciphertext[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)
    return plaintext.decode()

if subprocess.check_output(["which", "wl-copy"]):
    clipboard_content = subprocess.getoutput("wl-paste")
elif subprocess.check_output(["which", "xclip"]):
    clipboard_content = subprocess.getoutput("xclip -o -selection clipboard")

if (clipboard_content[:2] == "&&"):
    input_text = clipboard_content
else:
    input_text = input("Input Text: ")

if input_text.startswith("&&"):
    decrypted_text = decrypt(input_text[2:], password)
    print("Decrypted text:", decrypted_text)
    copy_to_clipboard(decrypted_text)
else:
    encrypted_text = encrypt(input_text, password)
    encrypted_text = ("&&" + encrypted_text)
    copy_to_clipboard(encrypted_text)
    print("Encrypted text copied")