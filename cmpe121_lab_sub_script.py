# CMPE 121 Lab Submission Script
# Author: Sam Mansfield
# 
# This script creates a dialog box that guides a user into creating a zip file
# with their lab report and lab files.
#
# How to run:
#   python cmpe121_lab_sub.py
#
# Dependencies:
#   python version 2.7.10 (probably python 2.7.x is fine)
#   Tkinter
#   tkFileDialog
#   tkMessageBox
#   os
#   shutil
#
# The dialog box is intended to take three pieces of information: user name,
# lab directory, and lab report. The name text box is used to enter the
# name of the submission. The Select Lab Directory button is used to select
# the lab directory and the Select Lab Report button is used to select the
# lab report. Output is written to the output text box. If no name is entered
# the default name is no_name. Only one lab directory can be selected so make
# sure to place all lab files into one directory and then select it.
#
# The Clean & Zip button will create a directory using the given name, copy
# the lab direcotry into name/lab, and copy the lab report into name/doc. If a 
# folder already exists with the same name the name with the next highest
# increment will be created (i.e. If no_name exists no_name1 will becreated.
# If both no_name and no_mame1 exists, no_name2 will be created and so on.)
# If no lab directory or lab report is selected an error message will be
# displayed and nothing will be created.
#
# The new directory is created in the current
# directory using the user name. For example if the user enters sam_mansfeld
# a new directory is created called sam_mansfield in the current directory.
# e.g. 
#   current directory is home
#   python dir_1/cmpe121_lab_sub.py
#   user_name created in home/user_name, not in home/dir_1/user_name
#
# The lab direcotry is then cleaned by deletiing all folders that contain
# generated code that is not necessary to build the lab.
# And finally the folder is archived into a zip folder of the same name
# and the directory that was archived is deleted.

from Tkinter import *
import tkFileDialog as tkfd
import tkMessageBox as tkmb
import os
import shutil

lab_dir = ""
report = ""

# lab_button_click: The callback function when the Select Lab Directory button
# is clicked. Prompts the user to select a lab directory and then prints 
# the directory name to the output text box.
def lab_button_click():
  global lab_dir
  lab_dir = tkfd.askdirectory();
  output_text.insert("insert", "Lab directory selected: " + lab_dir + "\n")

# report_button_click: The callback function when the Select Report button is 
# clicked. Prompts the user to select a lab report and then prints the
# report name to the output text box.
def report_button_click():
  global report
  report = tkfd.askopenfilename();
  output_text.insert("insert", "Report selected: " + report + "\n")

# zip_button_click: The callback function when the Clean & Zip button is 
# clicked. This function does the bulk of the work. It copies the
# directories into the name entered (the default name is no_name)
# then deletes all folders inside the lab directory that match
# the matches list. The name folder is then archived into a zip
# file and then the name fodler is deleted. If no lab directory
# or lab report is selected an error message is displayed and the
# function aborts.
def zip_button_click():
  if lab_dir == "" or report == "":
    tkmb.showerror("Error", "Lab directory or report not selected")
    return
  
  # Get the name from the name text box from the beginning, 1.0,
  # till the end 1.end
  name = name_text.get("1.0", "1.end")
  # Use the default name no_name if the text box is empty 
  if name == "":
    name = "no_name" 

  # Do not erase or error if the directory already exists. Instead
  # keep trying to create the folder by incrementing the name, i.e.
  # no_name, no_name1, no_name2, ...
  dir_name = name
  created = False
  i = 1
  while not created:
    if not os.path.exists(dir_name):  
      os.mkdir(dir_name)
      created = True
    else:
      dir_name = name + str(i)
      i = i + 1
  output_text.insert("insert", "Directory created: " + dir_name + "\n")
  
  # Create the doc directory and copy the report into it
  doc_dir = dir_name + "/doc" 
  os.mkdir(doc_dir)
  shutil.copy(report, doc_dir)
  output_text.insert("insert", "Report copied into: " + doc_dir + "\n")
  
  # Create the lab directory and copy the lab directory into it. Ideally
  # this would have instead just copied the lab directory into the name
  # folder, but the shutil.copytree function is a bit finicky and when
  # I attempted to do that it would error that the name directory already 
  # existed, as the function wants the name to be created the directory
  # where it should be placed. So, the simple solution was to just create
  # that directory and name it lab.
  shutil.copytree(lab_dir, dir_name + "/lab")
  output_text.insert("insert", "Lab copied into: " + dir_name + "/lab\n")

  # Delete all folders inside the lab directory that match any of the names 
  # in the matches list
  matches = ["codegentemp", "CortexM3", "Export", "Generated_Source"]
  for root, dirnames, filenames in os.walk(dir_name + "/lab"):
    for dirname in dirnames:
      if dirname in matches: 
        output_text.insert("insert", "Removing " + root + "/" + dirname + "\n")
        shutil.rmtree(root + "/" + dirname)

  # Archive the folder and give it the same name
  # If there is an archive that exists with the same name it will overwrite it
  shutil.make_archive(dir_name, "zip", dir_name)
  output_text.insert("insert", dir_name + ".zip created\n")
  
  # Delete the name folder after it was archived
  shutil.rmtree(dir_name)
  output_text.insert("insert", dir_name + " deleted\n")

# close_button_click: Callback function for the Close button. 
# Closes the application
def close_button_click():
  root.destroy()

# The following is the tkInter framework, used to create guis in Python. 
# A great guide can be found at 
# this url: http://thinkingtkinter.sourceforge.net.
# The basic concept is that you create a root using Tk(), add frames,
# add buttons or textboxes (called widgets) to the frames, and start
# the main loop. You must
# both create the widget and then use the pack function for it to appear.

# Creates the root gui window
root = Tk()
root.wm_title("CMPE 121 Lab Compressor")
root.geometry("600x400")

main_container = Frame(root)
main_container.pack(ipadx = "3m", ipady = "1m", padx = "10m", pady = "2m")

# Creates a label frame, without this it is hard to tell where the 
# textboxes are
name_container = LabelFrame(main_container, text = "Name")
name_container.pack()
name_text = Text(name_container, height = 1, width = 32)
name_text.pack()

lab_button = Button(main_container, text = "Select Lab Directory", 
                    command = lab_button_click)
lab_button.pack()

report_button = Button(main_container, text = "Select Report", 
                       command = report_button_click)
report_button.pack()

zip_button = Button(main_container, text = "Clean & Zip", 
                    command = zip_button_click)
zip_button.pack()

close_button = Button(main_container, text = "Close",
                       command = close_button_click)
close_button.pack()

# Creates a label frame, without this it is hard to tell where the 
# textboxes are
output_container = LabelFrame(main_container, text = "Output")
output_container.pack()
output_text = Text(output_container)
output_text.pack()

root.mainloop()
