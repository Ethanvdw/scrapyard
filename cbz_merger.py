import os
import tkinter as tk
from tkinter import filedialog, ttk
import zipfile

def merge_cbz_files():
    merged_cbz = zipfile.ZipFile(os.path.join(os.path.expanduser("~"), "Desktop", "merged.cbz"), "w")

    for cbz_index, file_path in enumerate(file_paths, start=1):
        with zipfile.ZipFile(file_path, "r") as cbz_file:
            for file_info in cbz_file.infolist():
                filename = file_info.filename
                if filename.endswith('/'):  # Skip directories
                    merged_cbz.writestr(filename, cbz_file.read(filename))
                else:
                    new_filename = f"{cbz_index:03d}_{filename}"
                    merged_cbz.writestr(new_filename, cbz_file.read(filename))

    merged_cbz.close()

    status_label.config(text=f"Files merged and saved to {os.path.join(os.path.expanduser('~'), 'Desktop', 'merged.cbz')}")

def browse_files():
    global file_paths
    file_paths = sorted(filedialog.askopenfilenames(
        title="Select CBZ Files",
        filetypes=[("CBZ Files", "*.cbz")]
    ))
    update_file_list()

def update_file_list():
    file_list.delete(0, tk.END)
    for file_path in file_paths:
        file_list.insert(tk.END, os.path.basename(file_path))

def move_up():
    selected_indices = file_list.curselection()
    if selected_indices:
        indices = list(selected_indices)
        for index in indices:
            if index > 0:
                file_paths.insert(index - 1, file_paths.pop(index))
        update_file_list()
        file_list.selection_clear(0, tk.END)
        for index in [idx - 1 for idx in indices if idx > 0]:
            file_list.selection_set(index)

def move_down():
    selected_indices = file_list.curselection()
    if selected_indices:
        indices = list(selected_indices)
        indices.reverse()
        for index in indices:
            if index < len(file_paths) - 1:
                file_paths.insert(index + 1, file_paths.pop(index))
        update_file_list()
        file_list.selection_clear(0, tk.END)
        for index in [idx + 1 for idx in indices if idx < len(file_paths) - 1]:
            file_list.selection_set(index)

def move_to_top():
    selected_indices = file_list.curselection()
    if selected_indices:
        indices = list(selected_indices)
        for index in indices:
            file_paths.insert(0, file_paths.pop(index))
        update_file_list()
        file_list.selection_clear(0, tk.END)
        for index in range(len(indices)):
            file_list.selection_set(index)

root = tk.Tk()
root.title("CBZ File Merger")

file_frame = ttk.Frame(root)
file_frame.pack(pady=10)

file_list = tk.Listbox(file_frame, width=40, selectmode=tk.EXTENDED)
file_list.pack(side=tk.LEFT, fill=tk.BOTH)

scroll_bar = ttk.Scrollbar(file_frame, orient=tk.VERTICAL, command=file_list.yview)
scroll_bar.pack(side=tk.RIGHT, fill=tk.Y)
file_list.config(yscrollcommand=scroll_bar.set)

button_frame = ttk.Frame(root)
button_frame.pack(pady=10)

browse_button = ttk.Button(button_frame, text="Browse Files", command=browse_files)
browse_button.pack(side=tk.LEFT, padx=5)

move_up_button = ttk.Button(button_frame, text="Move Up", command=move_up)
move_up_button.pack(side=tk.LEFT, padx=5)

move_down_button = ttk.Button(button_frame, text="Move Down", command=move_down)
move_down_button.pack(side=tk.LEFT, padx=5)

move_to_top_button = ttk.Button(button_frame, text="Move to Top", command=move_to_top)
move_to_top_button.pack(side=tk.LEFT, padx=5)

merge_button = ttk.Button(button_frame, text="Merge Files", command=merge_cbz_files)
merge_button.pack(side=tk.LEFT, padx=5)

status_label = ttk.Label(root, text="")
status_label.pack(pady=10)

file_paths = []

root.mainloop()