import socket

# =================== STEGO FUNCTIONS ===================
def to_binary(data):
    return ''.join(format(ord(char), '08b') for char in data)

def from_binary(binary_str):
    chars = [chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8)]
    return ''.join(chars)

def encode_hidden_data(word, placeholder, hidden_data):
    binary_data = to_binary(hidden_data)
    zwc = ['\u200b', '\u200c']  # 0 -> Zero Width Space, 1 -> Zero Width Non-Joiner
    zwc_data = ''.join([zwc[int(b)] for b in binary_data])

    result = ''
    inserted = False

    for char in word:
        result += char
        if char == placeholder and not inserted:
            result += zwc_data
            inserted = True

    return result

def auto_decode_hidden_data(encoded_text):
    zwc_to_binary = {
        '\u200b': '0',
        '\u200c': '1'
    }

    for i, char in enumerate(encoded_text):
        hidden_data = ''
        j = i + 1

        # Check if zero width characters follow
        while j < len(encoded_text) and encoded_text[j] in zwc_to_binary:
            hidden_data += zwc_to_binary[encoded_text[j]]
            j += 1

        if hidden_data:
            decoded = from_binary(hidden_data)
            print(f"\n✅ Extracted hidden data near '{char}': {decoded}")
            return decoded

    print("\n❌ No hidden data found!")
    return None

# =================== CLIENT SOCKET ===================
HOST = '127.0.0.1'
PORT = 65432

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print(f"[+] Connected to server at {HOST}:{PORT}")

# ========== USER INPUT ==========
word = input("📝 Enter the text you want to hide data inside (ex: Hello World): ")
placeholder = input("🔑 Enter the placeholder letter that will carry the hidden data (ex: o): ")

if placeholder not in word:
    print(f"⚠️ Placeholder '{placeholder}' not found in the word!")
    client_socket.close()
    exit()

hidden_text = input("🔐 Enter the secret message you want to hide: ")

# ========== ENCODE AND SEND ==========
stego_word = encode_hidden_data(word, placeholder, hidden_text)

print("\n✅ Stego text ready to send:")
print(stego_word)

client_socket.sendall(stego_word.encode())
print("[+] Data sent to server!")

# ========== ASK USER IF HE WANTS TO DECODE ==========
decode_choice = input("👉 Do you want to decode the message you just sent? (y/n): ")

if decode_choice.lower() == 'y':
    auto_decode_hidden_data(stego_word)

client_socket.close()
