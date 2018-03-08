# Criteria Matcher
The assignment was to create an application to match Testers based on search Criteria. I took a different approach by viewing the criteria on the table, then inserting it into the Results table. This is then pushed into a log when exiting the application for the user to analyze. This application focuses on individual searches to be added to a list. The action I omitted was to organize the listbox by experience. Based on my design, it was cleaner to list the results by addition than by number sorting. I have included the menu bar to later include additional components.

## Author
Jonathan Metzger

## Pre-requisites
'''
install brewery
install untangle
''''

## Running the Application
```
$ python main.py
```
A user can select a User or Country followed by Updating the Table and/or Adding to Results. They have the option to select a device, or only a device without the previous specification, to specify the search criteria.
- Updating the table prints the criteria on the table below
- Adding to Results prints experience count to results and clears the table/search criteria
- Reset Table resets the tablet to initial search engine
- Clear clears the Result table, but still saves in log

## Documents
- bugs.csv
- devices.csv
- tester_device.csv
- testers.csv

- main.py
- README.md
- logging.log

## Task
- [X] Make GUI
- [X] Parse CSV and Sort onto table
- [X] Search Bar with Button and Enter Key
- [X] Dropdown menu with Criteria Countries and Devices
- [X] Result Section
- [X] Output selection information
- [X] Treeview only shows values based on checkbox Country and Device (default=all,all)
- [X] Search for a keyword and prints only those rows
- [X] Count experience number (duplicate rows for devices and testers)
- [X] Data: Tester1, Tester2, etc. onto Result Table
- [X] Result: "User's Name: Experience"
- [X] Logging
- [ ] Rank Experience

## Functions

### logging(logMessage)

Outputs result into a log that will be created after exiting application

### importCSV(self)

Import CSV documents and sort into application table

### filterTesters()

Organize based on User/Tester input

### filterCountries()

Organize based on Country input

### filterDevices()

Organize based on Device input

### get_all_children()

Count TreeView rows

### countExperience()

Set experience count to be displayed

### initSearch()

Reset search criteria

### filtCriteria(widget)

Match input and output results

### viewTable()

Update table with criteria search

### clearTable()

Reset Table to all users

### initResults()

Reset Results table

### addResults()

Add Result Output to Table

### clearResults()

Erase result table

### SearchConstraints()

Makes sure criteria doesn't override (Testers and Countries)

### updateTesters()

Outputs testers to match criteria

### updateCountries()

Outputs countries to match criteria

### updateDevices()

Outputs countries to match criteria

### create_mainwindow()

creates GUI

### destroy_mainwindow()

exits GUI

### class mainwindow

GUI class
