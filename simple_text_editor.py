"""
Simple Text Editor
------------------
A simple text editor built using Python's Tkinter library.

Imports:
- tkinter as tk → GUI library (buttons, text, menus…).
- askopenfilename → Open File dialog (choose file).
- asksaveasfilename → Save As dialog (choose path/name to save).
- showerror → Show error popup.
- askyesno → Yes/No popup dialog (confirmation).
- os → Handle file paths (get file name from path).

Features:
- Open text files
- Save / Save As
- Scrollable text area
- Menu bar with keyboard shortcuts
- Warns on unsaved changes before exit
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror, askyesno
import os

# ------------------------------
# Global variable to track file
# ------------------------------
current_file = None

# ------------------------------
# Text editor Methods
# ------------------------------
def set_title(path):
    """
    Update the window title.
    If a path is provided, show file name.
    Otherwise, show "Untitled".
    """
    if path:
        window.title(f"Simple Text Editor - {os.path.basename(path)}")
    else:
        window.title("Simple Text Editor - Untitled")
#======================================================================================================#

def open_file():
    """
    Open a text file and load its content into the editor.
    - Uses askopenfilename() to select a file.
    - Replaces the current text content with the file content.
    - Updates the title bar with file name.
    """
    global current_file
    path = askopenfilename(filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not path:  # If user cancelled
        return
    try:
        with open(path, "r", encoding="utf-8") as input_file:
            content = input_file.read()
        txt_edit.delete("1.0", tk.END)  # Clear old content
        txt_edit.insert("1.0", content)  # Insert new content
        current_file = path
        set_title(path)
        txt_edit.edit_modified(False)  # Reset modified flag
    except Exception as e:
        showerror("Open Error", f"Could not open file:\n{e}")
#======================================================================================================#

def save_file_as():
    """
    Save the current text into a new file.
    - Uses asksaveasfilename() to ask for file name.
    - Writes editor content into the chosen file.
    - Updates title bar and resets modified flag.
    """
    global current_file
    path = asksaveasfilename(defaultextension=".txt",
                             filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if not path:
        return False
    try:
        with open(path, "w", encoding="utf-8") as output_file:
            content = txt_edit.get("1.0", "end-1c")  # avoid extra newline
            output_file.write(content)
        current_file = path
        set_title(path)
        txt_edit.edit_modified(False)
        return True
    except Exception as e:
        showerror("Save Error", f"Could not save file:\n{e}")
        return False
#======================================================================================================#

def save_file():
    """
    Save the file:
    - If already opened/saved, overwrite.
    - If no file exists, call save_file_as().
    """
    global current_file
    if current_file:
        try:
            with open(current_file, "w", encoding="utf-8") as f:
                f.write(txt_edit.get("1.0", "end-1c"))
            txt_edit.edit_modified(False)
        except Exception as e:
            showerror("Save Error", f"Could not save file:\n{e}")
    else:
        save_file_as()
#======================================================================================================#

def on_close():
    """
    Called when user closes the window.
    - If there are unsaved changes, ask for confirmation.
    - If confirmed, close the window.
    """
    if txt_edit.edit_modified():
        if not askyesno("Quit", "You have unsaved changes. Quit anyway?"):
            return
    window.destroy()


# ------------------------------
# GUI Setup
# ------------------------------
window = tk.Tk()
set_title(None)  # Start with Untitled
window.rowconfigure(0, weight=1)   # Allow text area to expand vertically
window.columnconfigure(1, weight=1)  # Allow text area to expand horizontally

# --- Left Frame with Buttons ---
frame_buttons = tk.Frame(window, relief=tk.RAISED)
btn_open = tk.Button(frame_buttons, text="Open File", width=12, command=open_file)
btn_save = tk.Button(frame_buttons, text="Save", width=12, command=save_file)
btn_saveas = tk.Button(frame_buttons, text="Save As", width=12, command=save_file_as)

# Place buttons inside frame (vertical)
btn_open.grid(column=0, row=0, sticky="ew", padx=5, pady=5)
btn_save.grid(column=0, row=1, sticky="ew", padx=5, pady=(0,5))
btn_saveas.grid(column=0, row=2, sticky="ew", padx=5)

# Place frame inside window
frame_buttons.grid(column=0, row=0, sticky="ns")

# --- Text Area with Scrollbar ---
txt_edit = tk.Text(window, wrap="word", undo=True, font=("Arial", 16))
scrollbar = tk.Scrollbar(window, orient='vertical', command=txt_edit.yview)
txt_edit.configure(yscrollcommand=scrollbar.set)

txt_edit.grid(column=1, row=0, sticky="nsew")
scrollbar.grid(column=2, row=0, sticky="ns")

# --- Menu Bar ---
menubar = tk.Menu(window)
filemenu = tk.Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=filemenu)
filemenu.add_command(label="Open...", accelerator="Ctrl+O", command=open_file)
filemenu.add_command(label="Save", accelerator="Ctrl+S", command=save_file)
filemenu.add_command(label="Save As...", accelerator="Ctrl+Shift+S", command=save_file_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=on_close)
window.config(menu=menubar)

# --- Keyboard Shortcuts ---
window.bind("<Control-o>", lambda e: open_file())
window.bind("<Control-s>", lambda e: save_file())
window.bind("<Control-S>", lambda e: save_file_as())  # Ctrl+Shift+S

# Focus text area & reset modified flag
txt_edit.focus_set()
txt_edit.edit_modified(False)

# Override window close button
window.protocol("WM_DELETE_WINDOW", on_close)

# Run application
window.mainloop()
