#! /usr/bin/env python

###################################################################################

from Tkinter import *
import ttk
from ttk import *
import tkFileDialog

import os

import subprocess
import sys

###################################################################################
# Functions

class DuplicateDictionary():
    
    # Set up variables for main loop
    all_files = {} # A dictionary of all files in folder_to_search, including subfiles.Key is filename, value is path. 
    duplicate_files = {}# A dictionary of all duplicate in folder_to_search, including subfiles. Key is filename, value is string of paths where the file exists.
    ignore_list = []


    def get_duplicate_files():
        return duplicate_files
    
    
    __init__(self):
        pass
        
    def create(self, folder_to_search, ignore_items):
        # Show Progrgress window
        progress_window = Toplevel()
        progress_window.title("Duplicate Finder")
        progress_window.resizable(FALSE,FALSE)
        
        progress_frame = ttk.Frame(progress_window, padding="10 10 10 10")
        progress_frame.grid(column=0, row=0, sticky=(W, N, E, S))
        
        ttk.Label(progress_frame, text="Searching for duplicate files.").grid(column=1, row=1, padx="15", pady="15", sticky=E)
        
        progress_bar = ttk.Progressbar(progress_frame, orient=HORIZONTAL, length=200, mode='indeterminate')
        progress_bar.grid(column=1, row=2, columnspan=3)
        progress_bar.start()
        
        
        folder_to_search_str = folder_to_search.get() # Get the toplevel directory
        
        
        # Check if file exists. If not, make alert
        if not os.path.exists(folder_to_search_str):
            alert_window = Toplevel()
            alert_window.title("Duplicate Finder")
            alert_window.resizable(FALSE,FALSE)
        
            alertframe = ttk.Frame(alert_window, padding="10 10 10 10")
            alertframe.grid(column=0, row=0, sticky=(W, N, E, S))
        
            ttk.Label(alertframe, text="The path you specified does not exist. Please try again").grid(column=0, row=1, padx="15", pady="15", sticky=E)
            ttk.Button(alertframe, text="Ok", command=lambda: alert_window.destroy()).grid(column=0, row=2)
            return
         
         
        ignore_list = list(ignore_items.get().split(",")) # Get the ignore files, split by the commas, turn to list
      
        
        # Main loop- walk through directories in folder_to_search 
        for dirpath, dirnames, filenames in os.walk(folder_to_search_str):
            
            # Remove items on the ignore list
            filenames = [x for x in filenames if x not in ignore_list]
        
            # Check what the file is and what to do with it, then do it
            for file in filenames:
                if file in all_files: #If its a duplicate,
                    if file in duplicate_files: #And its already known to be a dupilcate
                        duplicate_files[file].append(dirpath) # Add its path to duplicates list
                    else: # And its not known to be a duplicate
                        duplicate_files[file] = [all_files[file],]# Add the original (in all_files), creating a list
                        duplicate_files[file].append(dirpath)# And add the current one
                        
                else: # If its not a duplicate
                    all_files[file] = dirpath # If its not a duplicate, add to all files
        
                    
        #Destory progress window            
        progress_window.destroy()
        
        displayduplicates.ready()
        
        

class DisplayDuplicates():
    
    def __init__(self):
        pass
        
    def ready(): # Activates everything
        # Display output
        #Change colors to show enabled
        file_listbox.configure(bg='#fff')
        directory_listbox.configure(bg='#fff')
        
        
        # Scrollbars
        
        # File Listbox Y scrollbar
        file_listbox_scrollbar = ttk.Scrollbar(file_listbox, orient=VERTICAL, command=file_listbox.yview)
        file_listbox_scrollbar.pack(side = RIGHT, fill=Y)
        file_listbox.configure(yscrollcommand = file_listbox_scrollbar.set)
        
        # Directory listbox Y scrollbar
        directory_listbox_scrollbar = ttk.Scrollbar(directory_listbox, orient=VERTICAL, command=directory_listbox.yview)
        directory_listbox_scrollbar.pack(side = RIGHT, fill=Y)
        directory_listbox.configure(yscrollcommand = directory_listbox_scrollbar.set)
        # Directory listbox X scrollbar
        directory_listbox_scrollbar = ttk.Scrollbar(directory_listbox, orient=HORIZONTAL, command=directory_listbox.xview)
        directory_listbox_scrollbar.pack(side = BOTTOM, fill=X)
        directory_listbox.configure(xscrollcommand = directory_listbox_scrollbar.set)
        
        # Populate file listbox
        file_listbox.delete(0, END) # Clear the box from previous searches
        for file in duplicate_files.keys():
            file_listbox.insert(END, file)
        file_listbox.selection_set(0)
        
        # Call to populate directory listbox
        update_directory_listbox(duplicate_files, file_listbox)
        
    
    # A function and binding to populate the directory listbox when file listbox is clicked
    def update_directory_listbox(self):
        
        directory_listbox.delete(0, END) # Clear the box from previous selections
        
        current_file_listbox_key = file_listbox.get(file_listbox.curselection())                
        
        for directory in duplicate_files[current_file_listbox_key]:
            directory_listbox.insert(END, directory)
 
    

    # A function to open folders when clicked on and its bindings
    def open_selected_path(self):
        
        path = directory_listbox.get(directory_listbox.curselection())
       
        if sys.platform == 'darwin':
                subprocess.check_call(['open', '--', path])
        elif sys.platform == 'linux2':
                subprocess.check_call(['gnome-open', '--', path])
        elif sys.platform == 'windows':
                subprocess.check_call(['explorer', path])
    
    
    
    '''
    # A function to open files when double clicked on and its bindings
    def open_selected_file(duplicate_files, file_listbox):
        
        directory = directory_listbox.get(directory_listbox.curselection()[1])
        print(directory)
        file = file_listbox.get(file_listbox.curselection()[1])
        print(file)
        
        
        path = os.path.join(directory, file)
        print(path)
           
        if sys.platform == 'darwin':
                subprocess.check_call(['open', '--', path])
        elif sys.platform == 'linux2':
                subprocess.check_call(['gnome-open', '--', path])
        elif sys.platform == 'windows':
                subprocess.check_call(['explorer', path])
            
    directory_listbox.bind("<Button-2>", lambda x: open_selected_file(duplicate_files, file_listbox))
    '''




