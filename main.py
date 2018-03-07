#################################################

__author__ 	= "Jon Metzger"
__date__ 	= "03/07/18"
__copyright__ 	= "Copyright 2018"
__company__ 	= "Applause"
__version__ 	= "1.0"
__status__ 	= "Development"

#################################################

from Tkinter import *
import ttk
import csv
from csv import DictReader
import shutil
import os
from collections import OrderedDict
import brewery
from brewery import ds
import sys
import sqlite3
import sys
from Tkinter import *
from tkFileDialog import askopenfile
from tkFileDialog import askopenfilename
import untangle
from subprocess import *
import subprocess
import tempfile
import time
import ttk
import tkFont
import os
import Tkinter
import inspect
import operator
import Tkinter as tk

#################################################

'''
Set Globals
'''
top = None

lgrey = '#d9d9d9'
black = '#000000'
white = '#ffffff'

font_titleMain = "-family {Times New Roman} -size 30 -weight bold -slant roman -underline 0 -overstrike 0"
font_title = "-family {Times New Roman} -size 20 -weight bold -slant roman -underline 0 -overstrike 0"
font_table = "-family {Bitstream Vera Serif} -size 14 -weight normal -slant roman -underline 0 -overstrike 0"
font_results = "-family {Bitstream Vera Serif} -size 20 -weight normal -slant roman -underline 0 -overstrike 0"

finalTable = []
bugs = []

filter_testers = None
filter_countries = None
filter_devices = None

countries = ["All Countries", "US", "GB", "JP"]
devices = ["All Devices", "iPhone 4", "iPhone 4S", "iPhone 5", "Galaxy S3", "Galaxy S4", "Nexus 4",  "Droid Razor", "Droid DNA", "HTC One", "iPhone 3"]
testers = ["All Users", "Miguel Bautista", "Michael Lubavin", "Leonard Sutton", "Taybin Rutkin", "Mingquan Zheng", "Stanley Chen", "Lucas Lowry", "Sean Wellington", "Darshini Thiagarajan"]

# all csv documents
directory = 'orig/'
bugsCSV = directory +'bugs.csv'
devicesCSV = directory + 'devices.csv'
tester_deviceCSV = directory + 'tester_device.csv'
testersCSV = directory + 'testers.csv'

# remaining columsns
description = dict()
firstName = dict()
lastName = dict()
country = dict()
lastLogin = dict()

#################################################

'''
places results in log file
'''
def logging(logMessage):


    ### WHERE TO ORGANIZE LOG BY BUG EXPERIENCE
    ### TODO FOR FUTURE PROJECT

    old_stdout = sys.stdout
    sys.stdout = log_file
    print "\nRESULT: [ " +  logMessage + " ]"
    sys.stdout = old_stdout

'''
import CSV onto the table and matches onto the table
'''
def importCSV(self):
    global log_file
    log_file = open("logging.log","w")
    with open(devicesCSV, 'r') as f:
        reader = csv.reader(f)
        reader.next()
        for col in reader:
            description[col[0]] = col[1]


    with open(testersCSV, 'r') as f:
        reader = csv.reader(f)
        reader.next()
        for col in reader:
            firstName[col[0]] = col[1]
            lastName[col[0]] = col[2]
            country[col[0]] = col[3]
            lastLogin[col[0]] = col[4]

    with open(bugsCSV, 'r') as f2:
        finalReader = csv.reader(f2)
        finalReader.next()
        for finalColumns in finalReader:
            bugID = finalColumns[0]
            devID = finalColumns[1]
            testID = finalColumns[2]

            # match each row with respective Primary Key
            finalColumns.append( description[devID] )
            finalColumns.append( firstName[testID] + " " + lastName[testID] )
            finalColumns.append( country[testID] )
            finalColumns.append( lastLogin[testID] )

            # Populate Table
            self.list_table.insert('', END, values=finalColumns)
            
            # Add to final table
            finalTable.append( finalColumns )

#################################################

