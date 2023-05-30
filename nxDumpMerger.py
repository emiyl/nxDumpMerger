from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
import shutil
import glob
import os
import sys
import time
import platform

if platform.system() == 'Windows':
    from tkinter.ttk import *
else:
    from tkinter.ttk import Progressbar

root = Tk()
version = "1.0.1"
title = f"nxDumpMerger {version}"

class App:
    instructionString = "Select one file part and nxDumpMerger will automatically select the rest."

    inOutStrings = [
        'Input:',
        'Output:'
    ]
    
    OpenButtonString = '...'

    lowerButtonStrings = [
        'Merge Dump',
        'About',
        'Quit'
    ]
    
    authorString = 'written by emiyl'

    def __init__(self, master):
        title_label = Label(text=title)
        title_label.grid(pady=10)
        
        frame = Frame(master)
        frame.grid(padx=20, column=0)
        
        for i in range(0,2):
            inOutLabel = Label(frame, text=self.inOutStrings[i])
            inOutLabel.grid(row=i+1, column=0, padx=10)
        
        self.inputEntry = Entry(frame)
        self.inputEntry.grid(row=1, column=1, columnspan=2)
        getInputButton = Button(frame, text=self.OpenButtonString, command=self.getInputEntry)
        getInputButton.grid(row=1, column=3, padx=5)
        
        self.outputEntry = Entry(frame)
        self.outputEntry.grid(row=2, column=1, columnspan=2)
        getOutputButton = Button(frame, text=self.OpenButtonString, command=self.getOutputEntry)
        getOutputButton.grid(row=2, column=3, padx=5)
        
        end = Frame(master)
        end.grid(padx=20, column=0)
        
        lowerButton = []

        button = Button(end, text=self.lowerButtonStrings[0], command=self.mergeDump)
        lowerButton.append(button)

        button = Button(end, text=self.lowerButtonStrings[1], command=About)
        lowerButton.append(button)

        button = Button(end, text=self.lowerButtonStrings[2], command=root.quit)
        lowerButton.append(button)
        
        for i in range(0,3):
            lowerButton[i].grid(row=0, column=i, padx=10, pady=10)
       
        authorLabel = Label(text=self.authorString)
        authorLabel.grid(pady=(0, 10))
        
    def mergeDump(self):
        inputFile = self.inputEntry.get()
        outputDir = self.outputEntry.get()
        
        splitPath = os.path.splitext(inputFile)
        filename  = os.path.basename(splitPath[0])
        extension = splitPath[1]
        
        if not filename or not outputDir:
            return
        
        if (extension[:3] == '.xc' or extension[:3] == '.ns') and extension[3:].isdigit():   # .xc0 or .ns0
            if extension[:3] == '.xc':
                outputFile = filename + '.xci'
            elif extension[:3] == '.ns':
                outputFile = filename + '.nsp'
                
            outputPath = os.path.join(outputDir, outputFile)
                    
        elif (filename[-3:] == 'xci' or filename[-3:] == 'nsp') and len(extension) == 3 and extension[1:].isdigit(): # .xci.00 or .nsp.00
            outputFile = filename
            outputPath = os.path.join(outputDir, outputFile)
                    
        elif not extension and len(filename) == 2 and filename.isdigit(): # folder/00
            outputFile = outputDir + '.' + 'nsp'
            outputPath = os.path.join(outputDir, outputFile)
                
        if outputPath:
            OpenFiles(self.parts, outputPath)
        
    def getInputEntry(self):
        inputFile = filedialog.askopenfilename(initialdir="./", title="Select your NX dump part")
        inputFile = os.path.realpath(inputFile)
        inputDir = os.path.dirname(inputFile)
        
        splitPath = os.path.splitext(inputFile)
        filename  = os.path.basename(splitPath[0])
        extension = splitPath[1]
        
        if not filename:
            return
        
        self.parts = []
        
        if (extension[:3] == '.xc' or extension[:3] == '.ns') and extension[3:].isdigit(): # .xc0 or .ns0
            inputFiles = glob.escape(filename + extension[:3])
            inputPath  = os.path.join(inputDir, inputFiles)
            searchPath = inputPath + '*'
            
            for f in glob.glob(searchPath):
                e = os.path.splitext(f)[1]
                if e[3:].isdigit():
                    self.parts.append(f)
                    
        elif (filename[-3:] == 'xci' or filename[-3:] == 'nsp') and len(extension) == 3 and extension[1:].isdigit(): # .xci.00 or .nsp.00
            inputFiles = filename + '.'
            inputPath  = os.path.join(inputDir, inputFiles)
            searchPath = inputPath + '*'
            
            for f in glob.glob(searchPath):
                e = os.path.splitext(f)[1]
                if e[1:].isdigit():
                    self.parts.append(f)
                    
        elif not extension and len(filename) == 2 and filename.isdigit(): # folder/00
            inputFiles = ''
            inputPath  = os.path.join(inputDir, inputFiles)
            searchPath = inputPath + '*'
            
            for f in glob.glob(searchPath):
                n, e = os.path.splitext(f)
                n = os.path.basename(n)
                if not e and len(n) == 2 and n.isdigit():
                    self.parts.append(f)
                    
        try:
            if len(self.parts) < 1:
                WrongTypeError()
                return
        except:
            WrongTypeError()
            return
            
        self.inputEntry.delete(0, END)
        self.inputEntry.insert(0, inputFile)
        
        if not self.outputEntry.get():
            self.outputEntry.delete(0, END)
            self.outputEntry.insert(0, inputDir)
        
    def getOutputEntry(self):
        dirname = filedialog.askdirectory(initialdir="./", title="Select where you'd like to place your merged dump")
        dirname = os.path.realpath(dirname)
        if not dirname:
            return
        self.outputEntry.delete(0, END)
        self.outputEntry.insert(0, dirname)
        
