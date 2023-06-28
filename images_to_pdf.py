import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from reportlab.lib.pagesizes import landscape
from reportlab.pdfgen import canvas

class ImageToPDFConverter:
    def __init__(self, root):
        self.root = root
        self.image_paths = []
        self.root.title("Image to PDF Converter")
        self.root.geometry("750x600")
        self.select_images_button = tk.Button(self.root, text="Select Images", command=self.select_images, font=("Helvetica", 12),)
        self.select_images_button.pack(pady=10)
        self.convert_to_pdf_button = tk.Button(self.root, text="Convert to PDF", command=self.convert_to_pdf,font=("Helvetica", 12),)
        self.convert_to_pdf_button.pack(pady=10)
        self.select_images_label = tk.Label(self.root, text="Select Images", font=("Helvetica", 14))
        self.select_images_label.pack(pady=10)
        self.preview_frame = tk.Frame(self.root, width=380, height=200)
        self.preview_frame.pack(pady=10)

    def select_images(self):
        self.image_paths = filedialog.askopenfilenames(initialdir="/", title="Select Images", filetypes=(("Image Files", "*.jpg *.png"),))
        self.preview_frame.destroy()
        self.preview_frame = tk.Frame(self.root, width=380, height=200)
        self.preview_frame.pack(pady=10)

        for i, image_path in enumerate(self.image_paths):
            image = Image.open(image_path)
            image = self.resize_image(image, width=150, height=150)
            photo = ImageTk.PhotoImage(image)
            label = tk.Label(self.preview_frame, image=photo)
            label.image = photo
            label.grid(row=i // 3, column=i % 3, padx=10, pady=10)

    def resize_image(self, image, width, height):
        aspect_ratio = min(width / float(image.size[0]), height / float(image.size[1]))
        new_width = int(aspect_ratio * image.size[0])
        new_height = int(aspect_ratio * image.size[1])
        resized_image = image.resize((new_width, new_height), resample=Image.Resampling.BILINEAR)
        return resized_image

    def convert_to_pdf(self):
        pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=(("PDF Files", "*.pdf"),))
        c = canvas.Canvas(pdf_path, pagesize=landscape)
        for image_path in self.image_paths:
            image = Image.open(image_path)
            width, height = image.size
            c.setPageSize((width, height))
            c.drawImage(image_path, 0, 0, width=width, height=height)
            c.showPage()
        c.save()
        messagebox.showinfo("Conversion Successful", f"PDF saved at {pdf_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageToPDFConverter(root)
    root.mainloop()