'''
filter category of Testers
'''
def filterTesters():
    global filteredTesters, filter_select_testers
    filter_select_testers = filter_testers.get()
    filteredTesters = []

    if filter_select_testers == testers[0]:
        for element in finalTable:
            filteredTesters.append(element)
            top.list_table.insert('', END, values=(element)) 

    i = 1
    while(i<len(testers)):
        if filter_select_testers == testers[i]:
            filt = filter(lambda x: True if (x[4] == filter_select_testers) else False, finalTable)
            for element in filt:
                filteredTesters.append(element)
                top.list_table.insert('', END, values=(element)) 
        i = i + 1
'''
filter category of Countries
'''
def filterCountries():
    global filteredCountries, filter_select_country
    filter_select_country = filter_countries.get()
    filteredCountries = []

    if filter_select_country == countries[0]:
        for element in filteredTesters:
            filteredCountries.append(element)

    i = 1
    while(i < len(countries)):
        
        if filter_select_country == countries[i]:
            filt = filter(lambda x: True if (x[5] == filter_select_country) else False, filteredTesters)
            for element in filt:
                filteredCountries.append(element)
                top.list_table.insert('', END, values=(element)) 
        i = i + 1

'''
filter category of Devices
'''
def filterDevices():
    global filteredDevices, filter_select_device, filteredCountries
    filter_select_device = filter_devices.get()
    filteredDevices = []

    if filter_select_device == devices[0]:
        for element in filteredCountries:
            top.list_table.insert('', END, values=(element))

    i = 1
    while(i < len(devices)):
        if filter_select_device == devices[i]:
            filt = filter(lambda x: True if (x[3] == filter_select_device) else False, filteredCountries)
            for element in filt:
                filteredDevices.append(element)
                top.list_table.insert('', END, values=(element)) 
        i = i + 1

#################################################

'''
Count rows in TreeView
'''
def get_all_children(tree, item=''):
    children = tree.get_children(item)
    for child in children:
        children += get_all_children(tree, child)
    return children

'''
count how many rows in table criteria
'''
def countExperience():
    w = top.list_table
    bugs = str(len(get_all_children(w)))
    top.count_label.configure(text=bugs + " Bugs")

#################################################

'''
Reset the search again to default values
'''
def initSearch():
    filter_testers.set(testers[0])
    filter_devices.set(devices[0])
    filter_countries.set(countries[0])
    top.search_testers.configure(state="readonly")
    top.search_devices.configure(state="readonly")
    top.search_countries.configure(state="readonly")
    clearTable()
    for element in finalTable:
        top.list_table.insert('', END, values=(element)) 
    countExperience()

'''
Filter the criteria to match input
'''
def filtCriteria(widget):
    global filter_select_testers, filter_select_device, filter_select_country, bugs
    viewTable()
    #clearResults()

    country_output = filter_select_country
    tester_output = filter_select_testers
    
    # All Countries
    if filter_select_country != countries[0]:
        country_output = filter_select_country
        tester_output = ""
    else:
        country_output = ""
    
    w = top.list_table
    bugs = str(len(get_all_children(w)))
    
    output = tester_output + country_output + " filed " + bugs + " Bugs for " + filter_select_device
    logging(output)
    widget.insert(0, output)
    #widget.configure(text=output)

#################################################

'''
Populate the table with search criteria 
and count experience
'''
def viewTable():
    clearTable()
    updateTesters()
    updateCountries()
    updateDevices()
    countExperience()
    #print "Here"

def clearTable():
    items = top.list_table.get_children()
    # clear table for repolulation
    for item in items:
        top.list_table.delete(item)

#################################################

'''
Default result window
'''
def initResults():
    clearResults()
    top.result_table.insert(END, "Add to Results to import data")

'''
Add the results to the listbox
'''
def addResults():
    viewTable()
    filtCriteria(top.result_table)
    initSearch()

'''
reset the results window
'''
def clearResults():
    top.result_table.delete(0, END)
    updateTesters()


#################################################

