import os
import re
import tkinter as tk
from tkinter import filedialog, messagebox
new = []
old = []
exc = []
dir_path = ''

def addOffsetAndLeadingZero(Epnum, offset):
    Epnum = int(Epnum) + offset
    if Epnum < 10:
        return '0' + str(Epnum)
    return str(Epnum)

def updeteFileNemes():
    global new
    global old
    global dir_path

    unique_new = list(set(new))
    if len(unique_new) == len(new):
        for i in range(len(old)):
            os.rename(os.path.join(dir_path, old[i]), os.path.join(dir_path, new[i]))
        tk.messagebox.showinfo(title='Rename Files', message='File names have been updated.')
    else:
        tk.messagebox.showinfo(title='Rename Files', message='There are similar file names, please correct search pattern')

def delete(i):
    global exc
    global old
    global new
    exc.append(old[i])
    old.remove(old[i])
    new.remove(new[i])
    print(i)

def rename_files():
    global new
    global old
    global exc
    global dir_path
    new = []
    old = []
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
    # Loop through all the files and rename them if they match the pattern

    for file in files:
        if 'AutoFilesRename' in file:
            continue
        if file in exc:
            continue
        x = re.search(r''+ rgx + pattern_str, file)
        if x != None:
            Epnum = x.group()
            if rgx != '':
               Epnum = Epnum.replace(rgx,'')
            sp = file.split(".")
            ext = sp.pop()
            Epnum = addOffsetAndLeadingZero(Epnum, offset)
            new_file_name = replace_str + Epnum + "."+ext
            old.append(file)
            new.append(new_file_name)

    # e = old[0].replace(ext, '')
    # entry_text.set(e)
    for i in range(len(old)-len(exc)):

        old_label = tk.Label(root,width=len(old[i])+2, text=old[i] ,bd=1, relief="sunken")
        old_label.grid(row=8+i, column=0, padx=1, pady=1, sticky=tk.W)

        new_label = tk.Label(root,width=len(new[i])+2, text=new[i],bd=1, relief= "sunken")
        new_label.grid(row=8+i, column=1, padx=1, pady=1, sticky=tk.W)

    run_button = tk.Button(root, text='Updete Files Names', command=updeteFileNemes)
    run_button.grid(row=8+i+1, column=1, padx=5, pady=5, sticky=tk.E)

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

entry_text = tk.StringVar()
replace_label = tk.Label(root, text='Replace With:')
replace_label.grid(row=2, column=0, padx=5, pady=5, sticky=tk.W)
replace_input = tk.Entry(root, width=50, textvariable=entry_text )
entry_text.set("")
replace_input.grid(row=2, column=1, padx=5, pady=5)

offset_label = tk.Label(root, text='offset (default = 0):')
offset_label.grid(row=3, column=0, padx=5, pady=5, sticky=tk.W)
offset_input = tk.Entry(root, width=50)
offset_input.grid(row=3, column=1, padx=5, pady=5)

episodeCheckbox_var = tk.IntVar()
episodeCheckbox = tk.Checkbutton(root, text='Add Episode ', variable=episodeCheckbox_var)
episodeCheckbox.grid(row=4, column=2, padx=5, pady=5, sticky=tk.E)

SeasonDirCheckbox_var = tk.IntVar()
SeasonDirCheckbox = tk.Checkbutton(root, text='Season dir', variable=SeasonDirCheckbox_var)
SeasonDirCheckbox.grid(row=4, column=3, padx=5, pady=5, sticky=tk.E)

season_label = tk.Label(root, text='Season  (default = No Season):')
season_label.grid(row=4, column=0, padx=5, pady=5, sticky=tk.W)
season_input = tk.Entry(root, width=50)
season_input.grid(row=4, column=1, padx=5, pady=5)



# Create the "Preview" button
preview_button = tk.Button(root, text='Preview', command=rename_files)
preview_button.grid(row=6, column=1, padx=5, pady=5, sticky=tk.E)



# Start the Tkinter event loop
root.mainloop()

