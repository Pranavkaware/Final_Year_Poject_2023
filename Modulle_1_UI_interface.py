import tkinter as tk
from tkinter import ttk
from subprocess import call
from tkinter import messagebox
import csv
import os

def CameraMOD():
    call(["python", "Module_2_finger_dimension.py"])  # Adjusted to the correct path

def ARM():
    call(["python", "Module_3_arm_dimension.py"])  # Adjusted to the correct path

def LEG():
    call(["python", "LEGDIM.py"])  # Ensure this file path is correct

def Image():
    call(["python", "ak.py"])  # Ensure this file path is correct

def build_part(part):
    if part == 'finger':
        CameraMOD()
    elif part == 'arm':
        ARM()
    elif part == 'leg':
        LEG()
    elif part == 'image':
        Image()

def view_values(part):
    file_name = f"{part}_values.csv"
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            reader = csv.reader(file)
            values = '\n'.join(', '.join(row) for row in reader)
            messagebox.showinfo("Detected Values", values)
    else:
        messagebox.showinfo("No Values", f"No {part} values detected.")

def select_option():
    selected_option = option_var.get()
    build_part(selected_option)

# Creating the main application window
root = tk.Tk()
root.title("Prosthetic Options")

# Function to create navigation bar
def create_navigation_bar(root):
    navigation_frame = ttk.Frame(root, style='Navbar.TFrame')
    navigation_frame.pack(side="top", fill="x", pady=20)

    home_button = ttk.Label(navigation_frame, text="Home", style='Navbar.TLabel')
    home_button.pack(side="left", padx=30)

    about_button = ttk.Label(navigation_frame, text="About", style='Navbar.TLabel')
    about_button.pack(side="left", padx=30)

    products_button = ttk.Label(navigation_frame, text="Products", style='Navbar.TLabel')
    products_button.pack(side="left", padx=30)

    contact_button = ttk.Label(navigation_frame, text="Contact", style='Navbar.TLabel')
    contact_button.pack(side="left", padx=30)

    for part in ['finger', 'arm', 'leg', 'image']:
        view_values_button = ttk.Label(navigation_frame, text=f"View {part.capitalize()} Values", style='Navbar.TLabel')
        view_values_button.pack(side="left", padx=30)
        view_values_button.bind("<Button-1>", lambda event, p=part: view_values(p))

# Function to create footer
def create_footer(root):
    footer_frame = ttk.Frame(root, style='Footer.TFrame')
    footer_frame.pack(side="bottom", fill="x")

    footer_label = ttk.Label(footer_frame, text="© 2024 All rights reserved.", style='Footer.TLabel')
    footer_label.pack(side="bottom", padx=5, pady=5)

# Function to create prosthetic options
def create_prosthetic_options(root):
    options_frame = ttk.Frame(root)
    options_frame.pack(expand=True, padx=20, pady=20)

    ttk.Label(options_frame, text="Select Prosthetic:", font=('Arial', 16)).pack(pady=20)

    global option_var
    option_var = tk.StringVar()

    prosthetic_options = ['finger', 'arm', 'leg', 'image']

    for prosthetic in prosthetic_options:
        button = ttk.Label(options_frame, text=prosthetic, style='Prosthetic.TLabel')
        button.pack(side="left", padx=30, pady=40)
        button.bind("<Button-1>", lambda event, p=prosthetic: build_part(p))
        button.config(font=('Arial', 16))

# Configure style
style = ttk.Style()

style.configure('Navbar.TLabel', background='black', foreground='white', font=('Arial', 12), borderwidth=2, relief="raised")
style.map('Navbar.TLabel', background=[('active', 'black')])
style.configure('Footer.TLabel', background='#333', foreground='white', font=('Arial', 10))
style.configure('Navbar.TFrame', background='black')
style.configure('Footer.TFrame', background='#333')
style.configure('Prosthetic.TLabel', background='black', foreground='white', font=('Arial', 14), borderwidth=2, relief="raised")

# Create UI components
create_navigation_bar(root)
create_prosthetic_options(root)
create_footer(root)

root.mainloop()
