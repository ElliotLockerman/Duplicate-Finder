#! /usr/bin/env python

###################################################################################
# Imports

from Tkinter import *
import ttk
from ttk import *
import tkFileDialog

import os

import subprocess
import sys

###################################################################################
# Classes

class DuplicateDictionary():
    
    def __init__(self):
        self.all_files = {} # A dictionary of all files in folder_to_search, including subfiles.Key is filename, value is path. 
        self.duplicate_files = {}# A dictionary of all duplicate in folder_to_search, including subfiles. Key is filename, value is string of paths where the file exists.
        self.ignore_list = []
        pass
    
    def get_duplicate_files(self):
        return self.duplicate_files
    
    def create(self, folder_to_search, ignore_items, gui):
        # Show Progrgress window
        self.progress_window = Toplevel()
        self.progress_window.title("Duplicate Finder")
        self.progress_window.resizable(FALSE,FALSE)
        
        self.progress_frame = ttk.Frame(self.progress_window, padding="10 10 10 10")
        self.progress_frame.grid(column=0, row=0, sticky=(W, N, E, S))
        
        ttk.Label(self.progress_frame, text="Searching for duplicate files.").grid(column=1, row=1, padx="15", pady="15", sticky=E)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=HORIZONTAL, length=200, mode='indeterminate')
        self.progress_bar.grid(column=1, row=2, columnspan=3)
        self.progress_bar.start()
        
        
        self.folder_to_search_str = folder_to_search.get() # Get the toplevel directory
        
        
        # Check if file exists. If not, make alert
        if not os.path.exists(self.folder_to_search_str):
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
        for self.dirpath, self.dirnames, self.filenames in os.walk(self.folder_to_search_str):
            
            # Remove items on the ignore list
            self.filenames = [x for x in self.filenames if x not in ignore_list]
        
            # Check what the file is and what to do with it, then do it
            for file in self.filenames:
                if file in self.all_files: #If its a duplicate,
                    if file in self.duplicate_files: #And its already known to be a dupilcate
                        self.duplicate_files[file].append(dirpath) # Add its path to duplicates list
                    else: # And its not known to be a duplicate
                        self.duplicate_files[file] = [self.all_files[file],]# Add the original (in all_files), creating a list
                        self.duplicate_files[file].append(self.dirpath)# And add the current one
                        
                else: # If its not a duplicate
                    self.all_files[file] = self.dirpath # If its not a duplicate, add to all files
        
                    
        #Destory progress window            
        self.progress_window.destroy()
        
        gui.ready()
        
        