class WrongTypeError:
    titleString = 'Error'
    strings = [
        'Parts must be in one of the following formats:',
        ' - file.xc0, file.xc1, file.xc2, etc',
        ' - file.xci.00, file.xci.01, file.xci.02, etc',
        ' - file.ns0, file.ns1, file.ns2, etc',
        ' - file.nsp.00, file.nsp.01, file.nsp.02, etc',
        ' - folder/00, folder/01, folder/02, etc',
    ]
    
    def __init__(self):
        errorTk = Tk()
        errorTk.title(self.titleString)
        self.createWindow(errorTk)

    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)
        
        strCount = len(self.strings)
        
        for i in range(0,strCount):
            self.intro_label = Label(frame, text=self.strings[i], anchor=E, justify=LEFT, wraplength=400)
            self.intro_label.grid(row=i, column=0, sticky="W", pady=0)
            
        button = Button(frame, text='OK', command=master.destroy)
        button.grid(row=strCount+1, column=0, pady=(10,0))
        
class OpenFiles:
    titleString = 'Merging Files'

    def __init__(self, parts, outputPath):
        self.parts      = parts
        self.outputPath = outputPath
        
        self.openFilesTk = Tk()
        self.openFilesTk.title(self.titleString)
        self.createWindow(self.openFilesTk)
        
        self.initVar()
        self.startMerge()
    
    def initVar(self):
        self.totalSize = 0
        #self.speed     = 0
        #self.totalTime = 0
        self.fileSize  = []
        
        for (i, f) in enumerate(self.parts):
            self.fileSize.append(os.path.getsize(f))
            self.totalSize += self.fileSize[i]
            
        #self.bytesRemaining = self.totalSize
        self.bytesWritten   = 0

    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10, column=0)
        
        progressLabel = Label(frame, text="Progress")
        progressLabel.grid(columnspan=2)
        
        self.currentPart = 0
        self.currentByte = 0
        #eta = 0
        
        self.partProgressBar = Progressbar(frame, orient = HORIZONTAL, mode = 'determinate')
        self.partProgressBar.grid(row=0, column=0)
        
        self.fileProgressBar = Progressbar(frame, orient = HORIZONTAL, mode = 'determinate')
        self.fileProgressBar.grid(row=1, column=0, padx=20)
       
        self.partLabel = Label(frame)
        self.partLabel.grid(row=0, column=1, pady=10)
       
        self.fileLabel = Label(frame)
        self.fileLabel.grid(row=1, column=1, pady=10)
        
        #self.speedLabel = Label(frame, text="Speed:")
        #self.speedLabel.grid(columnspan=2)
        
        #self.etaLabel = Label(frame, text="ETA:")
        #self.etaLabel.grid(columnspan=2)
        
    def updateWindow(self):
        fileProgress = self.currentByte / self.fileSize[self.currentPart]
        partProgress = self.bytesWritten / self.totalSize
        
        self.fileProgressBar['value'] = 100 * fileProgress
        self.partProgressBar['value'] = 100 * partProgress
        
        fileProgressStr = fileProgress * 100
        fileProgressStr = round(fileProgressStr, 1)
        fileProgressStr = str(fileProgressStr)
        
        currentPartStr = self.currentPart + 1
        currentPartStr = str(currentPartStr)
        partCountStr   = str(self.partCount)
        
        #speedStr = self.speed / 1024**2
        #speedStr = str(int(speedStr))
        
        #timeStr = self.timeRemaining
        #if timeStr > 3599:
        #    timeStr = time.strftime('%H:%M:%S', time.gmtime(timeStr))
        #else:
        #    timeStr = time.strftime('%M:%S', time.gmtime(timeStr))
        
        strings = [
            fileProgressStr + '%',
            currentPartStr + '/' + partCountStr,
            #'Speed: ' + speedStr + ' MB/s',
            #'ETA: ' + timeStr
        ]
            
        self.fileLabel.config(text=strings[0])
        self.partLabel.config(text=strings[1])
        #self.speedLabel.config(text=strings[2])
        #self.etaLabel.config(text=strings[3])
        
        self.openFilesTk.update()

    def startMerge(self):
        self.currentByte = 0
        self.partTime    = 0
        self.partCount   = len(self.parts)
        with open(self.outputPath,'wb') as fdst:
            for (i, f) in enumerate(self.parts):
                self.currentPart = i
                self.currentByte = 0
                
                with open(f,'rb') as fsrc:
                    self.copyfileobj_readinto(fsrc, fdst)

    def copyfileobj_readinto(self, fsrc, fdst, length=0):
        READINTO_BUFSIZE = 1024 * 1024
        fsrc_readinto = fsrc.readinto
        fdst_write = fdst.write

        if not length:
            try:
                file_size = os.stat(fsrc.fileno()).st_size
            except OSError:
                file_size = READINTO_BUFSIZE
            length = min(file_size, READINTO_BUFSIZE)
            
        timeLoops  = []
        byteLoops  = []
        speedLoops = []
        counter    = 0

        with memoryview(bytearray(length)) as mv:
            while True:
                #start = time.time()
                n = fsrc_readinto(mv)
                if not n:
                    break
                if n < length:
                    with mv[:n] as smv:
                        fdst.write(smv)
                else:
                    fdst_write(mv)
                #end = time.time()
                
                #t = end - start
                
                #timeLoops.insert(0, t)
                #byteLoops.insert(0, n)
                
                #if len(timeLoops) > 100:
                #    timeLoops.remove(timeLoops[100])
                #if len(byteLoops) > 100:
                #    byteLoops.remove(byteLoops[100])
                
                #avgTime = sum(timeLoops) / len(timeLoops)
                #avgByte = sum(byteLoops) / len(byteLoops)
                
                #if avgTime > 0:
                #    speed = avgByte / avgTime
                #    speedLoops.insert(0, speed)
                
                #    if len(speedLoops) > 100:
                #        speedLoops.remove(speedLoops[100])
                    
                #if len(speedLoops) > 0:
                #    self.speed = sum(speedLoops) / len(speedLoops)
                #    self.speed = self.speed
                #else:
                #    self.speed = 0
                
                #self.partTime       += t
                #self.totalTime      += t
                self.currentByte    += n
                self.bytesWritten   += n
                #self.bytesRemaining -= n
                
                #if self.speed > 0:
                #    self.timeRemaining = self.bytesRemaining / self.speed
                #else:
                #    self.timeRemaining = 9999
                
                counter += 1
                if counter > 10:
                    self.updateWindow()
                    counter = 0
                
        self.updateWindow()
        
