from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import shutil
import glob
import os
import sys
import time
import platform

if platform.system() == "Windows":
    from tkinter.ttk import *
else:
    from tkinter.ttk import Progressbar

root = Tk()
version = "0.3.4"

def copyfileobj(fsrc, fdst, length=0):
    try:
        if "b" in fsrc.mode and "b" in fdst.mode and fsrc.readinto:
            return _copyfileobj_readinto(fsrc, fdst, length)
    except AttributeError:
        pass

    if not length:
        length = shutil.COPY_BUFSIZE

    fsrc_read = fsrc.read
    fdst_write = fdst.write

    copied = 0
    while True:
        buf = fsrc_read(length)
        if not buf:
            break
        fdst_write(buf)
        copied += len(buf)

READINTO_BUFSIZE = 1024 * 1024

def _copyfileobj_readinto(fsrc, fdst, length=0):
    fsrc_readinto = fsrc.readinto
    fdst_write = fdst.write

    if not length:
        try:
            file_size = os.stat(fsrc.fileno()).st_size
        except OSError:
            file_size = READINTO_BUFSIZE
        length = min(file_size, READINTO_BUFSIZE)

    copied = 0
    with memoryview(bytearray(length)) as mv:
        while True:
            n = fsrc_readinto(mv)
            if not n:
                break
            elif n < length:
                with mv[:n] as smv:
                    fdst.write(smv)
            else:
                fdst_write(mv)
            copied += n
            file_progress = 100 * (copied / file_size)
    
    