# Function for Select Folder Button
def get_root_folder():
    selected_folder.set(tkFileDialog.askdirectory())
    
    
        
###################################################################################

# Windows and Frame    

    
root = Tk()

root.title("Duplicate Finder")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.geometry('+30+30')
root.minsize(750,600)



# Root-level frame
mainframe
mainframe = ttk.Frame(root, padding="30 30 30 30")
mainframe.grid(column=0, row=0, sticky=(W, N, E, S))


mainframe.columnconfigure(0, weight=1)
mainframe.columnconfigure(1, weight=2, minsize="100")
mainframe.columnconfigure(2, weight=2, minsize="100")
mainframe.columnconfigure(3, weight=1)

mainframe.rowconfigure(0, weight=0)
mainframe.rowconfigure(1, weight=0)
mainframe.rowconfigure(2, weight=0)
mainframe.rowconfigure(3, weight=0)
mainframe.rowconfigure(4, weight=0)
mainframe.rowconfigure(5, weight=0)
mainframe.rowconfigure(6, weight=0)
mainframe.rowconfigure(7, weight=0)
mainframe.rowconfigure(8, weight=2)


# UI Elements

# Folder Duplicate
ttk.Label(mainframe, text="Folder to search (including subfolders): ").grid(column=0, row=1, padx="15", pady="15", sticky=E)
selected_folder = StringVar()
ttk.Entry(mainframe, textvariable=selected_folder).grid(column=1, row=1, columnspan=2, sticky=W+E)
ttk.Button(mainframe, text="Select Folder...", command=lambda: get_root_folder()).grid(column=3, row=1, sticky=W, padx="15", pady="15")


# Ignore map (to be implemented)

ttk.Label(mainframe, text="Files to ignore (comma delimited, no spaces): ").grid(column=0, row=4, padx="15", pady="15", sticky=E)
ignore_string = StringVar()
ignore_string.set(".DS_Store,") #Set default
ttk.Entry(mainframe, textvariable=ignore_string).grid(column=1, row=4, columnspan=2, sticky=W+E)


# Execute Button
ttk.Button(mainframe, text="Search!", command= lambda: duplicatedictionary.create(selected_folder,ignore_string)).grid(column=3, row=5, sticky=(W, E), padx="20", pady="30")




horizontal_separator = ttk.Separator(mainframe, orient=HORIZONTAL)           
horizontal_separator.grid(column=0, row=6, columnspan=4, pady="30", sticky=(W, E,)) 




# File Listbox
file_listbox_label = ttk.Label(mainframe, text="Duplicate Files (click to see locations)")
file_listbox_label.grid(column=0, row=7, padx="15", pady="5", sticky=(W, S))
file_listbox = Listbox(mainframe)
file_listbox.grid(column=0, row=8, sticky=(W, N, E, S), padx=15)
file_listbox.configure(bg='#ccc') # Starts out greyed out

file_listbox.bind("<<ListboxSelect>>", lambda x: displayduplicates.update_directory_listbox())



# Directory listbox
ttk.Label(mainframe, text="Locations Found (left click to open folder, right click to open file)").grid(column=1, row=7, padx="15", sticky=(W, S), pady="5")
directory_listbox = Listbox(mainframe)
directory_listbox.grid(column=1, row=8, columnspan=3, sticky=(W, N, E, S), padx=15)
directory_listbox.configure(bg='#ccc') # Starts out greyed out

directory_listbox.bind("<<ListboxSelect>>", lambda x: displayduplicates.open_selected_path())

duplicatedictionary = DuplicateDictionary()
displayduplicates = DisplayDuplicates() # Create and empty instance so we can call its methods

###################################################################################

root.mainloop()