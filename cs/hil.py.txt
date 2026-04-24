import numpy as np
import re

# -------- KEY MATRIX --------
def generate_key_matrix(key):
    key = re.sub(r'[^A-Z]', '', key.upper())
    length = len(key)

    n = int(length ** 0.5)
    if n * n != length:
        raise ValueError("Key length must be perfect square (4, 9, 16...)")

    values = [ord(c) - ord('A') for c in key]
    matrix = np.array(values).reshape(n, n)

    return matrix, n


# -------- MODULAR INVERSE --------
def mod_inverse(a, m=26):
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None


# -------- MATRIX INVERSE (mod 26) --------
def generate_inverse_matrix(matrix):
    det = int(round(np.linalg.det(matrix)))
    det_mod = det % 26

    det_inv = mod_inverse(det_mod)
    if det_inv is None:
        raise ValueError("Matrix not invertible mod 26. Change key.")

    # Adjoint matrix
    adj = np.round(det * np.linalg.inv(matrix)).astype(int)

    inverse = (det_inv * adj) % 26
    return inverse


# -------- ENCRYPTION --------
def encrypt_file(key):
    matrix, n = generate_key_matrix(key)

    with open("plaintext.txt", "r") as f:
        text = f.read()

    text = re.sub(r'[^A-Z]', '', text.upper())
    values = [ord(c) - ord('A') for c in text]

    # Padding
    while len(values) % n != 0:
        values.append(ord('X') - ord('A'))

    cipher = ""

    for i in range(0, len(values), n):
        block = np.array(values[i:i+n]).reshape(n, 1)
        result = np.dot(matrix, block) % 26

        cipher += ''.join(chr(int(x) + ord('A')) for x in result.flatten())

    with open("ciphertext.txt", "w") as f:
        f.write(cipher)

    print("Encryption Successful → ciphertext.txt")


# -------- DECRYPTION --------
def decrypt_file(key):
    matrix, n = generate_key_matrix(key)
    inverse_matrix = generate_inverse_matrix(matrix)

    with open("ciphertext.txt", "r") as f:
        cipher = f.read()

    values = [ord(c) - ord('A') for c in cipher]
    plain = ""

    for i in range(0, len(values), n):
        block = np.array(values[i:i+n]).reshape(n, 1)
        result = np.dot(inverse_matrix, block) % 26

        plain += ''.join(chr(int(x) + ord('A')) for x in result.flatten())

    with open("decrypted_text.txt", "w") as f:
        f.write(plain)

    print("Decryption Successful → decrypted_text.txt")


# -------- MENU --------
if __name__ == "__main__":
    while True:
        print("\n===== Hill Cipher =====")
        print("1. Encryption")
        print("2. Decryption")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            key = input("Enter key (perfect square length): ")
            try:
                encrypt_file(key)
            except Exception as e:
                print("Error:", e)

        elif choice == "2":
            key = input("Enter same key: ")
            try:
                decrypt_file(key)
            except Exception as e:
                print("Error:", e)

        elif choice == "0":
            print("Program exited.")
            break

        else:
            print("Invalid choice!")