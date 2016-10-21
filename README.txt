DISCLAIMER: It is your responsibility to use this script without
causing damage to your filesystem. I have tried to provide safety
checks, but they are minimal.

Lab Cleaner and Compressor for CMPE 121 

The lab cleaner and compressor consists of the script
cmpe121_lab_sub_script.py. It was tested using python 2.7 and
uses the following packages:
  Tkinter
  tkFileDialog
  tkMessageBox
  os
  shutil

These packages are normally already installed with python. Most of 
the testing for this script was performed in OS X, but was also
tested under Windows.

If python is not installed on your computer I recommend installing
the anaconda python manager (https://www.continuum.io/downloads).
It makes it easy to manage python packages and is available for
Mac, Windows, and Linux.

To run the script:
  python cmpe121_lab_sub_script.py

This will open a gui. Type the name you wish to use as your
file submission, i.e. sam_mansfield, select your lab directory,
and lab report. Then click on the Clean & Zip button, which 
will clean out your lab directory for unnecessary files and
zip it.

For more details on how the script works open the python script
in a text editor, it is heavily commented.
