def rail_fence_encrypt(text, depth):
    if depth == 1 or depth >= len(text):
        return text

    rails = ['' for _ in range(depth)]
    row = 0
    direction = 1

    for char in text:
        rails[row] += char
        row += direction

        if row == 0 or row == depth - 1:
            direction *= -1

    return ''.join(rails)


def rail_fence_decrypt(cipher, depth):
    if depth == 1 or depth >= len(cipher):
        return cipher

    # Step 1: Create zigzag pattern
    pattern = [0] * len(cipher)
    row = 0
    direction = 1

    for i in range(len(cipher)):
        pattern[i] = row
        row += direction

        if row == 0 or row == depth - 1:
            direction *= -1

    # Step 2: Count letters per rail
    rail_counts = [pattern.count(r) for r in range(depth)]

    # Step 3: Divide cipher into rails
    rails = []
    index = 0
    for count in rail_counts:
        rails.append(list(cipher[index:index + count]))
        index += count

    # Step 4: Reconstruct original text
    result = []
    rail_indices = [0] * depth

    for r in pattern:
        result.append(rails[r][rail_indices[r]])
        rail_indices[r] += 1

    return ''.join(result)


# ---------------- MAIN ----------------
if __name__ == "__main__":
    choice = ''

    while choice != '0':
        print("\n1. Encryption")
        print("2. Decryption")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            depth = int(input("Enter key depth: "))

            with open('plaintext.txt', 'r') as file:
                plain_text = file.read()

            plain_text = plain_text.replace(" ", "").strip()

            cipher = rail_fence_encrypt(plain_text, depth)

            with open('ciphertext.txt', 'w') as file:
                file.write(cipher)

            print("\nPlain Text :", plain_text)
            print("Cipher Text:", cipher)
            print("Cipher saved to ciphertext.txt")

        elif choice == '2':
            depth = int(input("Enter key depth: "))

            with open('ciphertext.txt', 'r') as file:
                cipher_text = file.read().strip()

            decrypted_text = rail_fence_decrypt(cipher_text, depth)

            print("\nCipher Text :", cipher_text)
            print("Decrypted Text:", decrypted_text)

        elif choice == '0':
            print("Exiting program")

        else:
            print("Invalid choice. Try again.")











Input: File - Large Plaintext (file.txt), Key Value
Output: File - Encoded Text (Cipher.txt)
Input File Name: Plaintext.txt
Encrypted File Name: Cipher.txt
Decrypted File Name: Recover.txt