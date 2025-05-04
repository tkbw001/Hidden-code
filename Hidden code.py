import base64
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# ============== TEXT STEGANOGRAPHY ==============

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

def decode_hidden_data(encoded_text, placeholder):
    zwc_to_binary = {
        '\u200b': '0',
        '\u200c': '1'
    }
    for i, char in enumerate(encoded_text):
        if char == placeholder:
            hidden_data = ''
            j = i + 1

            # التجميع من بعد placeholder لكل الحروف المخفية
            while j < len(encoded_text) and encoded_text[j] in zwc_to_binary:
                hidden_data += zwc_to_binary[encoded_text[j]]
                j += 1

            # ديباجية
            print(f"[Debug] Binary hidden data: {hidden_data}")

            if hidden_data:
                decoded = from_binary(hidden_data)
                print(f"[Debug] Decoded hidden data: {decoded}")
                return decoded
            else:
                print("[Debug] No zero-width characters found after placeholder!")

    return None

def extract_data_from_csv(csv_path):
    with open(csv_path, 'r', encoding="utf-8") as file:
        first_line = file.readline()  # قراءة أول سطر فقط
        match = re.search(r"# Hidden Data: (.+)", first_line)  # البحث عن البيانات المخفية
        if match:
            decoded_data = base64.b64decode(match.group(1)).decode()
            print(f"🔓 Extracted hidden data: {decoded_data}")
        else:
            print("❌ No hidden data found!")

