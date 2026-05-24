# Hidden-code
# 🕵️‍♂️ Steganography Tool 🛠️

A Python-based GUI application built with `tkinter` that allows you to hide and extract secret data within standard text, CSV, and SVG files. This tool uses various steganography techniques to ensure your hidden messages remain undetected.

## ✨ Features

* **📝 Text Steganography:** Hides secret messages within plain text using Zero-Width Characters (ZWC). The hidden text is completely invisible to the human eye!
* **📄 CSV Steganography:** Embeds base64-encoded secret data into the first line of a CSV file as a hidden comment, preserving the integrity of the tabular data.
* **🖼️ SVG Steganography:** Hides base64-encoded data inside the `<metadata>` tag of an SVG vector image without affecting the visual rendering of the image.
* **🖥️ User-Friendly GUI:** A clean and simple interface using Tkinter, making it easy to encode and decode messages with just a few clicks.

## 🚀 Prerequisites

* Python 3.x
* `tkinter` (Usually comes pre-installed with standard Python distributions)

## 🛠️ Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/yourusername/steganography-tool.git
    ```
2.  Navigate to the project directory:
    ```bash
    cd steganography-tool
    ```
3.  Run the application:
    ```bash
    python steganography_tool.py
    ```

## 📖 How to Use

### 1. Hide/Extract Text Data (ZWC)
* **Hide:** Enter a normal word, choose a specific placeholder letter (must exist in the word), and enter your secret text. Click **Hide Text** to generate the text with invisible data.
* **Extract:** Paste the encoded text, specify the placeholder letter used during encoding, and click **Extract Text** to reveal the secret.

### 2. Hide/Extract in CSV
* **Hide:** Enter your secret text, click **Hide in CSV**, and save the generated file.
* **Extract:** Click **Extract from CSV**, select the steganographic CSV file, and view the hidden message.

### 3. Hide/Extract in SVG
* **Hide:** Enter your text, click **Hide in SVG**, and save the `.svg` file. 
* **Extract:** Click **Extract from SVG**, select your modified SVG image, and the hidden data will be decoded and displayed.

## 🤝 Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## 📜 License
[MIT](https://choosealicense.com/licenses/mit/)
