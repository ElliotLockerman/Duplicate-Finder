#! /usr/bin/env python
'''A Python tkinter program to find duplicate files'''

###################################################################################
# Imports

from Tkinter import *
import ttk
from ttk import *
import tkFileDialog

import os

import subprocess
import sys

from duplicate_dictionary import *
###################################################################################
# Classes



class GUI():
    ''' The GUI and main class '''
    # Function for Select Folder Button

    
    
    def __init__(self):
        ''' Creates the root window, frame, and all widgets, some disabled ''' 
        self.root = Tk()
        
        self.root.title("Duplicate Finder")
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.geometry('+50+50')
        self.root.minsize(800,600)
        
        
        
        # Menu bar
        
        # Placeholders
        def copy():
            return
        def paste():
            return
        

        # Menus- Just to block the defaults
        self.root.option_add('*tearOff', FALSE)
        self.menubar = Menu(self.root)
        self.root['menu'] = self.menubar

        
        self.menu_file = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_file, label='File')
        self.menu_file.add_command(label='Select Folder...', command=lambda: self.set_root_folder(), accelerator="o")
        self.root.bind_all('<o>',self.set_root_folder)
        self.menu_file.add_command(label='Close', command=lambda: self.quit(), accelerator="w")
        self.root.bind_all('<w>',self.quit)
        
        self.menu_edit = Menu(self.menubar)
        self.menubar.add_cascade(menu=self.menu_edit, label='Edit')
        self.menu_edit.add_command(label='Copy', command=copy)
        self.menu_edit.add_command(label='Paste', command=paste)
        

        # Set platform-specific menus
        self.window_system = self.root.tk.call('tk', 'windowingsystem')    ; # will return x11, win32 or aqua
        print(self.window_system)
        if self.window_system == 'aqua':
            
            apple = Menu(self.menubar, name='apple')
            self.menubar.add_cascade(menu=apple)

            help = Menu(self.menubar, name='help') 
            self.menubar.add_cascade(menu=help)       
        
        elif self.window_system == 'win32':
            sysmenu = Menu(self.menubar, name='system')
            self.menubar.add_cascade(menu=sysmenu)
        else:
            self.menu_help = Menu(self.menubar, name='help')
            self.menubar.add_cascade(menu=menu_help, label='Help')

        
        # Root-level frame
        self.mainframe = ttk.Frame(self.root, padding="30 30 30 30")
        self.mainframe.grid(column=0, row=0, sticky=(W, N, E, S))
        
        
        self.mainframe.columnconfigure(0, weight=1, minsize="325")
        self.mainframe.columnconfigure(1, weight=2, minsize="100")
        self.mainframe.columnconfigure(2, weight=2, minsize="100")
        self.mainframe.columnconfigure(3, weight=1, minsize="150")
        
        self.mainframe.rowconfigure(0, weight=0)
        self.mainframe.rowconfigure(1, weight=0)
        self.mainframe.rowconfigure(2, weight=0)
        self.mainframe.rowconfigure(3, weight=0)
        self.mainframe.rowconfigure(4, weight=0)
        self.mainframe.rowconfigure(5, weight=0)
        self.mainframe.rowconfigure(6, weight=0)
        self.mainframe.rowconfigure(7, weight=0)
        self.mainframe.rowconfigure(8, weight=2)
        
        
             

        # Folder to search
        ttk.Label(self.mainframe, text="Folder to search (including subfolders): ").grid(column=0, row=1, padx="15", pady="15", sticky=E)
        self.selected_folder = StringVar()
        ttk.Entry(self.mainframe, textvariable=self.selected_folder).grid(column=1, row=1, columnspan=2, sticky=W+E)
        ttk.Button(self.mainframe, text="Select Folder...", command=lambda: self.set_root_folder()).grid(column=3, row=1, sticky=W, padx="15", pady="15")
        
        
        # Ignore 
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
        
        
        # Directory listbox
        ttk.Label(self.mainframe, text="Locations Found (left click to select, double click to open folder, right click to open file)").grid(column=1, row=7, columnspan=3, padx="15", sticky=(W, S), pady="5")
        self.directory_listbox = Listbox(self.mainframe)
        self.directory_listbox.grid(column=1, row=8, columnspan=3, sticky=(W, N, E, S), padx=15)
        self.directory_listbox.configure(bg='#ccc') # Starts out greyed out
                    
        
        
              
        self.root.mainloop()
  

    def set_root_folder(self, *args):
        ''' Gets the folder to be searched '''
        self.selected_folder.set(tkFileDialog.askdirectory())
       
            
    def ready(self):
        ''' Activates everything after the folder has been searched '''
        # Display output
        #Change colors to show enabled
        self.file_listbox.configure(bg='#ffffff')
        self.directory_listbox.configure(bg='#ffffff')
        
        
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
        
        # Add bindings
        self.file_listbox.bind("<<ListboxSelect>>", lambda x: self.update_directory_listbox())
        self.directory_listbox.bind("<Double-1>", lambda x: self.open_selected_path())
        self.directory_listbox.bind("<Button-2>", lambda x: self.open_selected_file())
        
        
    
    
    def quit(self,*args):
        ''' Quits the program'''
        self.root.destroy()
    
    def update_directory_listbox(self):
        ''' Populate the directory listbox when file listbox is clicked '''

        self.directory_listbox.delete(0, END) # Clear the box from previous selections
        
        self.current_file_listbox_key = self.file_listbox.get(self.file_listbox.curselection())                
        duplicate_files = duplicatedictionary.get_duplicate_files()
             
        for directory in duplicate_files[self.current_file_listbox_key]:
            self.directory_listbox.insert(END, directory)
 
    

    def open_selected_path(self):
        ''' Opens selected folder '''
        
        path = self.directory_listbox.get(self.directory_listbox.curselection())
       
        if sys.platform == 'darwin':
                subprocess.check_call(['open', '--', path])
        elif sys.platform == 'linux2':
                subprocess.check_call(['gnome-open', '--', path])
        elif sys.platform == 'windows':
                subprocess.check_call(['explorer', path])
    
    
 

    def open_selected_file(self):
        ''' 'Opens selected file '''
        if not self.directory_listbox.curselection(): # Make sure one is selected.
            return
        
        directory = self.directory_listbox.get(self.directory_listbox.curselection())
        print(directory)
        file = self.current_file_listbox_key
        print(file)
        
        
        path = os.path.join(directory, file)
        print(path)
           
        try: 
            if sys.platform == 'darwin':
                subprocess.check_call(['open', '--', path])
            elif sys.platform == 'linux2':
                subprocess.check_call(['gnome-open', '--', path])
            elif sys.platform == 'windows':
                subprocess.check_call(['explorer', path])
        except subprocess.CalledProcessError: # If the file cannot be opened. 
            self.show_alert("This file cannot be opened.")

    
    def show_progress_window(self):
        ''' Show Progress window '''
        self.progress_window = Toplevel()
        self.progress_window.title("Duplicate Finder")
        self.progress_window.resizable(FALSE,FALSE)
        
        self.progress_frame = ttk.Frame(self.progress_window, padding="10 10 10 10")
        self.progress_frame.grid(column=0, row=0, sticky=(W, N, E, S))
        
        ttk.Label(self.progress_frame, text="Searching for duplicate files.").grid(column=1, row=1, padx="15", pady="15", sticky=E)
        
        self.progress_bar = ttk.Progressbar(self.progress_frame, orient=HORIZONTAL, length=200, mode='indeterminate')
        self.progress_bar.grid(column=1, row=2, columnspan=3)
        self.progress_bar.start()
                
    def destroy_progress_window(self):
        ''' Destroys progress window '''
        self.progress_window.destroy()

        
    def show_alert(self,alert_text):
        ''' Shows an alert window. The argument is the text. There is also a button to hide the window, with the text "ok" '''        
        alert_window = Toplevel()
        alert_window.title("Duplicate Finder")
        alert_window.resizable(FALSE,FALSE)
        
        alertframe = ttk.Frame(alert_window, padding="10 10 10 10")
        alertframe.grid(column=0, row=0, sticky=(W, N, E, S))
        
        ttk.Label(alertframe, text=alert_text).grid(column=0, row=1, padx="15", pady="15", sticky=E)
        ttk.Button(alertframe, text="Ok", command=lambda: alert_window.destroy()).grid(column=0, row=2)
       
        
###################################################################################
# Create Instances
duplicatedictionary = DuplicateDictionary() # Create and empty instance so we can call its methods
gui = GUI() # Aaaaand... start her up!