class About:
    titleString = 'About nxDumpMerger'
    strings = [
        'nxDumpMerger is a simple merging application developed by emiyl, designed to be used with nxdumptool.',
        'To select dump parts, select one file from a dump. nxDumpMerger will then detect all other dumps in the directory.',
        'Parts must be in one of the following formats:'
    ]
    formats = [
        ' - file.xc0, file.xc1, file.xc2, etc',
        ' - file.xci.00, file.xci.01, file.xci.02, etc',
        ' - file.ns0, file.ns1, file.ns2, etc',
        ' - file.nsp.00, file.nsp.01, file.nsp.02, etc',
        ' - folder/00, folder/01, folder/02, etc'
    ]
    
    def __init__(self):
        aboutTk = Tk()
        aboutTk.title(self.titleString)
        self.createWindow(aboutTk)

    def createWindow(self, master):
        frame = Frame(master)
        frame.grid(padx=20, pady=10)
        
        strCount = len(self.strings)
        fmtCount = len(self.formats)
        
        for i in range(0,strCount):
            label = Label(frame, text=self.strings[i], anchor=E, justify=LEFT, wraplength=400)
            label.grid(row=i, column=0, sticky="W", pady=2)
        
        for i in range(0, fmtCount):
            label = Label(frame, text=self.formats[i], anchor=E, justify=LEFT, wraplength=400)
            label.grid(row=strCount+i, column=0, sticky="W", pady=0)
            
        button = Button(frame, text='OK', command=master.destroy)
        button.grid(row=strCount+fmtCount+1, column=0, pady=(10,0))

app = App(root)
root.title(title)
root.mainloop()