'''
avoids overwriting information
'''
def searchConstraints():
    if filter_testers.get() == testers[0]:
        top.search_countries.configure(state="readonly")
    if filter_testers.get() != testers[0]:
        top.search_countries.configure(state="disabled")
    if filter_countries.get() == countries[0]:
        top.search_testers.configure(state="readonly")
    if filter_countries.get() != countries[0]:
        top.search_testers.configure(state="disabled")

'''
refresh testers to match criteria
'''
def updateTesters():
    searchConstraints()
    clearTable()
    filterTesters()
'''
refresh countries to match criteria
'''
def updateCountries():
    updateTesters()
    filterCountries()

'''
refresh testers to match criteria
'''
def updateDevices():
    filterTesters()
    clearTable()
    filterDevices()    

#################################################

'''
Function to create the gui and initialize the frames to make the application.
'''
def create_mainwindow():
    global root, top
    root = Tk()
    top = mainwindow(root)
    root.mainloop()

'''
Function to exit and shut down the application.
'''
def destroy_mainwindow():
    global w
    w.destroy()
    log_file.close()
    w = None

#################################################

'''
GUI
'''
class mainwindow:
    '''
    Initializes the application with the following frames.
    '''
    def __init__(self, top):
        width, height = root.winfo_screenwidth(), root.winfo_screenheight()
        top.title("Criteria Application")
        top.configure(highlightcolor=black, background=white, width=width/2, height=height/2)

        self.title(top)
        self.table(top)
        self.search(top)
        self.result(top)
        self.menu(top)
        importCSV(self)

    '''
	Frame for the title and top frame.
    '''
    def title(self, top):

        self.title_frame = Frame(top, relief=SUNKEN, borderwidth="1")
        self.title_frame.place(relx=0, rely=0, relheight=0.1, relwidth=1.0)

        self.title_label = Label(self.title_frame, text="Experience Calculator", font=font_titleMain)
        self.title_label.place(relx=0.5, rely=0.5, relheight=1.0, relwidth=0.5, anchor="center")

    '''
    Frame for the search criteria
    '''
    def search(self, top):
        global filter_countries, filter_devices, filter_testers
        self.search_frame = Frame(top, relief=SUNKEN, borderwidth="1")
        self.search_frame.place(relx=0, rely=0.1, relheight=0.25, relwidth=0.5)

        self.search_title = Label(self.search_frame, text="Search", font=font_title, anchor="nw")
        self.search_title.place(relx=0.01, rely=0.02, relheight=0.3, relwidth=0.25)

        filter_testers = Tkinter.StringVar();
        filter_testers.set(testers[0])
        self.search_testers_label = Label(self.search_frame, text="User:", anchor="w")
        self.search_testers_label.place(relx=0, rely=0.25, relheight=0.25, relwidth=0.25)
        self.search_testers = ttk.Combobox(self.search_frame, textvariable=filter_testers, state="readonly", values=testers)
        self.search_testers.place(relx=0.15, rely=0.3, relheight=0.13, relwidth=0.5)
        self.view_table = Button(self.search_frame, font=font_table, text="Update Table", command=viewTable)
        self.view_table.place(relx=0.7, rely=0.25, relheight=0.25, relwidth=0.25)

        filter_countries = Tkinter.StringVar();
        filter_countries.set(countries[0])
        self.search_countries_label = Label(self.search_frame, text="Country:", anchor="w")
        self.search_countries_label.place(relx=0, rely=0.5, relheight=0.25, relwidth=0.25)
        self.search_countries = ttk.Combobox(self.search_frame, textvariable=filter_countries, state="readonly", values=countries)
        self.search_countries.place(relx=0.15, rely=0.55, relheight=0.13, relwidth=0.5)

        self.add_results = Button(self.search_frame, font=font_table, text="Add to Results", command=addResults)
        self.add_results.place(relx=0.7, rely=0.5, relheight=0.25, relwidth=0.25)

        filter_devices = Tkinter.StringVar();
        filter_devices.set(devices[0])
        self.search_devices_label = Label(self.search_frame, text="Device:", anchor="w")
        self.search_devices_label.place(relx=0, rely=0.75, relheight=0.25, relwidth=0.25)
        self.search_devices = ttk.Combobox(self.search_frame, textvariable=filter_devices, state="readonly", values=devices)
        self.search_devices.place(relx=0.15, rely=0.8, relheight=0.13, relwidth=0.5)

        self.reset_search = Button(self.search_frame, font=font_table, text="Reset Table", command=initSearch)
        self.reset_search.place(relx=0.7, rely=0.75, relheight=0.25, relwidth=0.25)
    '''
    Frame for the Results output frame
    '''
    def result(self,top):
        self.result_frame = Frame(top, relief=SUNKEN, borderwidth="1")
        self.result_frame.place(relx=0.5, rely=0.1, relheight=0.25, relwidth=0.5)

        self.result_title = Label(self.result_frame, text="Results", font=font_title, anchor="w")
        self.result_title.place(relx=0.01, rely=0.01, relheight=0.25, relwidth=0.25, anchor="nw")

        self.reset_results = Button(self.result_frame, font=font_table, text="Clear", command=initResults)
        self.reset_results.place(relx=0.99, rely=0.02, relheight=0.25, relwidth=0.25, anchor="ne")

        self.result_table = Listbox(self.result_frame, relief=RIDGE, font=font_table)
        self.result_table.place(relx=0.01, rely=0.25, relheight=0.7, relwidth=0.98, anchor="nw")
        self.result_table_scrollBar = ttk.Scrollbar(self.result_table, orient="vertical", command=self.result_table.yview)
        self.result_table_scrollBar.pack(side="right", fill="y")
        self.result_table.configure(yscrollcommand=self.result_table_scrollBar.set)
        self.result_table.insert(END, "Add to Results to import data")

    '''
	Frame for the table and bottom frame
    '''
    def table(self, top):
        self.table_frame = Frame(top, relief=SUNKEN, borderwidth="1")
        self.table_frame.place(relx=0, rely=0.35, relheight=0.65, relwidth=1.0)

        self.table_title = Label(self.table_frame, text="Table", font=font_title, anchor="nw")
        self.table_title.place(relx=0.005, rely=0.01, relheight=0.25, relwidth=0.25, anchor="nw")

        self.count_label =Label(self.table_frame, font=font_table, text="Bug Experience", anchor="center")
        self.count_label.place(relx=0.5, rely=0, relheight=0.1, relwidth=0.5, anchor="n")

        header = ["bug num","dev num","test num","description","tester", "country", "last login"]
        self.list_table = ttk.Treeview(self.table_frame, columns=header, show="headings",selectmode='none')
        self.list_table.place(relx=0, rely=0.1, relheight=0.9, relwidth=1.0)
        self.list_table_scrollBar = ttk.Scrollbar(self.list_table, orient="vertical", command=self.list_table.yview)
        self.list_table_scrollBar.pack(side="right", fill="y")
        self.list_table.configure(yscrollcommand=self.list_table_scrollBar.set)
        self.list_table.column('#1', width=5, stretch=True)
        self.list_table.column('#2', width=5, stretch=True)
        self.list_table.column('#3', width=5, stretch=True)
        self.list_table.column('#4', width=75, stretch=True)
        self.list_table.column('#5', width=75, stretch=True)
        self.list_table.column('#6', width=10, stretch=True)
        self.list_table.column('#7', width=150, stretch=True)
        for col in header:
            self.list_table.heading(col, text=col.title())

    '''
    Menu bar on the top to Open Files (Source and XML) and Exit the Application.
    '''
    def menu(self, top):
        self.menuBar = Menu(top)
        self.filemenu = Menu(self.menuBar)
        self.menuBar.add_cascade(label="File", menu=self.filemenu)
        self.menuBar.add_command(label="Exit",command=top.quit)
        top.config(menu=self.menuBar)


#################################################

if __name__ == '__main__':
    create_mainwindow()
