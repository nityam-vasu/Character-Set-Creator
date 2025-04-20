import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageDraw
import os

class HindiCharacterDrawingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Character Dataset Creator")
        self.grid_size = 32  # Default grid size
        self.cell_size = 16  # Reverted cell size
        self.characters = []
        self.frequency = 0
        self.current_char_index = 0
        self.current_draw_number = 1
        self.base_folder = ""
        self.char_file_path = ""  # Store character file path
        self.grid_state = []
        self.draw_history = []  # Store drawn cells for undo
        self.setup_initial_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)  # Handle window close

    def setup_initial_ui(self):
        """Set up UI for inputting base folder, character file, and frequency with larger text."""
        self.clear_window()

        tk.Label(self.root, text="Base Output Folder:", font=("Arial", 16)).grid(row=0, column=0, padx=5, pady=5)
        self.folder_entry = tk.Entry(self.root, width=50, font=("Arial", 14))
        self.folder_entry.grid(row=0, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.select_folder, font=("Arial", 14), width=8).grid(row=0, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Character File (.txt):", font=("Arial", 16)).grid(row=1, column=0, padx=5, pady=5)
        self.file_entry = tk.Entry(self.root, width=50, font=("Arial", 14))
        self.file_entry.grid(row=1, column=1, padx=5, pady=5)
        tk.Button(self.root, text="Browse", command=self.select_file, font=("Arial", 14), width=8).grid(row=1, column=2, padx=5, pady=5)

        tk.Label(self.root, text="Frequency per Character:", font=("Arial", 16)).grid(row=2, column=0, padx=5, pady=5)
        self.freq_entry = tk.Entry(self.root, width=10, font=("Arial", 14))
        self.freq_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        tk.Button(self.root, text="Start Drawing", command=self.start_drawing, font=("Arial", 16), width=12).grid(row=3, column=1, pady=10)

    def clear_window(self):
        """Clear all widgets from the window."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def select_folder(self):
        """Open folder selection dialog."""
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def select_file(self):
        """Open file selection dialog for .txt file and store path."""
        file = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file:
            self.file_entry.delete(0, tk.END)
            self.file_entry.insert(0, file)
            self.char_file_path = file  # Store file path

    def start_drawing(self):
        """Validate inputs and set up drawing UI."""
        self.base_folder = self.folder_entry.get()
        char_file = self.char_file_path  # Use stored file path

        if not self.base_folder or not os.path.exists(self.base_folder):
            messagebox.showerror("Error", "Please select a valid output folder.")
            return
        if not char_file or not os.path.exists(char_file):
            messagebox.showerror("Error", "Please select a valid character file.")
            return
        try:
            self.frequency = int(self.freq_entry.get())
            if self.frequency < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid frequency (positive integer).")
            return

        try:
            with open(char_file, 'r', encoding='utf-8') as f:
                self.characters = [line.strip() for line in f if line.strip()]
            if not self.characters:
                raise ValueError
        except:
            messagebox.showerror("Error", "Invalid or empty character file.")
            return

        self.setup_drawing_ui()

    def setup_drawing_ui(self):
        """Set up the drawing interface."""
        self.clear_window()

        # Current character and drawing number
        current_char = self.characters[self.current_char_index]
        tk.Label(self.root, text=f"Character :  {current_char}", font=("Arial", 14)).grid(row=0, column=0, padx=5, pady=5)
        tk.Label(self.root, text=f"Drawing: {self.current_draw_number} / {self.frequency}", font=("Arial", 14)).grid(row=0, column=1, padx=5, pady=5)

        # Grid size entry
        tk.Label(self.root, text="Grid Size:").grid(row=1, column=1, padx=5, pady=5)
        self.grid_size_entry = tk.Entry(self.root, width=10)
        self.grid_size_entry.insert(0, str(self.grid_size))
        self.grid_size_entry.grid(row=1, column=2, sticky="w", padx=5, pady=5)
        tk.Button(self.root, text="Change Grid", command=self.change_grid_size, width=8).grid(row=1, column=3, padx=5, pady=5)
		
		# Buttons
        tk.Button(self.root, text="Save", command=self.save_drawing, width=8).grid(row=2, column=0, pady=10)
        tk.Button(self.root, text="Clear", command=self.clear_grid, width=8).grid(row=2, column=1, pady=10)
        tk.Button(self.root, text="Undo", command=self.undo, width=8).grid(row=2, column=2, pady=10)
        tk.Button(self.root, text="Save Remaining", command=self.close_drawing, width=16).grid(row=2, column=3, pady=10)
		
        # Canvas for drawing
        self.canvas = tk.Canvas(self.root, width=self.grid_size * self.cell_size, height=self.grid_size * self.cell_size, bg="white")
        self.canvas.grid(row=3, column=0, columnspan=4, padx=5, pady=5)
        self.grid_state = [[0] * self.grid_size for _ in range(self.grid_size)]  # 0: white, 1: black
        self.draw_history = []  # Reset draw history
        self.draw_grid()
        self.canvas.bind("<Button-1>", self.start_drawing_cell)
        self.canvas.bind("<B1-Motion>", self.draw_cell)  # Continuous drawing


        # Bind Enter key to save
        self.root.bind("<Return>", lambda event: self.save_drawing())

    def draw_grid(self):
        """Draw the grid on the canvas."""
        self.canvas.delete("all")
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size
                y1 = i * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size
                color = "black" if self.grid_state[i][j] else "white"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def start_drawing_cell(self, event):
        """Start drawing on mouse click."""
        self.draw_cell(event)

    def draw_cell(self, event):
        """Draw continuously on mouse drag."""
        j = event.x // self.cell_size
        i = event.y // self.cell_size
        if 0 <= i < self.grid_size and 0 <= j < self.grid_size and not self.grid_state[i][j]:
            self.grid_state[i][j] = 1  # Set to black
            self.draw_history.append((i, j))  # Record for undo
            self.draw_grid()

    def clear_grid(self):
        """Clear the grid."""
        self.grid_state = [[0] * self.grid_size for _ in range(self.grid_size)]
        self.draw_history = []
        self.draw_grid()

    def undo(self):
        """Revert the last 10 drawn cells."""
        for _ in range(min(10, len(self.draw_history))):
            if self.draw_history:
                i, j = self.draw_history.pop()
                self.grid_state[i][j] = 0  # Set back to white
        self.draw_grid()

    def change_grid_size(self):
        """Change the grid size based on user input."""
        try:
            new_size = int(self.grid_size_entry.get())
            if new_size < 4 or new_size > 100:
                raise ValueError
            self.grid_size = new_size
            self.setup_drawing_ui()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid grid size (4-100).")

    def save_drawing(self):
        """Save the drawing as a PNG file silently."""
        current_char = self.characters[self.current_char_index]
        char_folder = os.path.join(self.base_folder, current_char)
        os.makedirs(char_folder, exist_ok=True)

        # Create image
        image = Image.new("L", (self.grid_size, self.grid_size), 255)  # Grayscale, white background
        draw = ImageDraw.Draw(image)
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.grid_state[i][j]:
                    image.putpixel((j, i), 0)  # Black pixel

        # Save image
        filename = os.path.join(char_folder, f"{current_char}_{self.current_draw_number}.png")
        image.save(filename)

        # Update drawing number and character
        self.current_draw_number += 1
        if self.current_draw_number > self.frequency:
            self.current_char_index += 1
            self.current_draw_number = 1
            if self.current_char_index >= len(self.characters):
                self.setup_initial_ui()
                return
        self.clear_grid()
        self.setup_drawing_ui()

    def save_remaining_chars(self):
        """Save remaining characters to a resume file."""
        if not self.characters or not self.char_file_path:
            return
        remaining = []
        # Include current character if frequency not complete
        if self.current_char_index < len(self.characters) and self.current_draw_number <= self.frequency:
            current_char = self.characters[self.current_char_index]
            remaining.extend([current_char] * (self.frequency - self.current_draw_number + 1))
        # Include remaining characters
        remaining.extend(self.characters[self.current_char_index + 1:])
        if remaining:
            original_file = os.path.basename(self.char_file_path)
            resume_filename = f"resume_{original_file}"
            resume_path = os.path.join(self.base_folder, resume_filename)
            with open(resume_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(remaining))

    def close_drawing(self):
        """Save remaining characters and return to initial UI."""
        try:
            resume_path = self.save_remaining_chars()
            if resume_path and os.path.exists(resume_path):
                messagebox.showinfo("Success", f"Resume file saved successfully at output folder: {self.base_folder}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save resume file: {e}")
        self.setup_initial_ui()
        
        
        
    def on_closing(self):
        """Handle window close by saving remaining characters and exiting."""
        try:
            self.save_remaining_chars()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save resume file: {e}")
        finally:
            self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = HindiCharacterDrawingApp(root)
    root.mainloop()
