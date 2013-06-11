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
        
        