import tkinter as tk
from pathlib import Path
from tkinter import font
from PIL import Image, ImageTk
import re

# loads the content from the markdown file and ensures that the file is found and catches any errors that may be there
def load_slides_formatINFO(file_name):
    try:
        with open(file_name, "r") as f:
            content = f.read()
            # Ensures file is not empty
            assert content.strip() != "", "Markdown file is empty or unreadable"
    except FileNotFoundError:
        raise FileNotFoundError(f"The file '{file_name}' was not found.")
    except Exception as e:
        raise RuntimeError(f"Failed to read '{file_name}': {e}")

    # Split content into slides based on headers and length
    slides = []
    current_slide = ""
    max_chars = 1200

    # Separates slides based on markdown into different important sections
    for line in content.splitlines():
        if line.startswith("# "):  # Major section
            if current_slide:
                slides.append(current_slide.strip())
            current_slide = line + "\n"
        elif line.startswith("### ") and not line.startswith("####"):
            if current_slide:
                slides.append(current_slide.strip())
            current_slide = line + "\n"
        else:
            current_slide += line + "\n"

    if current_slide:
        slides.append(current_slide.strip())

    # Break up overly long slides further
    final_slides = []
    for slide in slides:
        if len(slide) <= max_chars:
            final_slides.append(slide)
        else:
            paragraphs = slide.split("\n\n")
            temp = ""
            for para in paragraphs:
                if len(temp) + len(para) + 2 <= max_chars:
                    temp += para + "\n\n"
                else:
                    final_slides.append(temp.strip())
                    temp = para + "\n\n"
            if temp.strip():
                assert len(temp.strip()) <= max_chars, "Slide characters exceeds maximum length"
                final_slides.append(temp.strip())
    assert all(slide.strip() for slide in final_slides), "One or more slides are empty"
    
    return slides

# GUI of powerpoint
class QRStepSlideshow:
    def __init__(self, root, slides):
        self.root = root
        self.root.title("QR Code Research Slideshow")
        self.slides = slides
        self.index = 0
        self.image_refs = []

        # configures markdown to HTML elements for better readability
        self.text = tk.Text(root, wrap=tk.WORD, font=("Helvetica", 14), padx=20, pady=20)
        self.text.tag_configure("h1", font=("Helvetica", 28, "bold"))
        self.text.tag_configure("h2", font=("Helvetica", 24, "bold"))
        self.text.tag_configure("h3", font=("Helvetica", 20, "bold"))
        self.text.tag_configure("h4", font=("Helvetica", 16, "bold"))
        self.text.tag_configure("h5", font=("Helvetica", 14, "bold"))
        self.text.tag_configure("body", font=("Helvetica", 13))
        self.text.tag_configure("bold", font=("Helvetica", 13, "bold"))
        self.text.pack(expand=True, fill=tk.BOTH)

        # the buttons are created for user navigation in the powerpoint
        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.prev_btn = tk.Button(button_frame, text="Previous", command=self.prev_slide, width=10)
        self.prev_btn.grid(row=0, column=0, padx=10)

        self.next_btn = tk.Button(button_frame, text="Next", command=self.next_slide, width=10)
        self.next_btn.grid(row=0, column=1, padx=10)

        self.show_slide()
        self.update_buttons()

    def show_slide(self):
        self.text.config(state=tk.NORMAL)
        self.text.delete("1.0", tk.END)
        self.image_refs.clear()  # clear old image refs

        lines = self.slides[self.index].splitlines()

        for line in lines:
            tag = "body"
            text = line + "\n"

            # Header detection
            if line.startswith("###### "):
                tag = "h5"
                text = line[7:] + "\n"
            elif line.startswith("##### "):
                tag = "h5"
                text = line[6:] + "\n"
            elif line.startswith("#### "):
                tag = "h4"
                text = line[5:] + "\n"
            elif line.startswith("### "):
                tag = "h3"
                text = line[4:] + "\n"
            elif line.startswith("## "):
                tag = "h3"
                text = line[3:] + "\n"
            elif line.startswith("# "):
                tag = "h1"
                text = line[2:] + "\n"

            # checks for markdown style of image implementation to convert it
            elif line.strip().startswith("![](") and line.strip().endswith(")"):
                image_path = line.strip()[4:-1].strip()
                if Path(image_path).exists():
                    try:
                        img = Image.open(image_path)
                        img = img.resize((200, 200), Image.LANCZOS) 
                        tk_img = ImageTk.PhotoImage(img)
                        self.image_refs.append(tk_img)
                        self.text.image_create(tk.END, image=tk_img)
                        self.text.insert(tk.END, "\n\n")
                    except Exception as e:
                        self.text.insert(tk.END, f"[Image load error: {e}]\n", "body")
            
            # checks for HTML style of image implementation to convert it
            else:
                img_tag_match = re.search(r'<img\s+[^>]*src="([^"]+)"', line)
                if img_tag_match:
                    image_path = img_tag_match.group(1)
                    if Path(image_path).exists():
                        try:
                            img = Image.open(image_path)
                            img = img.resize((400, 400), Image.LANCZOS)
                            tk_img = ImageTk.PhotoImage(img)
                            self.image_refs.append(tk_img)
                            self.text.image_create(tk.END, image=tk_img)
                            self.text.insert(tk.END, "\n\n")
                            continue
                        except Exception as e:
                            self.text.insert(tk.END, f"[Image load error: {e}]\n")
                            continue

            # Normal text
            start = self.text.index(tk.INSERT)
            self.text.insert(tk.END, text)
            end = self.text.index(tk.INSERT)
            self.text.tag_add(tag, start, end)

            # Bold text using **bold**
            i = start
            while True:
                start_bold = self.text.search(r"\*\*", i, stopindex=end, regexp=True)
                if not start_bold:
                    break
                end_bold = self.text.search(r"\*\*", f"{start_bold}+2c", stopindex=end, regexp=True)
                if not end_bold:
                    break
                self.text.delete(end_bold, f"{end_bold}+2c")
                self.text.delete(start_bold, f"{start_bold}+2c")
                self.text.tag_add("bold", start_bold, end_bold)
                i = end_bold

        self.text.config(state=tk.DISABLED)

    # functions to increment or decrement index and call show_slide when navigation button is clicked
    def next_slide(self):
        if self.index < len(self.slides) - 1:
            self.index += 1
            self.show_slide()
            self.update_buttons()

    def prev_slide(self):
        if self.index > 0:
            self.index -= 1
            self.show_slide()
            self.update_buttons()

    # buttons are updated based on slide index to enable or disable buttons like at the starting or finishing slide
    def update_buttons(self):
        assert 0 <= self.index < len(self.slides), f"Current slide index {self.index} out of range"
        self.prev_btn.config(state=tk.NORMAL if self.index > 0 else tk.DISABLED)
        self.next_btn.config(state=tk.NORMAL if self.index < len(self.slides) - 1 else tk.DISABLED)


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    final_slides = load_slides_formatINFO("katieResearch.md")
    app = QRStepSlideshow(root, final_slides)
    root.mainloop()
