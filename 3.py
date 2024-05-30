import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import numpy as np
import cv2


class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Editor")

        self.original_image = None
        self.processed_image = None
        self.selected_points = []

        # Frame for images
        self.image_frame = tk.Frame(root)
        self.image_frame.pack(side=tk.TOP, pady=10)

        self.left_panel = tk.Label(self.image_frame)
        self.left_panel.pack(side="left", padx=10, pady=10)

        self.right_panel = tk.Label(self.image_frame)
        self.right_panel.pack(side="right", padx=10, pady=10)

        # Frame for additional fields
        self.additional_fields_frame = tk.Frame(root)
        self.additional_fields_frame.pack(side=tk.BOTTOM, pady=10)

        # Frame for control buttons
        self.control_frame = tk.Frame(root)
        self.control_frame.pack(side=tk.BOTTOM, pady=10)

        self.load_button = tk.Button(self.control_frame, text="Load Image", command=self.load_image)
        self.load_button.pack(side=tk.LEFT, padx=0, pady=5)

        self.size_label = tk.Label(self.control_frame, text="")
        self.size_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.scale_button = tk.Button(self.control_frame, text="Scale Image", command=self.show_scale_fields)
        self.scale_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.shift_button = tk.Button(self.control_frame, text="Shift Image", command=self.show_shift_fields)
        self.shift_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.rotate_button = tk.Button(self.control_frame, text="Rotate Image", command=self.show_rotate_fields)
        self.rotate_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.mirror_button = tk.Button(self.control_frame, text="Mirror Image", command=self.show_mirror_buttons)
        self.mirror_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.project_button = tk.Button(self.control_frame, text="Project Fragment", command=self.project_fragment)
        self.project_button.pack(side=tk.LEFT, padx=5, pady=5)

        # Additional fields (initially not created)
        self.additional_fields_created = False
        self.additional_fields = []

        # Mirror buttons (initially not created)
        self.mirror_buttons_created = False
        self.mirror_buttons = []

        self.image_label = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.original_image = Image.open(file_path)
            self.display_image(self.original_image, self.left_panel)
            self.update_size_label()

    def display_image(self, image, panel):
        imgtk = ImageTk.PhotoImage(image=image)
        panel.imgtk = imgtk
        panel.config(image=imgtk)

    def update_size_label(self):
        if self.original_image:
            width, height = self.original_image.size
            self.size_label.config(text=f"Original size: {width} x {height}")

    def show_scale_fields(self):
        self.clear_fields_frame()

        self.width_scale_label = tk.Label(self.additional_fields_frame, text="Width Scale:")
        self.width_scale_label.pack(side=tk.TOP, padx=5, pady=5)
        self.width_scale_entry = tk.Entry(self.additional_fields_frame)
        self.width_scale_entry.pack(side=tk.TOP, padx=5, pady=5)

        self.height_scale_label = tk.Label(self.additional_fields_frame, text="Height Scale:")
        self.height_scale_label.pack(side=tk.TOP, padx=5, pady=5)
        self.height_scale_entry = tk.Entry(self.additional_fields_frame)
        self.height_scale_entry.pack(side=tk.TOP, padx=5, pady=5)

        self.apply_scale_button = tk.Button(self.additional_fields_frame, text="Apply Scale", command=self.scale_image)
        self.apply_scale_button.pack(side=tk.TOP, padx=5, pady=5)

        self.apply_scale_bilinear_button = tk.Button(self.additional_fields_frame, text="Apply Bilinear Scale", command=self.scale_image_bilinear)
        self.apply_scale_bilinear_button.pack(side=tk.TOP, padx=5, pady=5)

        self.additional_fields_created = True

    def show_shift_fields(self):
        self.clear_fields_frame()

        self.shift_value_label = tk.Label(self.additional_fields_frame, text="Shift Value (0 to 1):")
        self.shift_value_label.pack(side=tk.TOP, padx=5, pady=5)
        self.shift_value_entry = tk.Entry(self.additional_fields_frame)
        self.shift_value_entry.pack(side=tk.TOP, padx=5, pady=5)

        self.apply_shift_button = tk.Button(self.additional_fields_frame, text="Apply Shift", command=self.shift_image)
        self.apply_shift_button.pack(side=tk.TOP, padx=5, pady=5)

        self.additional_fields_created = True

    def show_rotate_fields(self):
        self.clear_fields_frame()

        self.rotation_angle_label = tk.Label(self.additional_fields_frame, text="Rotation Angle:")
        self.rotation_angle_label.pack(side=tk.TOP, padx=5, pady=5)
        self.rotation_angle_entry = tk.Entry(self.additional_fields_frame)
        self.rotation_angle_entry.pack(side=tk.TOP, padx=5, pady=5)

        self.rotation_center_label = tk.Label(self.additional_fields_frame, text="Rotation Center (x, y):")
        self.rotation_center_label.pack(side=tk.TOP, padx=5, pady=5)
        self.rotation_center_entry = tk.Entry(self.additional_fields_frame)
        self.rotation_center_entry.pack(side=tk.TOP, padx=5, pady=5)

        self.apply_rotation_button = tk.Button(self.additional_fields_frame, text="Apply Rotation", command=self.rotate_image)
        self.apply_rotation_button.pack(side=tk.TOP, padx=5, pady=5)

        self.apply_rotation_bilinear_button = tk.Button(self.additional_fields_frame, text="Apply Bilinear Rotation", command=self.rotate_image_bilinear)
        self.apply_rotation_bilinear_button.pack(side=tk.TOP, padx=5, pady=5)

        self.additional_fields_created = True

    def show_mirror_buttons(self):
        self.clear_fields_frame()

        self.mirror_normal_button = tk.Button(self.additional_fields_frame, text="Normal Image", command=lambda: self.mirror_image("normal"))
        self.mirror_normal_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.mirror_left_button = tk.Button(self.additional_fields_frame, text="Mirror Left", command=lambda: self.mirror_image("left"))
        self.mirror_left_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.mirror_top_button = tk.Button(self.additional_fields_frame, text="Mirror Top", command=lambda: self.mirror_image("top"))
        self.mirror_top_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.mirror_diagonal_button = tk.Button(self.additional_fields_frame, text="Mirror Diagonal", command=lambda: self.mirror_image("diagonal"))
        self.mirror_diagonal_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.mirror_buttons_created = True

    def clear_fields_frame(self):
        if self.additional_fields_created:
            for widget in self.additional_fields_frame.winfo_children():
                widget.pack_forget()
            self.additional_fields_created = False
        if self.mirror_buttons_created:
            for widget in self.additional_fields_frame.winfo_children():
                widget.pack_forget()
            self.mirror_buttons_created = False

    def scale_image(self):
        if self.original_image:
            try:
                width_scale = float(self.width_scale_entry.get())
                height_scale = float(self.height_scale_entry.get())
                if width_scale <= 0 or height_scale <= 0:
                    raise ValueError("Scale factors must be positive numbers.")
                new_width = int(self.original_image.width * width_scale)
                new_height = int(self.original_image.height * height_scale)

                self.processed_image = self.original_image.resize((new_width, new_height), Image.LANCZOS)

                # Crop the image to the original size to simulate zoom
                if width_scale > 1 or height_scale > 1:
                    crop_width = min(self.original_image.width, new_width)
                    crop_height = min(self.original_image.height, new_height)
                    left = (new_width - crop_width) // 2
                    top = (new_height - crop_height) // 2
                    right = left + crop_width
                    bottom = top + crop_height
                    self.processed_image = self.processed_image.crop((left, top, right, bottom))

                self.display_image(self.processed_image, self.right_panel)
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
        else:
            messagebox.showerror("No Image", "Please load an image first.")

    def scale_image_bilinear(self):
        if self.original_image:
            try:
                width_scale = float(self.width_scale_entry.get())
                height_scale = float(self.height_scale_entry.get())
                if width_scale <= 0 or height_scale <= 0:
                    raise ValueError("Scale factors must be positive numbers.")
                new_width = int(self.original_image.width * width_scale)
                new_height = int(self.original_image.height * height_scale)

                self.processed_image = self.original_image.resize((new_width, new_height), Image.BILINEAR)

                # Crop the image to the original size to simulate zoom
                if width_scale > 1 or height_scale > 1:
                    crop_width = min(self.original_image.width, new_width)
                    crop_height = min(self.original_image.height, new_height)
                    left = (new_width - crop_width) // 2
                    top = (new_height - crop_height) // 2
                    right = left + crop_width
                    bottom = top + crop_height
                    self.processed_image = self.processed_image.crop((left, top, right, bottom))

                self.display_image(self.processed_image, self.right_panel)
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
        else:
            messagebox.showerror("No Image", "Please load an image first.")

    def shift_image(self):
        if self.original_image:
            try:
                shift_value = float(self.shift_value_entry.get())
                if not (0 <= shift_value <= 1):
                    raise ValueError("Shift value must be between 0 and 1.")
                width, height = self.original_image.size
                new_image = Image.new("RGB", (width, height))

                # Shift the image
                for y in range(height):
                    for x in range(width):
                        new_x = int(x + shift_value * (height - y))
                        new_y = y
                        if 0 <= new_x < width:
                            new_image.putpixel((new_x, new_y), self.original_image.getpixel((x, y)))

                self.processed_image = new_image
                self.display_image(self.processed_image, self.right_panel)
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
        else:
            messagebox.showerror("No Image", "Please load an image first.")

    def rotate_image(self):
        if self.original_image:
            try:
                angle = float(self.rotation_angle_entry.get())
                center = self.rotation_center_entry.get().split(',')
                center_x = int(center[0])
                center_y = int(center[1])

                if angle == 0:
                    messagebox.showwarning("Warning", "Rotation angle is 0. Image remains unchanged.")
                    return

                if not (0 <= center_x < self.original_image.width) or not (0 <= center_y < self.original_image.height):
                    raise ValueError("Rotation center coordinates are out of image bounds.")

                self.processed_image = self.original_image.rotate(angle, center=(center_x, center_y), resample=Image.NEAREST)
                self.display_image(self.processed_image, self.right_panel)
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
        else:
            messagebox.showerror("No Image", "Please load an image first.")

    def rotate_image_bilinear(self):
        if self.original_image:
            try:
                angle = float(self.rotation_angle_entry.get())
                center = self.rotation_center_entry.get().split(',')
                center_x = int(center[0])
                center_y = int(center[1])

                if angle == 0:
                    messagebox.showwarning("Warning", "Rotation angle is 0. Image remains unchanged.")
                    return

                if not (0 <= center_x < self.original_image.width) or not (0 <= center_y < self.original_image.height):
                    raise ValueError("Rotation center coordinates are out of image bounds.")

                self.processed_image = self.original_image.rotate(angle, center=(center_x, center_y), resample=Image.BILINEAR)
                self.display_image(self.processed_image, self.right_panel)
            except ValueError as e:
                messagebox.showerror("Invalid Input", str(e))
        else:
            messagebox.showerror("No Image", "Please load an image first.")

    def mirror_image(self, direction):
        if self.original_image:
            try:
                width, height = self.original_image.size
                new_image = Image.new("RGB", (width, height))

                if direction == "normal":
                    new_image = self.original_image.copy()
                elif direction == "left":
                    for x in range(width):
                        for y in range(height):
                            new_x = width - x - 1
                            new_image.putpixel((new_x, y), self.original_image.getpixel((x, y)))
                elif direction == "top":
                    for x in range(width):
                        for y in range(height):
                            new_y = height - y - 1
                            new_image.putpixel((x, new_y), self.original_image.getpixel((x, y)))
                elif direction == "diagonal":
                    for x in range(width):
                        for y in range(height):
                            new_x = width - x - 1
                            new_y = height - y - 1
                            new_image.putpixel((new_x, new_y), self.original_image.getpixel((x, y)))

                self.processed_image = new_image
                self.display_image(self.processed_image, self.right_panel)
            except Exception as e:
                messagebox.showerror("Error", str(e))
        else:
            messagebox.showerror("No Image", "Please load an image first.")

    def project_fragment(self):
        if self.original_image:
            self.selected_points = []
            self.image_label = tk.Label(self.left_panel, image=self.left_panel.imgtk)
            self.image_label.pack()
            self.image_label.bind("<Button-1>", self.get_mouse_click)

            messagebox.showinfo("Info", "Click on the image to select 4 points for the projection.")
        else:
            messagebox.showerror("No Image", "Please load an image first.")

    def get_mouse_click(self, event):
        if len(self.selected_points) < 4:
            self.selected_points.append((event.x, event.y))
            if len(self.selected_points) == 4:
                self.perform_projection()

    def perform_projection(self):
        if len(self.selected_points) != 4:
            messagebox.showerror("Error", "Please select exactly 4 points.")
            return

        src_points = np.array(self.selected_points, dtype="float32")

        dst_points = np.array([
            [0, 0],
            [self.original_image.width - 1, 0],
            [self.original_image.width - 1, self.original_image.height - 1],
            [0, self.original_image.height - 1]
        ], dtype="float32")

        matrix = cv2.getPerspectiveTransform(src_points, dst_points)
        cv_image = np.array(self.original_image)
        warped_image = cv2.warpPerspective(cv_image, matrix, (self.original_image.width, self.original_image.height))

        self.processed_image = Image.fromarray(warped_image)
        self.display_image(self.processed_image, self.right_panel)

        self.image_label.unbind("<Button-1>")
        self.selected_points = []
        self.image_label.pack_forget()


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()