class GUI():
    
    def __init__(self):
        self.root = Tk()
        
        self.root.title("Duplicate Finder")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.geometry('+30+30')
        self.root.minsize(750,600)
        
        
        
        # Root-level frame
        self.mainframe = ttk.Frame(self.root, padding="30 30 30 30")
        self.mainframe.grid(column=0, row=0, sticky=(W, N, E, S))
        
        
        self.mainframe.columnconfigure(0, weight=1)
        self.mainframe.columnconfigure(1, weight=2, minsize="100")
        self.mainframe.columnconfigure(2, weight=2, minsize="100")
        self.mainframe.columnconfigure(3, weight=1)
        
        self.mainframe.rowconfigure(0, weight=0)
        self.mainframe.rowconfigure(1, weight=0)
        self.mainframe.rowconfigure(2, weight=0)
        self.mainframe.rowconfigure(3, weight=0)
        self.mainframe.rowconfigure(4, weight=0)
        self.mainframe.rowconfigure(5, weight=0)
        self.mainframe.rowconfigure(6, weight=0)
        self.mainframe.rowconfigure(7, weight=0)
        self.mainframe.rowconfigure(8, weight=2)
        
        
        # UI Elements
        
        # Folder Duplicate
        ttk.Label(self.mainframe, text="Folder to search (including subfolders): ").grid(column=0, row=1, padx="15", pady="15", sticky=E)
        self.selected_folder = StringVar()
        ttk.Entry(self.mainframe, textvariable=self.selected_folder).grid(column=1, row=1, columnspan=2, sticky=W+E)
        ttk.Button(self.mainframe, text="Select Folder...", command=lambda: self.set_root_folder()).grid(column=3, row=1, sticky=W, padx="15", pady="15")
        
        
        # Ignore map (to be implemented)
        
        ttk.Label(self.mainframe, text="Files to ignore (comma delimited, no spaces): ").grid(column=0, row=4, padx="15", pady="15", sticky=E)
        self.ignore_string = StringVar()
        self.ignore_string.set(".DS_Store,") #Set default
        ttk.Entry(self.mainframe, textvariable=self.ignore_string).grid(column=1, row=4, columnspan=2, sticky=W+E)
        
        
        # Execute Button
        ttk.Button(self.mainframe, text="Search!", command= lambda: duplicatedictionary.create(self.selected_folder,self.ignore_string, self)).grid(column=3, row=5, sticky=(W, E), padx="20", pady="30")
        
        
        
        
        self.horizontal_separator = ttk.Separator(self.mainframe, orient=HORIZONTAL)           
        self.horizontal_separator.grid(column=0, row=6, columnspan=4, pady="30", sticky=(W, E,)) 
        
        
        
        
        # File Listbox
        self.file_listbox_label = ttk.Label(self.mainframe, text="Duplicate Files (click to see locations)")
        self.file_listbox_label.grid(column=0, row=7, padx="15", pady="5", sticky=(W, S))
        self.file_listbox = Listbox(self.mainframe)
        self.file_listbox.grid(column=0, row=8, sticky=(W, N, E, S), padx=15)
        self.file_listbox.configure(bg='#ccc') # Starts out greyed out
        
        self.file_listbox.bind("<<ListboxSelect>>", lambda x: gui.update_directory_listbox())
        
        
        
        # Directory listbox
        ttk.Label(self.mainframe, text="Locations Found (left click to open folder, right click to open file)").grid(column=1, row=7, padx="15", sticky=(W, S), pady="5")
        self.directory_listbox = Listbox(self.mainframe)
        self.directory_listbox.grid(column=1, row=8, columnspan=3, sticky=(W, N, E, S), padx=15)
        self.directory_listbox.configure(bg='#ccc') # Starts out greyed out
        
        self.directory_listbox.bind("<<ListboxSelect>>", lambda x: gui.open_selected_path())
                    
        self.root.mainloop()
        
      # Function for Select Folder Button
    def set_root_folder(self):
        self.selected_folder.set(tkFileDialog.askdirectory())
       
    # Not sure if I will need this.   
    def get_root_folder(self):
        return self.selected_folder.get()  
            
    def ready(self): # Activates everything
        # Display output
        #Change colors to show enabled
        self.file_listbox.configure(bg='#fff')
        self.directory_listbox.configure(bg='#fff')
        
        
        # Scrollbars
        
        # File Listbox Y scrollbar
        self.file_listbox_scrollbar = ttk.Scrollbar(self.file_listbox, orient=VERTICAL, command=self.file_listbox.yview)
        self.file_listbox_scrollbar.pack(side = RIGHT, fill=Y)
        self.file_listbox.configure(yscrollcommand = self.file_listbox_scrollbar.set)
        
        # Directory listbox Y scrollbar
        self.directory_listbox_scrollbar = ttk.Scrollbar(self.directory_listbox, orient=VERTICAL, command=self.directory_listbox.yview)
        self.directory_listbox_scrollbar.pack(side = RIGHT, fill=Y)
        self.directory_listbox.configure(yscrollcommand = self.directory_listbox_scrollbar.set)
        # Directory listbox X scrollbar
        self.directory_listbox_scrollbar = ttk.Scrollbar(self.directory_listbox, orient=HORIZONTAL, command=self.directory_listbox.xview)
        self.directory_listbox_scrollbar.pack(side = BOTTOM, fill=X)
        self.directory_listbox.configure(xscrollcommand = self.directory_listbox_scrollbar.set)
        
        # Populate file listbox
        self.file_listbox.delete(0, END) # Clear the box from previous searches
        for file in duplicatedictionary.duplicate_files.keys():
            self.file_listbox.insert(END, file)
        self.file_listbox.selection_set(0)
        
        # Call to populate directory listbox
        self.update_directory_listbox()
        
    
    # A function and binding to populate the directory listbox when file listbox is clicked
    def update_directory_listbox(self):
        
        self.directory_listbox.delete(0, END) # Clear the box from previous selections
        
        self.current_file_listbox_key = file_listbox.get(file_listbox.curselection())                
        
        for directory in duplicate_files[self.current_file_listbox_key]:
            self.directory_listbox.insert(END, directory)
 
    

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

###################################################################################
# Create Instances

duplicatedictionary = DuplicateDictionary() # Create and empty instance so we can call its methods
gui = GUI() # Aaaaand... start her up!
