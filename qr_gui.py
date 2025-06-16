import tkinter as tk 
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import data_masking 
from pathlib import Path
from powerpoint import QRStepSlideshow, load_slides_formatINFO # change

'''
In this file the relevant files are imported to put everything together
both the actual qr and the powerpoint are imported
and the GUI is completed and presented
This is the file that you need to run to be able to run the code
'''


def generate_qr_image(qr_matrix):
    qr_numeric = np.array([[0 if cell == 'B' else 1 for cell in row] for row in qr_matrix])
    qr_with_quiet = np.pad(qr_numeric, pad_width=4, mode='constant', constant_values=1)  # This is the 4-module quiet zone
    return qr_with_quiet


def display_qr_in_gui(qr_array, frame):
    # clear anything that may still be on the frame when calling it
    for widget in frame.winfo_children():
        widget.destroy()

    # create the matplotlib figure to display in the GUI
    fig, ax = plt.subplots(figsize=(5, 5), dpi=100)
    # draws QR image
    ax.imshow(qr_array, cmap='grey', interpolation='none')  # 'none' ensures that the scanning process is not affected
    # ensure that the block where QR displayed is clear and clean
    ax.axis('off')
    fig.tight_layout(pad=0)

    # Matplotlib is embedded into Tkinter GUI
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # ensures that the code finishes running when the window is closed
    plt.close(fig)


def generate_and_display_qr(text, version, display_frame):
    # These are a series of warnings to catch any incorrect input fro users, like:
    
    # requiring text for the QR and input on the version or no version preferred
    if not text and not version:
        messagebox.showwarning("Input is needed", "Please enter text or a URL and the QR version")
        return

    # requiring that text is entered and not numbers
    if not text:
        messagebox.showwarning("Input is needed", "Please enter text or a URL for the QR code")
        return
    
    # ensuring only required data is entered for version and that version is not empty
    if not version or version not in ["v1", "v2", "no"]:
        messagebox.showwarning("Version input is needed", "Please enter 'v1', 'v2' or 'no' for the QR version")
        return

    #If anything goes wrong the error is caught and shown in terminal and in gui as a message box
    try:
        # the qr is created and returned via the previous file data_masking where text for qr and version is entered through parameters'
        # an image is generated through the qr created and that image is displayed in the GUI
        qr_matrix = data_masking.finishedQR(qr_enter=text, v1_enter=version)
        qr_array = generate_qr_image(qr_matrix)
        display_qr_in_gui(qr_array, display_frame)
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        messagebox.showerror("Error", f"QR Code Generation not successful:\n{str(e)}")



def launch_slideshow():
    # This function launches the slideshow
    # It uses the tkinter library to create a new window
    # A check is made to ensure that the markdown file for the powerpoint exists
    if not Path("katieResearch.md").exists():
        messagebox.showerror("File Missing", "The file 'katieResearch.md' was not found in the directory")
        return

    #a window is made and size is given for the powerpoint and the powerpoint is displayed
    slides = load_slides_formatINFO("katieResearch.md")
    root = tk.Toplevel()
    root.geometry("700x700")
    QRStepSlideshow(root, slides)
    root.mainloop()



def main():
    # This function creates the main GUI window
    root = tk.Tk()
    root.title("Functional QR Code Generator")  # Title of the GUI window

    # Text instructing the user what to do to create a qr code
    tk.Label(root, text="Enter plain text or a URL for the QR code:", font=('Helvetica', 10, 'bold')).pack(pady=(80, 5))
    input_entry = tk.Entry(root, width=50)
    input_entry.pack(pady=5)

    # Text labeling and showing the user where to enter information for the preferred version for the qr code
    tk.Label(root, text="QR version (v1, v2 or 'no' for automatic selection of version based on amount of input):", font=('Helvetica', 10, 'bold')).pack()
    version_entry = tk.Entry(root, width=10)
    version_entry.pack(pady=5)

    # This is the QR Display Area
    display_frame = tk.Frame(root)
    display_frame.pack(pady=10)

    # This button will generate the QR code
    tk.Button(
        text="Generate QR Code",
        font=('Helvetica', 10, 'bold'),
        command=lambda: generate_and_display_qr(input_entry.get(), version_entry.get(), display_frame)
    ).pack(pady=(10, 30))  # Provides spacing between the button and the QR code

    # This button opens the QR code step-by-step slideshow
    tk.Button(
        text="Open Slideshow",
        font=('Helvetica', 10, 'bold'),
        command=launch_slideshow
    ).pack(pady=(10, 30))

    # Label warning the user about the risks of QR Code scanning
    tk.Label(
        root,
        text="⚠️QR codes can lead to content that is not safe. Scan QR codes with caution⚠️",
        font=('Helvetica', 10, 'bold'),
        fg="red",
        wraplength=400,
        justify="center"
    ).pack(pady=10)

    root.mainloop()


if __name__ == "__main__":
    main()