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
        self.ignore_list = [] # A list of all filenames to ignore
        pass
    
    def get_duplicate_files(self): # A fuction so the gui ca
        return self.duplicate_files
    
    def create(self, folder_to_search, ignore_items, gui):
        
        gui.show_progress_window()
        
        self.folder_to_search_str = folder_to_search.get() # Get the directory to search. Note: Folder to search is still StringVar()

        
        # Check if file exists. If not, show alert
        if not os.path.exists(self.folder_to_search_str):
            gui.destroy_progress_window()
            gui.show_alert("The path you specified does not exist. Please try again")
            return # Exit the function prematurely
        
        ignore_list = list(ignore_items.get().split(",")) # Get the ignore files, split by the commas, turn to list
      
        
        # Main loop- walk through directories in folder_to_search 
        for self.dirpath, self.dirnames, self.filenames in os.walk(self.folder_to_search_str):
            
            # Remove items on the ignore list
            self.filenames = [x for x in self.filenames if x not in ignore_list]
        
            # Check what the file is and what to do with it, then do it
            for file in self.filenames:
                
                if file in self.all_files: #If its a duplicate,
                    if file in self.duplicate_files: #And its already known to be a dupilcate
                        self.duplicate_files[file].append(self.dirpath) # Add its path to duplicates list
                    else: # And its not known to be a duplicate
                        self.duplicate_files[file] = [self.all_files[file],]# Add the original (in all_files), creating a list
                        self.duplicate_files[file].append(self.dirpath)# And add the current one
                        
                else: # If its not a duplicate
                    self.all_files[file] = self.dirpath # If its not a duplicate, add to all files
        
            
        gui.destroy_progress_window() #Destroy progress window            

        gui.ready() # Now that we have everything, tell the gui to put it up. 
        
        