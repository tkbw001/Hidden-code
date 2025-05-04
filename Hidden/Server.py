import socket

def auto_decode_hidden_data(encoded_text):
    zwc_to_binary = {
        '\u200b': '0',
        '\u200c': '1'
    }

    for i, char in enumerate(encoded_text):
        hidden_data = ''
        j = i + 1

        while j < len(encoded_text) and encoded_text[j] in zwc_to_binary:
            hidden_data += zwc_to_binary[encoded_text[j]]
            j += 1

        if hidden_data:
            decoded = from_binary(hidden_data)
            print(f"\n✅ Extracted hidden data near '{char}': {decoded}")
            return decoded

    print("\n❌ No hidden data found!")
    return None

def from_binary(binary_str):
    chars = [chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8)]
    return ''.join(chars)

HOST = '127.0.0.1'
PORT = 65432

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

print(f"[+] Server listening on {HOST}:{PORT}")

conn, addr = server_socket.accept()
print(f"[+] Connected by {addr}")

while True:
    data = conn.recv(4096)
    if not data:
        break

    stego_text = data.decode()
    print(f"[+] Received stego data: {stego_text}")

    # Decode automatically
    auto_decode_hidden_data(stego_text)

conn.close()
