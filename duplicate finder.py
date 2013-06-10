#! /usr/bin/env python

###################################################################################

from Tkinter import *
import ttk
from ttk import *
import tkFileDialog

import os
from shutil import move

###################################################################################
# Functions

# Function for Select Folder Button
def get_root_folder():
    selected_folder.set(tkFileDialog.askdirectory())

# Function for Search! button- main algorithm     
def search(folder_to_search, topdown=True):

    # Set up variables
    all_files = {} # A dictionary of all files in folder_to_search, including subfiles.Key is filename, value is path. 
    duplicate_files = {}# A dictionary of all duplicate in folder_to_search, including subfiles. Key is filename, value is string of paths where the file exists.
    
    # Main loop- walk through directories in folder_to_search 
    for dirpath, dirnames, filenames in os.walk(str(folder_to_search.get())):
        for file in filenames:
            if file in allfiles: #If its a duplicate,
                if file in duplicate_files #And its already known to be a dupilcate
                    duplicate_files[file].append(dirpath) # Add its path to duplicates list
                else # And its not known to be a duplicate
                    duplicate_files[file] = all_files[file]# Add the original (in all_files)
                    duplicate_files[file].append(dirpath)# And add the current one
                    
            else # If its not a duplicate
                all_files[file] = dirpath # If its not a duplicate, add to all files
                
                
    #Print output (to be replaced with GUI)
    print(all_files)
    print(duplicate_files)
    
    
###################################################################################
# Windows and Frame    

    
root = Tk()

root.title("Duplicate Finder")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry('+30+30')
root.minsize(650,350)
root.maxsize(2000,350)


# Root-level frame
mainframe = ttk.Frame(root, padding="10 30 10 10")
mainframe.grid(column=0, row=0, sticky=(W, N, E, S))

mainframe.columnconfigure(0, weight=0)
mainframe.columnconfigure(1, weight=1, minsize="100")
mainframe.columnconfigure(2, weight=1, minsize="100")
mainframe.columnconfigure(3, weight=0)

mainframe.rowconfigure(0, weight=0)
mainframe.rowconfigure(1, weight=0)
mainframe.rowconfigure(2, weight=0)
mainframe.rowconfigure(3, weight=0)
mainframe.rowconfigure(4, weight=0)
mainframe.rowconfigure(5, weight=0)



# UI Elements

# Folder Duplicate
ttk.Label(mainframe, text="Folder to search: ").grid(column=0, row=1, padx="15", pady="15", sticky=E)
selected_folder = StringVar()
ttk.Entry(mainframe, textvariable=selected_folder).grid(column=1, row=1, columnspan=2, padx="15", pady="15", sticky=W+E)
ttk.Button(mainframe, text="Select Folder...", command=lambda: get_root_folder()).grid(column=3, row=1, sticky=W, padx="15", pady="15")


# Ignore map (to be implemented)
'''
ttk.Label(mainframe, text="Files to ignore(comma delimited, no spaces): ").grid(column=0, row=4, padx="15", pady="15", sticky=E)
ignore_map = StringVar()
ignore_map.set(".DS_Store,")
ttk.Entry(mainframe, textvariable=ignore_map).grid(column=1, row=4, columnspan=2, sticky=W+E)
'''

# Execute Button
ttk.Button(mainframe, text="Search!", command= lambda: search(selected_folder)).grid(column=3, row=5, sticky=(W, E), padx="20", pady="30")

###################################################################################

root.mainloop()