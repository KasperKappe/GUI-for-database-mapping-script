##########################################################################
#original functions:
##########################################################################
import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import folium
import os

# Global variable to hold the loaded Excel data
df = None

def select_input_file():
    """
    Opens a file dialog for selecting an Excel file, loads the data into a DataFrame, 
    and updates dropdown menus with column options for user selection.

    This function uses a file dialog to prompt the user to select an Excel file (.xlsx). 
    The file is then read into a global DataFrame (`df`). Column names from the DataFrame 
    are extracted and used to populate dropdown menus for selecting columns for coordinates, 
    specimen names, and descriptions.

    Global Variables:
        df (pd.DataFrame): The global DataFrame that holds the contents of the selected file.
        input_file_path (tk.StringVar): A Tkinter variable storing the file path of the selected file.
        coordinate_column (tk.StringVar): Tkinter variable for the coordinate column selection.
        specimen_name_column (tk.StringVar): Tkinter variable for the specimen name column selection.
        description_column (tk.StringVar): Tkinter variable for the description column selection.
        coord_dropdown (tk.OptionMenu): Dropdown menu for coordinate column selection.
        name_dropdown (tk.OptionMenu): Dropdown menu for specimen name column selection.
        desc_dropdown (tk.OptionMenu): Dropdown menu for description column selection.

    Exceptions:
        Displays an error message dialog if an error occurs while loading the file.

    Returns:
        None
    """
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
    """
    Opens a directory selection dialog for the user to choose an output folder, 
    and sets the selected folder path to a Tkinter variable.

    This function prompts the user to select a folder through a dialog, 
    and stores the path of the selected folder in a Tkinter `StringVar`.

    Global Variables:
        output_folder_path (tk.StringVar): A Tkinter variable that stores the path 
                                           of the chosen output folder.

    Returns:
        None
    """
    folderpath = filedialog.askdirectory()
    output_folder_path.set(folderpath)

def process_data():
    """
    Processes the selected data and generates an interactive map with specimen markers, 
    saving the result to an HTML file.

    This function uses the selected columns for coordinates, specimen name, and description 
    from a loaded DataFrame (`df`). It retrieves user-selected settings for zoom level and output 
    folder, creates a map centered on (0, 0), and adds markers for each specimen based on 
    coordinate data. The map is saved as an HTML file in the specified output folder.

    Global Variables:
        df (pd.DataFrame): The global DataFrame containing specimen data.
        coordinate_column (tk.StringVar): Selected column for coordinates.
        specimen_name_column (tk.StringVar): Selected column for specimen names.
        description_column (tk.StringVar): Selected column for descriptions.
        zoom_level_var (tk.StringVar): The zoom level for the map, set by the user.
        output_folder_path (tk.StringVar): The path to the folder where the output HTML file will be saved.

    Raises:
        ValueError: If no data is loaded, required columns are not selected, selected columns are not 
                    in the data, the output folder is not selected, or if coordinate data is in 
                    an invalid format.

    Exceptions:
        Displays an error dialog if any unexpected error occurs during data processing.

    Returns:
        None
    """    
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

##########################################################################
#test functions:
##########################################################################

import pytest
from unittest import mock
import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox

# Assuming select_input_file is imported from your module
# from your_module import select_input_file

@pytest.fixture
def mock_tkinter_widgets():
    # Mock Tkinter widgets
    mock_input_file_path = mock.Mock()
    mock_coordinate_column = mock.Mock()
    mock_specimen_name_column = mock.Mock()
    mock_description_column = mock.Mock()
    mock_coord_dropdown = mock.Mock()
    mock_name_dropdown = mock.Mock()
    mock_desc_dropdown = mock.Mock()

    # Mock the 'menu' attribute directly inside the dropdowns
    mock_coord_dropdown.menu = mock.Mock()
    mock_name_dropdown.menu = mock.Mock()
    mock_desc_dropdown.menu = mock.Mock()

    return {
        'input_file_path': mock_input_file_path,
        'coordinate_column': mock_coordinate_column,
        'specimen_name_column': mock_specimen_name_column,
        'description_column': mock_description_column,
        'coord_dropdown': mock_coord_dropdown,
        'name_dropdown': mock_name_dropdown,
        'desc_dropdown': mock_desc_dropdown,
    }


def test_select_input_file_error(mock_tkinter_widgets):
    # Assign global variables (normally used in your function)
    global input_file_path, coordinate_column, specimen_name_column, description_column
    global coord_dropdown, name_dropdown, desc_dropdown

    # Ensure the global variables are correctly assigned
    input_file_path = mock_tkinter_widgets['input_file_path']
    coordinate_column = mock_tkinter_widgets['coordinate_column']
    specimen_name_column = mock_tkinter_widgets['specimen_name_column']
    description_column = mock_tkinter_widgets['description_column']
    coord_dropdown = mock_tkinter_widgets['coord_dropdown']
    name_dropdown = mock_tkinter_widgets['name_dropdown']
    desc_dropdown = mock_tkinter_widgets['desc_dropdown']

    # Mock filedialog.askopenfilename to return a valid path
    with mock.patch.object(filedialog, 'askopenfilename', return_value="test_file.xlsx"):
        # Mock pd.read_excel to raise an exception
        with mock.patch.object(pd, 'read_excel', side_effect=Exception("Failed to read file")):
            # Call the function and ensure an error message box is shown
            with mock.patch.object(messagebox, 'showerror') as mock_showerror:
                select_input_file()
                mock_showerror.assert_called_with("Error", "An error occurred while loading the file: Failed to read file")