class App:
    def __init__(self, master):
        self.title_label = Label(text="nxDumpMerger v" + version)
        self.title_label.grid(pady=10)
        
        frame = Frame(master)
        frame.grid(padx=20, column=0)
        
        self.input_label = Label(frame, text="Input:")
        self.input_label.grid(row=1, column=0, padx=10)
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
        
        end = Frame(master)
        end.grid(padx=20, column=0)

        self.merge_dump = Button(end, text="Merge Dump", command=self.cmd_merge_dump)
        self.merge_dump.grid(row=0, column=0, pady=10, padx=10)

        self.merge_dump = Button(end, text="Help", command=self.show_help)
        self.merge_dump.grid(row=0, column=1, padx=10)

        self.merge_dump = Button(end, text="Quit", command=root.quit)
        self.merge_dump.grid(row=0, column=2, padx=10)
       
        self.title_label = Label(text="written by emiyl")
        self.title_label.grid(pady=(0, 10))
        
    def show_help(self):
        help = Tk()
        help.title("nxDumpMerger Help")
        help_win = Help(help)
        
    def cmd_merge_dump(self):
        input_file = self.input_entry.get()
        extension  = input_file[input_file.rfind('.') - len(input_file) + 1:][:2]
        
        if not input_file:
            return
        
        if extension == "xc":
            game_name = input_file[input_file.rfind('/') - len(input_file) + 1:][:input_file.rfind('.') - len(input_file) + 1] + "xci"
            output_file = self.output_entry.get() + game_name
            file_path   = input_file[:input_file.rfind('.') - len(input_file) + 1] + "xc"
            part_count  = 0
            
            for f in glob.glob(file_path + "*"):
                if f[f.rfind('.') - len(f) + 1:][2:].isdigit():
                    part_count += 1
        else:
            file_path   = input_file[:-2]
            game_name   = input_file[:-3]
            game_name   = game_name[game_name.rfind('/') - len(game_name) + 1:]
            output_file = self.output_entry.get() + game_name
            part_count  = 0
            
            for f in glob.glob(file_path + "*"):
                f = f[-2:]
                if f.isdigit():
                    part_count += 1
                
        current_part = "0"
        
        class Merge_dump_window:
            def __init__(self, master):
                merge_frame = Frame(master)
                merge_frame.grid(padx=20, pady=10, column=0)
                
                self.title_label = Label(merge_frame, text="Progress - " + game_name)
                self.title_label.grid(columnspan=2)
                
                current_part = 0
                file_progress = 0
                eta = 0
                
                part_progress_bar = Progressbar(merge_frame, orient = HORIZONTAL, mode = 'determinate')
                part_progress_bar.grid(row=1, column=0)
                
                file_progress_bar = Progressbar(merge_frame, orient = HORIZONTAL, mode = 'determinate')
                file_progress_bar.grid(row=2, column=0, padx=20)
               
                self.part_label = Label(merge_frame)
                self.part_label.grid(row=1, column=1, pady=10)
               
                self.file_label = Label(merge_frame)
                self.file_label.grid(row=2, column=1, pady=10)
                
                self.speed_label = Label(merge_frame, text="Speed:")
                self.speed_label.grid(columnspan=2)
                
                self.eta_label = Label(merge_frame, text="ETA:")
                self.eta_label.grid(columnspan=2)
                
                master.update()
                
                total_size = 0
                speed_list = []
                for i in range(part_count):
                    x = str(i)
                    if not extension == "xc":
                        if len(x) < 2:
                            x = "0" + str(i)
                    f = file_path + x
                    total_size = total_size + os.stat(f).st_size
                    
                bytes_remaining = total_size
                
                with open(output_file,'wb') as wfd:
                    for i in range(part_count):
                        x = str(i)
                        if not extension == "xc":
                            if len(x) < 2:
                                x = "0" + str(i)
                        f = file_path + x
                        with open(f,'rb') as fd:
                            current_part = i
                            self.part_label.config(text=str(current_part + 1) + "/" + str(part_count))
                            file_progress = 0

                            READINTO_BUFSIZE = 1024 * 1024
                                
                            try:
                                if "b" in fd.mode and "b" in wfd.mode and fd.readinto:
                                        fsrc_readinto = fd.readinto
                                        fdst_write = wfd.write
                                        
                                        length = 0
                                        try:
                                            file_size = os.stat(fd.fileno()).st_size
                                        except OSError:
                                            file_size = READINTO_BUFSIZE
                                        length = min(file_size, READINTO_BUFSIZE)

                                        copied = 0
                                        elapsed = 0
                                        bytes_transferred = 0
                                        timer = 501
                                        
                                        with memoryview(bytearray(length)) as mv:
                                            while True:
                                                timer = timer + 1
                                                
                                                start = time.time()
                                                
                                                file_progress = copied / file_size
                                                part_progress = (total_size - bytes_remaining) / total_size
                                                file_progress_bar['value'] = 100 * file_progress
                                                part_progress_bar['value'] = 100 * part_progress
                                                self.file_label.config(text=str(round(100 * file_progress, 1)) + "%")
                                                master.update()
                                                
                                                n = fsrc_readinto(mv)
                                                if not n:
                                                    break
                                                elif n < length:
                                                    with mv[:n] as smv:
                                                        wfd.write(smv)
                                                else:
                                                    fdst_write(mv)
                                                copied += n
                                                
                                                end = time.time()
                                                elapsed = elapsed + end - start
                                                bytes_transferred = bytes_transferred + n
                                                
                                                bytes_remaining = bytes_remaining - n
                                                megabytes_remaining = bytes_remaining / 1000000
                                                
                                                if timer > 500:
                                                    megabytes = bytes_transferred / 1000000
                                                    
                                                    speed = megabytes / elapsed
                                                    speed_list.append(speed)
                                                    avg_speed = sum(speed_list)/len(speed_list)
                                                    
                                                    time_remaining = int(megabytes_remaining / avg_speed)
                                                    
                                                    self.speed_label.config(text="Speed: " + str(round(speed, 1)) + "MB/s")
                                                    
                                                    seconds_remaining = int(time_remaining % 60)
                                                    if seconds_remaining < 10:
                                                        seconds_remaining = '0' + str(seconds_remaining)
                                                    else:
                                                        seconds_remaining = str(seconds_remaining)
                                                    minutes_remaining = str(int(time_remaining / 60))
                                                    
                                                    self.eta_label.config(text="ETA: " + minutes_remaining + ":" + seconds_remaining)
                                                    
                                                    elapsed = 0
                                                    bytes_transferred = 0
                                                    timer = 0
                            except AttributeError:
                                pass

                            length = shutil.COPY_BUFSIZE

                            fsrc_read = fd.read
                            fdst_write = wfd.write

                            copied = 0
                            while True:
                                buf = fsrc_read(length)
                                if not buf:
                                    break
                                fdst_write(buf)
                                copied += len(buf)
                
                            
                    
        merge = Tk()
        merge.title("Progress")
        merge_win = Merge_dump_window(merge)
        merge.destroy()
        
    def get_input_entry(self):
        filename = filedialog.askopenfilename(initialdir="./", title="Select your NX dump part")
        extension = filename[filename.rfind('.') - len(filename) + 1:][:2]
        
        if not filename:
            return
            
        if extension == "xc":
            file_path = filename[:filename.rfind('.') - len(filename) + 1][2:]
            part_num = filename[filename.rfind('.') - len(filename) + 1:][2:]
            part_count = 0
            
            for f in glob.glob(file_path + "xc" + "*"):
                if f[f.rfind('.') - len(f) + 1:][2:].isdigit():
                    part_count += 1
                    
            for i in range(part_count):
                if not os.path.isfile(file_path + "xc" + str(i)):
                    messagebox.showinfo("Error", "Incomplete dump. Part(s) are missing.")
                    return
                
            if not part_num.isdigit():
                messagebox.showinfo("Error", "This file is either not a valid part file or has not been named correctly. Please view the Help tab for more information.")
                return
        else:
            file_path = filename[:-2]
            part_count = 0
            
            for f in glob.glob(file_path + "/*"):
                f = f[-2:]
                if f.isdigit():
                    part_count += 1
            
            if part_count == 0:
                messagebox.showinfo("Error", "This file is either not a valid part file or has not been named correctly. Please view the Help tab for more information.")
                return
                    
            for i in range(part_count):
                x = str(i)
                if len(x) < 2:
                    x = "0" + str(i)
                if not os.path.isfile(file_path + x):
                    messagebox.showinfo("Error", "Incomplete dump. Part(s) are missing." )
                    return
            
        self.input_entry.delete(0, END)
        self.input_entry.insert(0, filename)
        
        if not self.output_entry.get():
            self.output_entry.delete(0, END)
            self.output_entry.insert(0, filename[:filename.rfind('/') - len(filename) + 1])
        
    def get_output_entry(self):
        dirname = filedialog.askdirectory(initialdir="./", title="Select where you'd like to place your merged dump")
        if not dirname:
            return
        dirname += '/'
        self.output_entry.delete(0, END)
        self.output_entry.insert(0, dirname)
        
class Help:
    def __init__(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)
       
        self.intro_label = Label(frame, text="To select dump parts, select one file from a dump. nxDumpMerger will then detect all other dumps in the directory.", anchor=E, justify=LEFT, wraplength=400)
        self.intro_label.grid(row=1, column=0, sticky="W")
       
        self.nsp_label = Label(frame, text="NSPs should be in the format game.nsp/00, game.nsp/01, game.nsp/02 and so on, where game.nsp is a folder.", anchor=E, justify=LEFT, wraplength=400)
        self.nsp_label.grid(row=3, column=0, sticky="W")
       
        self.xci_label = Label(frame, text="XCIs should be in the format game.xc0, game.xc1, game.xc2 and so on.", anchor=E, justify=LEFT, wraplength=400)
        self.xci_label.grid(row=4, column=0, sticky="W")
       
        self.version_label = Label(frame, text="nxDumpMerger is a simple merging application developed by emiyl, designed to be used with nxdumptool.", anchor=E, justify=LEFT, wraplength=400)
        self.version_label.grid(row=5, column=0, sticky="W")

app = App(root)
root.title("nxDumpMerger v" + version)
root.mainloop()
