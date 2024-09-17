import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
from tkinter import font
import os

class Notepad:
    def __init__(self, root):
        self.root = root
        self.root.title("Untitled - Notepad")
        self.root.geometry("800x600")

        self.text_area = tk.Text(self.root, undo=True, wrap='word', font=("Arial", 12))
        self.text_area.pack(expand=True, fill='both')

        self.current_file = None

        self.create_menu()
        self.create_shortcuts()

    def create_menu(self):
        menubar = tk.Menu(self.root)

        # File Menu
        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_as_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", accelerator="Alt+F4", command=self.exit_app)
        menubar.add_cascade(label="File", menu=file_menu)

        # Edit Menu
        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=self.text_area.edit_undo)
        edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=self.text_area.edit_redo)
        edit_menu.add_separator()
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=lambda: self.text_area.event_generate('<<Cut>>'))
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=lambda: self.text_area.event_generate('<<Copy>>'))
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=lambda: self.text_area.event_generate('<<Paste>>'))
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=self.find_text)
        edit_menu.add_command(label="Replace", accelerator="Ctrl+H", command=self.replace_text)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        # Format Menu
        format_menu = tk.Menu(menubar, tearoff=0)
        format_menu.add_command(label="Increase Font Size", command=self.increase_font_size)
        format_menu.add_command(label="Decrease Font Size", command=self.decrease_font_size)
        menubar.add_cascade(label="Format", menu=format_menu)

        self.root.config(menu=menubar)

    def create_shortcuts(self):
        self.root.bind("<Control-n>", lambda event: self.new_file())
        self.root.bind("<Control-o>", lambda event: self.open_file())
        self.root.bind("<Control-s>", lambda event: self.save_file())
        self.root.bind("<Control-Shift-s>", lambda event: self.save_as_file())
        self.root.bind("<Control-f>", lambda event: self.find_text())
        self.root.bind("<Control-h>", lambda event: self.replace_text())
        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def new_file(self):
        if self.ask_save_changes():
            self.text_area.delete(1.0, tk.END)
            self.current_file = None
            self.root.title("Untitled - Notepad")

    def open_file(self):
        if self.ask_save_changes():
            file_path = filedialog.askopenfilename(defaultextension=".txt",
                                                   filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
            if file_path:
                with open(file_path, "r") as file:
                    self.text_area.delete(1.0, tk.END)
                    self.text_area.insert(tk.END, file.read())
                self.current_file = file_path
                self.root.title(os.path.basename(file_path) + " - Notepad")

    def save_file(self):
        if self.current_file:
            with open(self.current_file, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
        else:
            self.save_as_file()

    def save_as_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                                 filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(self.text_area.get(1.0, tk.END))
            self.current_file = file_path
            self.root.title(os.path.basename(file_path) + " - Notepad")

    def exit_app(self):
        if self.ask_save_changes():
            self.root.quit()

    def ask_save_changes(self):
        if self.text_area.edit_modified():
            response = messagebox.askyesnocancel("Save changes?", "Do you want to save changes to the current file?")
            if response:
                self.save_file()
            elif response is None:
                return False
        return True

    def find_text(self):
        find_window = tk.Toplevel(self.root)
        find_window.title("Find")
        find_window.geometry("300x100")

        tk.Label(find_window, text="Find:").pack(side='left', padx=10)
        find_entry = tk.Entry(find_window, width=20)
        find_entry.pack(side='left', padx=10)

        def find():
            self.text_area.tag_remove('highlight', '1.0', tk.END)
            text_to_find = find_entry.get()
            if text_to_find:
                idx = '1.0'
                while True:
                    idx = self.text_area.search(text_to_find, idx, nocase=1, stopindex=tk.END)
                    if not idx:
                        break
                    last_idx = f"{idx}+{len(text_to_find)}c"
                    self.text_area.tag_add('highlight', idx, last_idx)
                    idx = last_idx
                self.text_area.tag_config('highlight', background='yellow')

        tk.Button(find_window, text="Find", command=find).pack(side='left', padx=10)

    def replace_text(self):
        replace_window = tk.Toplevel(self.root)
        replace_window.title("Replace")
        replace_window.geometry("400x120")

        tk.Label(replace_window, text="Find:").grid(row=0, column=0, padx=10, pady=10)
        tk.Label(replace_window, text="Replace:").grid(row=1, column=0, padx=10, pady=10)

        find_entry = tk.Entry(replace_window, width=20)
        replace_entry = tk.Entry(replace_window, width=20)
        find_entry.grid(row=0, column=1, padx=10, pady=10)
        replace_entry.grid(row=1, column=1, padx=10, pady=10)

        def replace():
            text_to_find = find_entry.get()
            replacement_text = replace_entry.get()
            content = self.text_area.get(1.0, tk.END)
            new_content = content.replace(text_to_find, replacement_text)
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, new_content)

        tk.Button(replace_window, text="Replace", command=replace).grid(row=2, column=1, padx=10, pady=10)

    def increase_font_size(self):
        current_font = font.nametofont(self.text_area['font'])
        current_size = current_font['size']
        current_font.configure(size=current_size + 2)

    def decrease_font_size(self):
        current_font = font.nametofont(self.text_area['font'])
        current_size = current_font['size']
        current_font.configure(size=current_size - 2)

if __name__ == "__main__":
    root = tk.Tk()
    notepad = Notepad(root)
    root.mainloop()
