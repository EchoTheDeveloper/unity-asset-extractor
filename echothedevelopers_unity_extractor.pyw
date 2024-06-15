import UnityPy
import os
import tkinter as tk
from tkinter import filedialog, messagebox, Text
from ttkbootstrap import Style
from ttkbootstrap.widgets import Frame, Label, Entry, Button

def extract_assets_from_unity_game(game_path, output_path, output_text):
    os.makedirs(output_path, exist_ok=True)
    for root, _, files in os.walk(game_path):
        for file in files:
            file_path = os.path.join(root, file)
            try:
                env = UnityPy.load(file_path)
            except PermissionError:
                output_text.insert(tk.END, f"Permission denied: {file_path}\n")
                continue
            except Exception as e:
                output_text.insert(tk.END, f"Error loading file {file_path}: {e}\n")
                continue
            for obj in env.objects:
                try:
                    if obj.type.name in ["Texture2D", "Sprite"]:
                        data = obj.read()
                        img = data.image
                        img_path = os.path.join(output_path, f"{data.name}.png")
                        img.save(img_path)
                        output_text.insert(tk.END, f"Extracted {data.name}.png\n")
                    elif obj.type.name == "TextAsset":
                        data = obj.read()
                        txt_path = os.path.join(output_path, f"{data.name}.txt")
                        with open(txt_path, "w", encoding="utf-8") as txt_file:
                            txt_file.write(data.script)
                        output_text.insert(tk.END, f"Extracted {data.name}.txt\n")
                    elif obj.type.name == "AudioClip":
                        data = obj.read()
                        audio_path = os.path.join(output_path, f"{data.name}.wav")
                        with open(audio_path, "wb") as audio_file:
                            audio_file.write(data.samples)
                        output_text.insert(tk.END, f"Extracted {data.name}.wav\n")
                except PermissionError:
                    output_text.insert(tk.END, f"Permission denied when extracting asset: {file_path}\n")
                    continue
                except Exception as e:
                    output_text.insert(tk.END, f"Error extracting asset from file {file_path}: {e}\n")
                    continue

class AssetExtractorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unity Asset Extractor")
        self.style = Style(theme="darkly")

        self.frame = Frame(root, padding=(20, 10))
        self.frame.pack(fill=tk.BOTH, expand=True)

        self.label_game_path = Label(self.frame, text="Select Unity Game Path:")
        self.label_game_path.pack(anchor=tk.W, pady=(0, 5))

        self.entry_game_path = Entry(self.frame, width=50)
        self.entry_game_path.pack(fill=tk.X, pady=(0, 10))

        self.button_game_path = Button(self.frame, text="Browse", command=self.browse_game_path)
        self.button_game_path.pack(pady=(0, 10))

        self.label_output_path = Label(self.frame, text="Select Output Path:")
        self.label_output_path.pack(anchor=tk.W, pady=(0, 5))

        self.entry_output_path = Entry(self.frame, width=50)
        self.entry_output_path.pack(fill=tk.X, pady=(0, 10))

        self.button_output_path = Button(self.frame, text="Browse", command=self.browse_output_path)
        self.button_output_path.pack(pady=(0, 10))

        self.button_extract = Button(self.frame, text="Extract Assets", command=self.extract_assets)
        self.button_extract.pack(pady=(20, 0))

        self.label_output = Label(self.frame, text="Output:")
        self.label_output.pack(anchor=tk.W, pady=(20, 5))

        self.output_text = Text(self.frame, height=10, wrap=tk.WORD)
        self.output_text.pack(fill=tk.BOTH, expand=True)

    def browse_game_path(self):
        game_path = filedialog.askdirectory()
        if game_path:
            self.entry_game_path.delete(0, tk.END)
            self.entry_game_path.insert(0, game_path)

    def browse_output_path(self):
        output_path = filedialog.askdirectory()
        if output_path:
            self.entry_output_path.delete(0, tk.END)
            self.entry_output_path.insert(0, output_path)

    def extract_assets(self):
        game_path = self.entry_game_path.get()
        output_path = self.entry_output_path.get()
        if not game_path or not output_path:
            messagebox.showerror("Error", "Please select both game path and output path.")
            return
        self.output_text.delete(1.0, tk.END)  # Clear previous output
        try:
            extract_assets_from_unity_game(game_path, output_path, self.output_text)
            messagebox.showinfo("Success", "Assets extracted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = AssetExtractorApp(root)
    root.mainloop()
