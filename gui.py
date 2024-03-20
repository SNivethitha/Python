import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import pytesseract
import pyperclip

# Set the path to Tesseract executable (change this to your installation path)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Global variables for cropping
original_image = None

def extract_text_from_image(image, lang='eng'):
    try:
        text = pytesseract.image_to_string(image, lang=lang)
        return text
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {str(e)}")
def open_file_dialog():
    global original_image, text_box
    filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg")])
    if filename:
        original_image = cv2.imread(filename)
        select_roi()

def display_image(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = cv2.resize(img, (400, 400))
    img = Image.fromarray(img)
    img = ImageTk.PhotoImage(img)
    image_label.config(image=img)
    image_label.image = img  # Keep a reference to prevent garbage collection

def select_roi():
    global original_image, text_box
    if original_image is not None:
        roi = cv2.selectROI("Select ROI", original_image, fromCenter=False, showCrosshair=True)
        if all(roi):
            x, y, w, h = roi
            cropped_img = original_image[y:y+h, x:x+w]
            display_image(cropped_img)
            lang = 'eng'  # Default language
            text = extract_text_from_image(cropped_img, lang=lang)
            if text:
                text_box.delete(1.0, tk.END)  # Clear previous text
                text_box.insert(tk.END, text)  # Insert extracted text
                pyperclip.copy(text)  # Copy text to clipboard
        cv2.destroyWindow("Select ROI")

# Create the Tkinter window
root = tk.Tk()
root.title("Text Extractor")

# Create GUI components
open_button = tk.Button(root, text="Open Image", command=open_file_dialog)
open_button.pack(pady=10)

image_label = tk.Label(root)
image_label.pack()

# Create a Text widget to display extracted text
text_box = tk.Text(root, height=15, width=60)
text_box.pack(pady=10)

root.mainloop()
