import socket
import random
import time

# Check prime
def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

# Generate random prime
def generate_prime():
    while True:
        p = random.randint(10000, 99999)
        if is_prime(p):
            return p

def start_server():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()

        print("Server is listening...\n")

        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")

            # Step 1: Receive request
            request = conn.recv(1024).decode()
            if request:
                print("1. Request accepted from client")

            # Step 2: Generate P and G
            P = generate_prime()
            G = random.randint(2, P - 2)

            print(f"2. Generated P: {P}, G: {G}")

            # Step 3: Send P and G
            conn.sendall(f"{P}|{G}".encode())
            print("3. Sent P and G to client")

            # Step 4: Receive R1 from client
            r1_data = conn.recv(1024).decode()
            R1 = int(r1_data)
            print(f"4. Received R1: {R1}")

            # Step 5: Generate private Y and R2
            Y = random.randint(1, P - 1)
            R2 = pow(G, Y, P)

            print(f"5. Private Y: {Y}, Calculated R2: {R2}")

            # Step 6: Send R2
            conn.sendall(str(R2).encode())
            print("6. Sent R2 to client")

            # Step 7: Compute shared key
            secret_key = pow(R1, Y, P)
            print(f"7. Symmetric Key (Server): {secret_key}")


if __name__ == "__main__":
    start_server()





import socket
import random

def start_client():
    host = '127.0.0.1'
    port = 65432

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))

        # Step 1: Request key exchange
        s.sendall(b"KEY_EXCHANGE_REQUEST")
        print("1. Sent request for key exchange to the server")

        # Step 2: Receive P and G
        pg_data = s.recv(1024).decode()
        P_str, G_str = pg_data.split('|')
        P, G = int(P_str), int(G_str)

        print(f"2. Received Prime P: {P}, Generator G: {G}")

        # Step 3: Generate private key and compute R1
        X = random.randint(1, P - 1)
        R1 = pow(G, X, P)

        print(f"3. Private X: {X}, Calculated R1: {R1}")

        # Step 4: Send R1 to server
        s.sendall(str(R1).encode())
        print("4. Sent R1 to server")

        # Step 5: Receive R2
        r2_data = s.recv(1024).decode()
        R2 = int(r2_data)

        print(f"5. Received R2: {R2}")

        # Step 6: Compute shared secret key
        secret_key = pow(R2, X, P)
        print(f"6. Symmetric Key (Client): {secret_key}")


if __name__ == "__main__":
    start_client()