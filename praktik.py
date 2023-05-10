import pymongo
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes


# Koneksi ke basis data MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["Chat"]
col = db["Chat"]


# Generate key RSA
key = RSA.generate(2048)


# Fungsi untuk melakukan enkripsi pesan
def encrypt_message(message):
    public_key = key.publickey()
    cipher_rsa = PKCS1_OAEP.new(public_key)
    # Generate random key untuk AES
    session_key = get_random_bytes(16)
    # Enkripsi pesan menggunakan AES
    cipher_aes = AES.new(session_key, AES.MODE_EAX)
    ciphertext, tag = cipher_aes.encrypt_and_digest(message.encode())
    # Enkripsi session key menggunakan RSA
    encrypted_session_key = cipher_rsa.encrypt(session_key)
    # Gabungkan data enkripsi menjadi satu pesan yang terenkripsi
    encrypted_message = encrypted_session_key + cipher_aes.nonce + tag + ciphertext
    return base64.b64encode(encrypted_message).decode()


# Fungsi untuk melakukan dekripsi pesan
def decrypt_message(encrypted_message):
    private_key = key
    cipher_rsa = PKCS1_OAEP.new(private_key)
    # Potong data enkripsi menjadi bagian-bagian
    encrypted_message = base64.b64decode(encrypted_message)
    encrypted_session_key = encrypted_message[:private_key.size_in_bytes()]
    nonce = encrypted_message[private_key.size_in_bytes():private_key.size_in_bytes()+16]
    tag = encrypted_message[private_key.size_in_bytes()+16:private_key.size_in_bytes()+32]
    ciphertext = encrypted_message[private_key.size_in_bytes()+32:]
    # Dekripsi session key menggunakan RSA
    session_key = cipher_rsa.decrypt(encrypted_session_key)
    # Dekripsi pesan menggunakan AES
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce=nonce)
    decrypted_message = cipher_aes.decrypt_and_verify(ciphertext, tag)
    return decrypted_message.decode()


# Halaman untuk menginput chat yang sudah terenkripsi ke basis data
def input_chat():
    name = input("Masukkan nama pengguna: ")
    message = input("Masukkan pesan: ")
    encrypted_message = encrypt_message(message)
    data = {"name": name, "message": encrypted_message}
    col.insert_one(data)
    print("Pesan berhasil dienkripsi dan disimpan ke basis data")


# Halaman untuk mengambil hasil chat yang sudah didekripsi dari basis data
def get_chat():
    name = input("Masukkan nama pengguna: ")
    results = col.find({"name": name})
    for result in results:
        decrypted_message = decrypt_message(result["message"])
        print(result["name"] + ": " + decrypted_message)


# Main program
while True:
    print("\n--- ChatGPT ---")
    print("1. Input chat")
    print("2. Tampilkan chat")
    print("3. Keluar")
    choice = input("Pilih menu: ")
    if choice == "1":
        input_chat()
    elif choice == "2":
        get_chat()
    elif choice == "3":
        break
    else:
        print("Menu tidak tersedia")







