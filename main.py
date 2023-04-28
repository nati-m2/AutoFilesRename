import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox

def addOffsetAndLeadingZero(Epnum, offset):
    Epnum = int(Epnum) + offset
    if Epnum < 10:
        return '0' + str(Epnum)
    return str(Epnum)

def rename_files():
    # Get the directory path, search pattern, and replacement string from the user
    if path_input.get() == '':
        dir_path = os.getcwd()
    else:
        dir_path = path_input.get()

    if pattern_input.get() == '':
        rgx = ''
    else:
        rgx = pattern_input.get()
    pattern_str = "(\d+)"

    if offset_input.get() == '':
        offset = 0
    else:
        offset = int(offset_input.get())
    replace_str = replace_input.get()

    if season_input.get() != '':
        replace_str = replace_str + " Season " + season_input.get()

    if episodeCheckbox_var.get():
        replace_str = replace_str + " Episode "

    # Get a list of all the files in the directory
    files = os.listdir(dir_path)
    f=''
    # Loop through all the files and rename them if they match the pattern
    for file in files:
        x = re.search(r''+ rgx + pattern_str, file)
        if x != None:
            Epnum = x.group()
            if rgx != '':
               Epnum = Epnum.replace(rgx,'')
            sp = file.split(".")
            ext = sp.pop()
            Epnum = addOffsetAndLeadingZero(Epnum, offset)
            new_file_name = replace_str + Epnum + "."+ext
            # Rename the file
            os.rename(os.path.join(dir_path, file), os.path.join(dir_path, new_file_name))
            f += new_file_name+'\n'
    # Show a message box indicating that the files have been renamed
    tk.messagebox.showinfo(title='Rename Files', message='File names have been updated.')
    tk.messagebox.showinfo(title='Rename Files', message= f )

# Create a Tkinter window
root = tk.Tk()
root.title('Rename Files')

# Create the input fields
path_label = tk.Label(root, text='Path (default = current directory):')
path_label.grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
path_input = tk.Entry(root, width=50)
path_input.grid(row=0, column=1, padx=5, pady=5)

path_button = tk.Button(root, text='Select a folder', command=lambda: path_input.insert(tk.END, filedialog.askdirectory()))
path_button.grid(row=0, column=2, padx=5, pady=5)

pattern_label = tk.Label(root, text='Pattern (default = (\d+)):')
pattern_label.grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
pattern_input = tk.Entry(root, width=50)
pattern_input.grid(row=1, column=1, padx=5, pady=5)

replace_label = tk.Label(root, text='Replace With:')
replace_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
replace_input = tk.Entry(root, width=50)
replace_input.grid(row=2, column=1, padx=5, pady=5)

offset_label = tk.Label(root, text='offset (default = 0):')
offset_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
offset_input = tk.Entry(root, width=50)
offset_input.grid(row=3, column=1, padx=5, pady=5)

episodeCheckbox_var = tk.IntVar()
episodeCheckbox = tk.Checkbutton(root, text='Add Episode ', variable=episodeCheckbox_var)
episodeCheckbox.grid(row=4, column=2, padx=5, pady=5, sticky=tk.E)

season_label = tk.Label(root, text='Season  (default = No Season):')
season_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
season_input = tk.Entry(root, width=50)
season_input.grid(row=4, column=1, padx=5, pady=5)



# Create the "Run" button
run_button = tk.Button(root, text='Run', command=rename_files)
run_button.grid(row=6, column=1, padx=5, pady=5, sticky=tk.E)

# Start the Tkinter event loop
root.mainloop()

