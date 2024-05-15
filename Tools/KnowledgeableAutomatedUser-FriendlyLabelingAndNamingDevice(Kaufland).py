import os
import re
import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageDraw

class KnowledgeableAutomatedUserFriendlyLabelingAndNamingDevice:
    def __init__(self, root):
        self.root = root
        self.root.title("Knowledgeable Automated User-Friendly Labeling And Naming Device (KAUFLAND)")

        self.label = tk.Label(root, text="Select the folder containing images")
        self.label.pack()

        self.select_button = tk.Button(root, text="Select Folder", command=self.select_folder)
        self.select_button.pack()

        self.listbox = tk.Listbox(root)
        self.listbox.pack(fill=tk.BOTH, expand=1)
        self.listbox.bind('<<ListboxSelect>>', self.on_select)

        self.canvas = tk.Canvas(root)
        self.canvas.pack()
        self.canvas.bind("<Motion>", self.update_cursor_position)
        self.canvas.bind("<Button-1>", self.on_canvas_click)

        self.cursor_position_label = tk.Label(root, text="Cursor Position: ")
        self.cursor_position_label.pack()

        self.edit_button = tk.Button(root, text="Enter Editing Mode", command=self.toggle_edit_mode, bg="red")
        self.edit_button.pack()

        self.next_button = tk.Button(root, text="Next", command=self.show_next_image)
        self.next_button.pack()

        self.prev_button = tk.Button(root, text="Previous", command=self.show_prev_image)
        self.prev_button.pack()

        self.delete_button = tk.Button(root, text="Delete Picture", command=self.delete_picture)
        self.delete_button.pack()

        self.folder_path = ""
        self.images = []
        self.current_image_index = -1
        self.current_image = None
        self.edit_mode = False
        self.upscale_factor = 2

        # Bind arrow keys for navigation
        root.bind('<Right>', lambda event: self.show_next_image())
        root.bind('<Left>', lambda event: self.show_prev_image())

    def select_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.load_images()
            self.populate_listbox()

    def load_images(self):
        self.images = [f for f in os.listdir(self.folder_path) if f.endswith(('.jpg', '.jpeg', '.png'))]

    def populate_listbox(self):
        self.listbox.delete(0, tk.END)
        for image in self.images:
            self.listbox.insert(tk.END, image)

    def on_select(self, event):
        selection = event.widget.curselection()
        if selection:
            self.current_image_index = selection[0]
            image_path = os.path.join(self.folder_path, self.images[self.current_image_index])
            self.display_image_with_labels(image_path)

    def display_image_with_labels(self, image_path):
        self.image_path = image_path
        self.original_image = Image.open(image_path)
        draw = ImageDraw.Draw(self.original_image)

        # Extract coordinates from filename
        basename = os.path.basename(image_path)
        self.coordinates = re.findall(r'(\d+)_(\d+)', basename)
        for coord in self.coordinates:
            x, y = map(int, coord)
            self.draw_red_circle(draw, x, y)

        # Upscale the image for display
        upscaled_image = self.original_image.resize(
            (self.original_image.width * self.upscale_factor, self.original_image.height * self.upscale_factor),
            Image.LANCZOS
        )

        self.current_image = ImageTk.PhotoImage(upscaled_image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.current_image)
        self.canvas.config(width=upscaled_image.width, height=upscaled_image.height)

        # Highlight the selected image in the listbox
        self.listbox.selection_clear(0, tk.END)
        self.listbox.selection_set(self.current_image_index)
        self.listbox.activate(self.current_image_index)
        self.listbox.see(self.current_image_index)  # Ensure the selected image is visible

    def draw_red_circle(self, draw, x, y, radius=5):
        left_up_point = (x - radius, y - radius)
        right_down_point = (x + radius, y + radius)
        draw.ellipse([left_up_point, right_down_point], outline="red", width=2)

    def update_cursor_position(self, event):
        self.cursor_position_label.config(text=f"Cursor Position: {event.x}, {event.y}")

    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        self.edit_button.config(bg="green" if self.edit_mode else "red")
        self.edit_button.config(text="Exit Editing Mode" if self.edit_mode else "Enter Editing Mode")

    def on_canvas_click(self, event):
        if self.edit_mode:
            # Adjust for the upscaling factor
            x = event.x // self.upscale_factor
            y = event.y // self.upscale_factor
            self.relabel_point((x, y))
            self.update_image_filename()
            self.display_image_with_labels(self.image_path)

    def relabel_point(self, new_label):
        new_x, new_y = new_label
        if len(self.coordinates) > 1:
            self.coordinates[0] = (new_x, new_y)
        else:
            self.coordinates = [(new_x, new_y)]

    def update_image_filename(self):
        # Get the original filename without coordinates
        basename = os.path.basename(self.image_path)
        name_parts = re.split(r'(\d+_\d+)', basename)
        # Replace only the first two coordinates
        if len(self.coordinates) > 0:
            name_parts[1] = f"{self.coordinates[0][0]}_{self.coordinates[0][1]}"
        if len(self.coordinates) > 1:
            name_parts[3] = f"{self.coordinates[1][0]}_{self.coordinates[1][1]}"

        # Join parts back together
        new_basename = "".join(name_parts)
        new_image_path = os.path.join(self.folder_path, new_basename)
        os.rename(self.image_path, new_image_path)
        self.image_path = new_image_path
        self.images[self.current_image_index] = new_basename
        self.populate_listbox()

    def show_next_image(self):
        if self.current_image_index < len(self.images) - 1:
            self.current_image_index += 1
            image_path = os.path.join(self.folder_path, self.images[self.current_image_index])
            self.display_image_with_labels(image_path)

    def show_prev_image(self):
        if self.current_image_index > 0:
            self.current_image_index -= 1
            image_path = os.path.join(self.folder_path, self.images[self.current_image_index])
            self.display_image_with_labels(image_path)

    def delete_picture(self):
        if self.current_image_index >= 0 and self.current_image_index < len(self.images):
            image_path = os.path.join(self.folder_path, self.images[self.current_image_index])
            os.remove(image_path)
            del self.images[self.current_image_index]
            self.populate_listbox()
            self.canvas.delete("all")
            self.current_image_index = -1

if __name__ == "__main__":
    root = tk.Tk()
    app = KnowledgeableAutomatedUserFriendlyLabelingAndNamingDevice(root)
    root.mainloop()
