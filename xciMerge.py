from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import shutil
import glob
import os
import sys

root = Tk()
menubar = Menu(root)

class App:
    def __init__(self, master):
        frame = Frame(master)
        frame.grid(padx=20)
       
        self.title_label = Label(frame, text="nxDumpMerger v0.1.0")
        self.title_label.grid(row=0, column=0, columnspan=4, pady=10)
        
        self.input_label = Label(frame, text="Input:")
        self.input_label.grid(row=1, column=0, sticky=W)
        self.input_entry = Entry(frame)
        self.input_entry.grid(row=1, column=1, columnspan=2)
        self.merge_dump = Button(frame, text="...", command=self.get_input_entry)
        self.merge_dump.grid(row=1, column=3, padx=5)
        
        self.output_label = Label(frame, text="Output:")
        self.output_label.grid(row=2, column=0, sticky=W)
        self.output_entry = Entry(frame)
        self.output_entry.grid(row=2, column=1, columnspan=2)
        self.merge_dump = Button(frame, text="...", command=self.get_output_entry)
        self.merge_dump.grid(row=2, column=3, padx=5)

        self.delete = False
        self.delete_old_files_checkbutton = Checkbutton(frame, text="Delete original files", variable=self.delete, command=self.cb)
        self.delete_old_files_checkbutton.grid(row = 3, column = 0, columnspan=4)

        self.merge_dump = Button(frame, text="Merge Dump", command=self.cmd_merge_dump)
        self.merge_dump.grid(row=4, column=0, columnspan=2, pady=10)

        self.button = Button(frame, text="Quit", command=frame.quit)
        self.button.grid(row=4, column=2, columnspan=2)
       
        self.title_label = Label(frame, text="written by emiyl")
        self.title_label.grid(row=5, column=0, columnspan=4)
        
    def cb(self):
        self.delete = not self.delete
        print(self.delete)
        
    def cmd_merge_dump(self):
        input_file     = self.input_entry.get()
        output_file    = self.output_entry.get() + input_file[input_file.rfind('/') - len(input_file) + 1:][:input_file.rfind('.') - len(input_file) + 1] + "xci"
        file_path      = input_file[:input_file.rfind('.') - len(input_file) + 1] + "xc"
        filename_count = 0
        
        for f in glob.glob(file_path + "*"):
            if f[f.rfind('.') - len(f) + 1:][2:].isdigit():
                filename_count += 1
        
        with open(output_file,'wb') as wfd:
            for i in range(filename_count):
                f = file_path + str(i)
                with open(f,'rb') as fd:
                    shutil.copyfileobj(fd, wfd)
                 
        if self.delete:
            for i in range(filename_count):
                os.remove(file_path + str(i))
        
    def get_input_entry(self):
        filename = filedialog.askopenfilename(initialdir="./",  title="Select your NX dump part")
        file_path = filename[:filename.rfind('.') - len(filename) + 1][2:]
        extension = filename[filename.rfind('.') - len(filename) + 1:][:2]
        part_num = filename[filename.rfind('.') - len(filename) + 1:][2:]
        filename_count = 0
        
        if not filename:
            return
        
        for f in glob.glob(file_path + "xc" + "*"):
            if f[f.rfind('.') - len(f) + 1:][2:].isdigit():
                filename_count += 1
                
        for i in range(filename_count):
            if not os.path.isfile(file_path + "xc" + str(i)):
                messagebox.showinfo("Error", "Incomplete dump. Part(s) are missing." )
                return
        
        if extension != "xc":
            messagebox.showinfo("Error", "nxDumpMerger only supports XCI format dumps at the moment.")    
            return
            
        if not part_num.isdigit():
            messagebox.showinfo("Error", "Not a valid part file.")    
            return
            
        self.input_entry.delete(0, END)
        self.input_entry.insert(0, filename)
        
        self.output_entry.delete(0, END)
        self.output_entry.insert(0, filename[:filename.rfind('/') - len(filename) + 1])
        
    def get_output_entry(self):
        dirname = filedialog.askdirectory(initialdir="./",  title="Select where you'd like to place your merged dump")
        if not dirname:
            return
        self.output_entry.delete(0, END)
        self.output_entry.insert(0, dirname)

app = App(root)
root.title("nxDumpMerger v0.1.0")
root.config(menu=menubar)
root.mainloop()