def hide_data_in_svg(data, output_svg):
    encoded_data = base64.b64encode(data.encode()).decode()  # تشفير البيانات
    svg_template = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
        <text x="50" y="100" font-size="30" fill="black">🔒</text>
        <metadata>{encoded_data}</metadata>  <!-- تخزين البيانات المخفية -->
    </svg>
    '''
    with open(output_svg, 'w') as file:
        file.write(svg_template)

    print(f"✅ Data hidden in {output_svg}")

import re

def extract_data_from_svg(svg_path):
    with open(svg_path, 'r', encoding="utf-8") as file:
        content = file.read()
    
    match = re.search(r'<metadata>(.*?)</metadata>', content, re.DOTALL)
    if match:
        decoded_data = base64.b64decode(match.group(1)).decode()
        print(f"🔓 Extracted hidden data: {decoded_data}")
    else:
        print("❌ No hidden data found!")


# ============== GUI =====================

def hide_text_action():
    word = word_entry.get()
    placeholder = placeholder_entry.get()
    hidden_text = hidden_text_entry.get()

    if not word or not placeholder or not hidden_text:
        messagebox.showwarning("Warning", "⚠️ Please fill in all fields!")
        return

    if placeholder not in word:
        messagebox.showwarning("Warning", f"⚠️ Placeholder '{placeholder}' not found in word!")
        return

    stego_word = encode_hidden_data(word, placeholder, hidden_text)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, stego_word)

def extract_text_action():
    encoded_text = encoded_text_entry.get()
    placeholder = placeholder_extract_entry.get()

    if not encoded_text or not placeholder:
        messagebox.showwarning("Warning", "⚠️ Please fill in all fields!")
        return

    extracted_data = decode_hidden_data(encoded_text, placeholder)

    if extracted_data:
        messagebox.showinfo("Extracted Data", f"✅ Extracted hidden data: {extracted_data}")
    else:
        messagebox.showerror("No Data", "❌ No hidden data found!")

# ============== CSV FUNCTIONS ==============

def hide_data_in_csv():
    data = csv_text_entry.get()
    if not data:
        messagebox.showwarning("⚠️ Warning", "Please enter the text to hide!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    encoded_data = base64.b64encode(data.encode()).decode()
    
    try:
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(f"# Hidden Data: {encoded_data}\n")
            file.write("Name, Age, Country\nAli, 25, Egypt\n")

        messagebox.showinfo("✅ Success", f"Data hidden successfully in: {file_path}")

    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to hide data: {e}")

def extract_data_from_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if not file_path:
        return

    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            first_line = file.readline()
            match = re.search(r"# Hidden Data: (.+)", first_line)
            if match:
                decoded_data = base64.b64decode(match.group(1)).decode()
                messagebox.showinfo("🔓 Extracted Data", f"Hidden Data: {decoded_data}")
            else:
                messagebox.showerror("❌ Error", "No hidden data found!")

    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to extract data: {e}")

# ============== SVG FUNCTIONS ==============

def hide_data_in_svg():
    data = svg_text_entry.get()
    if not data:
        messagebox.showwarning("⚠️ Warning", "Please enter the text to hide!")
        return

    file_path = filedialog.asksaveasfilename(defaultextension=".svg", filetypes=[("SVG Files", "*.svg")])
    if not file_path:
        return

    encoded_data = base64.b64encode(data.encode()).decode()
    svg_template = f'''
    <svg xmlns="http://www.w3.org/2000/svg" width="200" height="200">
        <text x="50" y="100" font-size="30" fill="black">🔒</text>
        <metadata>{encoded_data}</metadata>
    </svg>
    '''
    
    try:
        with open(file_path, 'w', encoding="utf-8") as file:
            file.write(svg_template)

        messagebox.showinfo("✅ Success", f"Data hidden successfully in: {file_path}")

    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to hide data: {e}")

def extract_data_from_svg():
    file_path = filedialog.askopenfilename(filetypes=[("SVG Files", "*.svg")])
    if not file_path:
        return

    try:
        with open(file_path, 'r', encoding="utf-8") as file:
            content = file.read()
        
        match = re.search(r'<metadata>(.*?)</metadata>', content, re.DOTALL)
        if match:
            decoded_data = base64.b64decode(match.group(1)).decode()
            messagebox.showinfo("🔓 Extracted Data", f"Hidden Data: {decoded_data}")
        else:
            messagebox.showerror("❌ Error", "No hidden data found!")

    except Exception as e:
        messagebox.showerror("❌ Error", f"Failed to extract data: {e}")


# ============== GUI WINDOW ==============

root = tk.Tk()
root.title("🕵️‍♂️ Steganography Tool 🛠️")
root.geometry("600x600")

# Hide Text Section
tk.Label(root, text="📝 Hide Text Data", font=('Arial', 12, 'bold')).pack()

tk.Label(root, text="Word:").pack()
word_entry = tk.Entry(root, width=50)
word_entry.pack()

tk.Label(root, text="Placeholder Letter:").pack()
placeholder_entry = tk.Entry(root, width=50)
placeholder_entry.pack()

tk.Label(root, text="Hidden Text Data:").pack()
hidden_text_entry = tk.Entry(root, width=50)
hidden_text_entry.pack()

tk.Button(root, text="Hide Text", command=hide_text_action).pack(pady=5)

result_text = tk.Text(root, height=4, width=60)
result_text.pack(pady=5)

# Extract Text Section
tk.Label(root, text="🔍 Extract Hidden Text", font=('Arial', 12, 'bold')).pack()

tk.Label(root, text="Encoded Text:").pack()
encoded_text_entry = tk.Entry(root, width=50)
encoded_text_entry.pack()

tk.Label(root, text="Placeholder Letter:").pack()
placeholder_extract_entry = tk.Entry(root, width=50)
placeholder_extract_entry.pack()

tk.Button(root, text="Extract Text", command=extract_text_action).pack(pady=5)

root = tk.Tk()
root.title("🕵️‍♂️ Steganography Tool")
root.geometry("400x400")

# CSV Section
tk.Label(root, text="📄 Hide Data in CSV", font=('Arial', 12, 'bold')).pack(pady=5)
csv_text_entry = tk.Entry(root, width=50)
csv_text_entry.pack(pady=5)
tk.Button(root, text="💾 Hide in CSV", command=hide_data_in_csv).pack(pady=5)
tk.Button(root, text="🔍 Extract from CSV", command=extract_data_from_csv).pack(pady=5)

# SVG Section
tk.Label(root, text="🖼️ Hide Data in SVG", font=('Arial', 12, 'bold')).pack(pady=10)
svg_text_entry = tk.Entry(root, width=50)
svg_text_entry.pack(pady=5)
tk.Button(root, text="💾 Hide in SVG", command=hide_data_in_svg).pack(pady=5)
tk.Button(root, text="🔍 Extract from SVG", command=extract_data_from_svg).pack(pady=5)

root.mainloop()
