# S-S-python-project
Kasper Kappe 5349214

Project name: GUI for a mineral collection mapping script

Project description:
For work i did in the past, i created a script capable of reading a Mineral collection database file, interpreting the location of each sample with the use of Google Maps and MinDat APIs, and plotting each sample on an interactive map using Folium. However, this script is written in jupyter notebooks and is diffficult to use. For this project, I will make a GUI for this script to make it easier to understand, use, and more versitile. This GUI would include the ability to open the read and write excel files with file explorer, the ability to set the settings and parameters in an organised manner, keep track of progress and report errors, and more.
For now, making a GUI for the original base script was too difficult. Becouse of this, i created the GUI for a simplified version of the base script. It is capable of some of the tasks mentioned above.

Methods/required libraries:
The original collection mapping script uses Pandas to read the imput data, Nominatim to interpret location names if coördinates are not availible for a specimen, and Folium to plot the data on an interactive map. The map is then exported as an html file.
The new GUI is created using Tkinter.

Example input and output:
The original collection mapping code is provided in the file "base script". Example data for the base script is provided in the file "example data base script". The expected output of the base script using the example data is provided in the file "example output base script". 
For the GUI version of the simplified base script, example data and an example output are also provided. They can be found in the files "example data GUI simplified" and "example output GUI simplified".

Testing:
To test the functions of the script, run:"pytest test_file1" or "pytest test_file2" in the CMD. Test file 1 contains one test function that works. Test file 2 contains a second function. However, since my code requires reading excel files and user interface interaction, it was very hard to make working test functions. I tried to ask ChatGPT for help but i could'nt get more than one function to work.

