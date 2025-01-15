import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import os

# Encode a message into an image
def encode_message(image_path, message, output_path):
    image = Image.open(image_path)
    encoded = image.copy()
    width, height = image.size
    message += "~~~"  # Delimiter to indicate the end of the message
    binary_message = ''.join([format(ord(char), '08b') for char in message])
    
    data_index = 0
    for x in range(width):
        for y in range(height):
            if data_index < len(binary_message):
                pixel = list(image.getpixel((x, y)))
                for i in range(3):
                    if data_index < len(binary_message):
                        pixel[i] = (pixel[i] & ~1) | int(binary_message[data_index])
                        data_index += 1
                encoded.putpixel((x, y), tuple(pixel))
            else:
                break
    
    encoded.save(output_path)
    messagebox.showinfo("Success", f"Message encoded and saved to {output_path}")

# Decode a message from an image
def decode_message(image_path):
    image = Image.open(image_path)
    width, height = image.size
    binary_message = ""

    for x in range(width):
        for y in range(height):
            pixel = image.getpixel((x, y))
            for i in range(3):
                binary_message += str(pixel[i] & 1)

    all_bytes = [binary_message[i:i+8] for i in range(0, len(binary_message), 8)]
    decoded_message = "".join([chr(int(byte, 2)) for byte in all_bytes if int(byte, 2) != 0])
    
    if "~~~" in decoded_message:
        return decoded_message.split("~~~")[0]
    return "No hidden message found!"

# GUI application
def main():
    def load_image():
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.bmp;*.jpg;*.jpeg;*.tiff")])
        if file_path:
            img = Image.open(file_path)
            img.thumbnail((300, 300))
            img = ImageTk.PhotoImage(img)
            image_label.configure(image=img)
            image_label.image = img
            app.image_path = file_path
            status_label.config(text=f"Loaded: {os.path.basename(file_path)}")

    def encode():
        if not hasattr(app, 'image_path'):
            messagebox.showerror("Error", "No image loaded!")
            return
        message = message_entry.get()
        if not message:
            messagebox.showerror("Error", "No message entered!")
            return
        output_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG Image", "*.png")])
        if output_path:
            encode_message(app.image_path, message, output_path)

    def decode():
        if not hasattr(app, 'image_path'):
            messagebox.showerror("Error", "No image loaded!")
            return
        decoded_message = decode_message(app.image_path)
        messagebox.showinfo("Decoded Message", decoded_message)

    # Create main window
    app = tk.Tk()
    app.title("Image Steganography")

    # UI components
    load_button = tk.Button(app, text="Load Image", command=load_image)
    load_button.pack(pady=5)

    image_label = tk.Label(app)
    image_label.pack(pady=5)

    message_label = tk.Label(app, text="Enter Message to Encode:")
    message_label.pack(pady=5)

    message_entry = tk.Entry(app, width=40)
    message_entry.pack(pady=5)

    encode_button = tk.Button(app, text="Encode Message", command=encode)
    encode_button.pack(pady=5)

    decode_button = tk.Button(app, text="Decode Message", command=decode)
    decode_button.pack(pady=5)

    status_label = tk.Label(app, text="", fg="green")
    status_label.pack(pady=5)

    # Run the application
    app.mainloop()

if __name__ == "__main__":
    main()
