import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import folium
import os

# Global variable to hold the loaded Excel data
df = None

def select_input_file():
    global df
    filepath = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
    input_file_path.set(filepath)

    try:
        # Load the Excel file and update dropdown options
        df = pd.read_excel(filepath)
        column_options = df.columns.tolist()

        # Update dropdown menus with column names
        coordinate_column.set('')
        specimen_name_column.set('')
        description_column.set('')
        coord_dropdown['menu'].delete(0, 'end')
        name_dropdown['menu'].delete(0, 'end')
        desc_dropdown['menu'].delete(0, 'end')

        for col in column_options:
            coord_dropdown['menu'].add_command(label=col, command=tk._setit(coordinate_column, col))
            name_dropdown['menu'].add_command(label=col, command=tk._setit(specimen_name_column, col))
            desc_dropdown['menu'].add_command(label=col, command=tk._setit(description_column, col))

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while loading the file: {e}")

def select_output_folder():
    folderpath = filedialog.askdirectory()
    output_folder_path.set(folderpath)

def process_data():
    try:
        global df
        if df is None:
            raise ValueError("No data loaded. Please select an input file.")

        # Get selected columns from the dropdowns
        coord_col = coordinate_column.get()
        name_col = specimen_name_column.get()
        desc_col = description_column.get()

        if not coord_col or not name_col:
            raise ValueError("Please select all required columns (coordinates, name).")

        # Check if the selected columns exist in the DataFrame
        if not {coord_col, name_col, desc_col}.issubset(df.columns):
            raise ValueError("Selected columns do not exist in the data.")

        # Processing the settings
        zoom_level = int(zoom_level_var.get())  # Get the zoom level from user input

        # Create the map
        m = folium.Map(location=[0, 0], zoom_start=zoom_level)  # Center map around (0, 0)

        # Add markers with popups for each specimen
        for _, row in df.iterrows():
            try:
                lat, lon = map(float, row[coord_col].split(','))  # Split the coordinate string into lat, lon
                popup_text = f"<b>{row[name_col]}</b><br>{row[desc_col]}"
                folium.Marker([lat, lon], popup=popup_text).add_to(m)
            except ValueError:
                raise ValueError(f"Invalid coordinate format in row: {row[coord_col]}")

        # Set output file
        output_folder = output_folder_path.get()
        if not output_folder:
            raise ValueError("Output folder not selected.")

        output_file = os.path.join(output_folder, "mineral_collection_map.html")
        m.save(output_file)

        messagebox.showinfo("Success", f"Interactive map created successfully at {output_file}!")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# Set up the main window
root = tk.Tk()
root.title("Mineral Collection Mapper")

# Variables to store file paths and settings
input_file_path = tk.StringVar()
output_folder_path = tk.StringVar()
zoom_level_var = tk.StringVar(value="6")  # Default zoom level
coordinate_column = tk.StringVar()
specimen_name_column = tk.StringVar()
description_column = tk.StringVar()

# Input file section
tk.Label(root, text="Select Input Excel File:").pack(pady=5)
tk.Entry(root, textvariable=input_file_path, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=select_input_file).pack(pady=5)

# Dropdown for selecting the coordinate column
tk.Label(root, text="Select Coordinate Column (Latitude, Longitude):").pack(pady=5)
coord_dropdown = tk.OptionMenu(root, coordinate_column, [])
coord_dropdown.pack(pady=5)

# Dropdown for selecting the specimen name column
tk.Label(root, text="Select Specimen Name Column:").pack(pady=5)
name_dropdown = tk.OptionMenu(root, specimen_name_column, [])
name_dropdown.pack(pady=5)

# Dropdown for selecting the description column
tk.Label(root, text="Select Description Column:").pack(pady=5)
desc_dropdown = tk.OptionMenu(root, description_column, [])
desc_dropdown.pack(pady=5)

# Output folder section
tk.Label(root, text="Select Output Folder:").pack(pady=5)
tk.Entry(root, textvariable=output_folder_path, width=50).pack(pady=5)
tk.Button(root, text="Browse", command=select_output_folder).pack(pady=5)

# Zoom level section
tk.Label(root, text="Set Map Zoom Level (1-18):").pack(pady=5)
tk.Entry(root, textvariable=zoom_level_var, width=5).pack(pady=5)

# Process button
tk.Button(root, text="Generate Map", command=process_data).pack(pady=20)

# Run the application
root.mainloop()
