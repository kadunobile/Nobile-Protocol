import tkinter as tk
from tkinter import ttk, messagebox

class LinkedInUploadScreen:
    def __init__(self, master):
        self.master = master
        master.title("LinkedIn Upload Screen")

        self.tab_control = ttk.Notebook(master)

        self.upload_tab = ttk.Frame(self.tab_control)
        self.tutorial_tab = ttk.Frame(self.tab_control)
        self.validation_tab = ttk.Frame(self.tab_control)
        self.preview_tab = ttk.Frame(self.tab_control)

        self.tab_control.add(self.upload_tab, text='Upload')
        self.tab_control.add(self.tutorial_tab, text='Tutorial')
        self.tab_control.add(self.validation_tab, text='Validation')
        self.tab_control.add(self.preview_tab, text='Preview')

        self.tab_control.pack(expand=1, fill="both")

        self.create_upload_tab()
        self.create_tutorial_tab()
        self.create_validation_tab()
        self.create_preview_tab()

    def create_upload_tab(self):
        label = ttk.Label(self.upload_tab, text="Upload your file:")
        label.pack(padx=10, pady=10)

        self.upload_button = ttk.Button(self.upload_tab, text="Upload", command=self.upload_file)
        self.upload_button.pack(padx=10, pady=10)

    def upload_file(self):
        messagebox.showinfo("Upload", "File uploaded successfully!")

    def create_tutorial_tab(self):
        tutorial_text = "This is a tutorial on how to upload files."
        label = ttk.Label(self.tutorial_tab, text=tutorial_text)
        label.pack(padx=10, pady=10)

    def create_validation_tab(self):
        validation_text = "Ensure that your file is in the correct format."
        label = ttk.Label(self.validation_tab, text=validation_text)
        label.pack(padx=10, pady=10)

    def create_preview_tab(self):
        preview_text = "Preview of the uploaded file will be shown here."
        label = ttk.Label(self.preview_tab, text=preview_text)
        label.pack(padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    LinkedInUploadScreen(root)
    root.mainloop()