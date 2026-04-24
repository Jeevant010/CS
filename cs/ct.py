import math

# Remove spaces from key
def process_key(key):
    return key.replace(" ", "")

# Generate column order
def get_key_order(key):
    order = []
    for i in range(len(key)):
        count = 0
        for j in range(len(key)):
            if key[j] < key[i]:
                count += 1
            elif key[j] == key[i] and j < i:
                count += 1
        order.append(count)
    return order


# ---------------- ENCRYPTION ----------------
def encrypt():
    try:
        with open("Plaintext.txt", "r") as f:
            text = f.read()
    except:
        print("File Error!")
        return

    key = input("Enter Key (Word or Sentence): ")
    key = process_key(key)

    key_len = len(key)
    text_len = len(text)
    order = get_key_order(key)

    rows = math.ceil(text_len / key_len)

    # Fill matrix with 'X'
    matrix = [['X' for _ in range(key_len)] for _ in range(rows)]

    k = 0
    for i in range(rows):
        for j in range(key_len):
            if k < text_len:
                matrix[i][j] = text[k]
                k += 1

    # Read column-wise based on order
    cipher = ""
    for num in range(key_len):
        for j in range(key_len):
            if order[j] == num:
                for i in range(rows):
                    cipher += matrix[i][j]

    with open("Cipher.txt", "w") as f:
        f.write(cipher)

    print("Encryption Completed! Output stored in Cipher.txt")


# ---------------- DECRYPTION ----------------
def decrypt():
    try:
        with open("Cipher.txt", "r") as f:
            cipher = f.read()
    except:
        print("File Error!")
        return

    key = input("Enter Key (Word or Sentence): ")
    key = process_key(key)

    key_len = len(key)
    cipher_len = len(cipher)
    order = get_key_order(key)

    rows = cipher_len // key_len

    matrix = [['' for _ in range(key_len)] for _ in range(rows)]

    k = 0
    for num in range(key_len):
        for j in range(key_len):
            if order[j] == num:
                for i in range(rows):
                    matrix[i][j] = cipher[k]
                    k += 1

    plain = ""
    for i in range(rows):
        for j in range(key_len):
            plain += matrix[i][j]

    with open("Recover.txt", "w") as f:
        f.write(plain.rstrip('X'))  # remove padding

    print("Decryption Completed! Output stored in Recover.txt")


# ---------------- MAIN MENU ----------------
while True:
    print("\n===== Columnar Transposition Cipher =====")
    print("1. Encryption")
    print("2. Decryption")
    print("3. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        encrypt()
    elif choice == "2":
        decrypt()
    elif choice == "3":
        print("Exiting...")
        break
    else:
        print("Invalid Choice!")









Input: File - Large Plaintext (file.txt), Key Value (Word or Sentence)
Output: File - Encoded Text (Cipher.txt)
Input File Name: Plaintext.txt
Encrypted File Name: Cipher.txt
Decrypted File Name: Recover.txt