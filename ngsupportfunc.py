#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Copyright (c) 2019 AndrewBCN Andre Derrick Balsa (andrebalsa@gmail.com)
#
# This file is licensed under the terms of the GNU General Public
# License version 3. This program is licensed "as is" without any
# warranty of any kind, whether express or implied.
#
# ngsupportfunc.py - support functions for build.py
#
# This file is a part of the Armbian-NG project
# https://github.com/AndrewBCN/Armbian-NG

# check Armbian-NG as well as standard Armbian documentation for more info

import os
import sys
import subprocess
import time
import argparse

def checkarch():
    
    arch = os.uname()
    
    if not arch.machine == "aarch64":
        print('Build host architecture is', arch.machine) 
        print('Armbian-NG must be built on an ARM 64-bit host (Aarch64)')
        sys.exit(1)

def installmodules():
    
    print("Downloading and installing various Python packages, please wait...")
    
    # ordered list of packages to install
    packages_to_install = [
        "wheel",        # needed by other things
        "setuptools",   # ditto
        "distro",       # reports detailed host Linux distribution information
        "pyfiglet",     # prints nice banners
        "clint",         # command line interface tools
        "npyscreen"     # console user interface library
        ]
    
    for package in packages_to_install:
        try:
            __import__(package)
            print(package,'was already installed')
        except ModuleNotFoundError:
            print('Installing', package)
            subprocess.run(['pip3', 'install', package])
        
    print("Done installing Python packages!")

def checklinuxdistro():
    # Checks that the build host Linux distribution/release is in the list below
    import distro
    
    validbuildhostdists = {
        'ubuntu': '18.04 18.10 19.04',
        'debian': '9.6 9.7 9.8',
        'neon': '18.04 18.10 19.04'
        }
    
    if distro.id() in validbuildhostdists:
        hostdist=distro.id()
        hostdistversion=distro.version()
        if hostdistversion in validbuildhostdists[hostdist]:
            print('Your host distribution is',hostdist.capitalize(),hostdistversion,'running on Aarch64 hardware. Good!')
        else:
            print('Your host distribution release',hostdist.capitalize(),hostdistversion,'is not supported for building Armbian-NG.')
            sys.exit(1)
    else:
        print('Your host distribution',hostdist.capitalize(),hostdistversion,'is not supported for building Armbian-NG.')
        sys.exit(1)

def printbanner():
    # Prints Armbian-NG banner using pyfiglet
    from pyfiglet import Figlet
    f = Figlet(font='slant')
    print(f.renderText('Armbian-NG'))
    
def armbianngmsg(s):
    # Prints special Armbian-NG message in red
    from clint.textui import puts, colored, indent
    with indent(4, quote='>>>'):
        puts(colored.red(s))
        
def parsecommandline(currentngversion):
    # Parses arguments on build.py command line, if any
    # Takes appropriate action in some cases
    # Armbian-NG version is passed as parameter from build.py
    parser = argparse.ArgumentParser(prog='build.py',description='A Python version of the Armbian build scripts',epilog="More information can be found in the Armbian-NG documentation, available in the /docs directory.")
    parser.add_argument('--version','-v',action='version',version=currentngversion)
    parser.add_argument('--armbianbranch','-a',action='store',dest="armbianbranch",default='master',choices=['master','next','tvboxes'],help="Specify the Armbian branch to clone")
    parser.add_argument('--configfile','-c',default="./config-default.conf",help="Specify the Armbian-style build configuration file")
    parser.add_argument('--distcc','-d',action="store_true",default=False,help="Use distcc to compile the Linux kernel on multiple machines")
    return parser.parse_args()

def reportbuildtime(b):
    # Calculates and prints the total build.py execution time
    from clint.textui import puts, colored, indent
    if b == 0:
        with indent(4, quote='>>>'):
            puts(colored.cyan('Build time: less than a minute'))
    else:
        if b < 2:
            with indent(4, quote='>>>'):
                puts(colored.green('Build time: less than a couple of minutes'))                     
        else:
            with indent(4, quote='>>>'):
                puts(colored.yellow('Build time: approximately ' + str(b) + ' minutes'))

#########################################################
# More complex build-related functions from this point on
 
def clonearmbianbranch(branchtoclone):
    # Create directory if not exists, change into it and git clone selected armbian-build branch
    # if directory exists assume it contains up-to-date armbian build clone
    dirName="armbian-" + branchtoclone
    
    if not os.path.exists(dirName):
        os.mkdir(dirName)
        print("Directory",dirName,"created ")
    else:    
        print("Directory",dirName,"already exists")
        return
    
    cwdName = os.getcwd()
    newtempName = cwdName + "/" + dirName
    
    print("Current Working Directory " , cwdName)
    
    try:
        # Change the current working Directory    
        os.chdir(newtempName)
        print("Directory changed")
    except OSError:
        print("Can't change the Current Working Directory")        
 
    print("Current Working Directory " , os.getcwd())
    
    # Git clone
    clonecommand = "git clone --depth 1 --branch " + branchtoclone + " https://github.com/armbian/build.git"
    print(clonecommand)
    # subprocess.run(clonecommand)
    subprocess.run(['git', 'clone', '--depth', '1', '--branch', branchtoclone, 'https://github.com/armbian/build.git'])
    
    # Go back
    os.chdir(cwdName)
    print("Back to Current Working Directory " , os.getcwd())
    
def gettargets(armbianbranch):
    # Create list of [board targets,types] for Armbian-NG from the files in armbian-<armbianbranch>/build/config/boards
    def get_boardname_and_type(filename):
        # split
        index = filename.find('.')
        return filename[:index], filename[index + 1:]
    # create empty list
    boardlist=[]
    # get list of files
    mylist=os.listdir("armbian-"+armbianbranch+"/build/config/boards")
    # from list of files create our list of [board targets,types]
    for file in mylist:
        boardlist.append(get_boardname_and_type(file))
    #return list of [board targets,types]
    return(boardlist)

#########################################################
# Console user input interface using npyscreen

# This is based on screenshots from armbian and tries to mimic armbian's dialogues as much as possible.
# Still missing is a way to select which forms are displayed and which are skipped, according to
# build options previously parsed from the configuration file.

# These can be passed in an array to the dialog() function.
# Also the dialog() function must return the newly set option values

# To do most urgently:
# - point the directory listing to the correct armbian directory
# - return the user provided values to dialog()

def dialog(progversion):
    import npyscreen
    global ngver
    ngver = "Armbian-NG Version " + progversion
    npyscreen.wrapper(ngTUI().run()) # this does all the work
    return(1) # should return a list of options set by the user

class ngTUI(npyscreen.NPSAppManaged):
    def onStart(self):
        # Set the theme. DefaultTheme is used by default
        # npyscreen.setTheme(npyscreen.Themes.ElegantTheme)
        # Sequential list of forms
        self.addForm("MAIN", myTUI, name= (ngver + " - Build Configuration User Interface - General instructions"))
        self.addForm("First", myTUI1, name= (ngver + " - Build selection"))
        self.addForm("Second", myTUI2, name= (ngver + " - Kernel configuration editing"))
        self.addForm("Third", myTUI3, name= (ngver + " - Target board configuration file selection"))
        self.addForm("Fourth", myTUI4, name= (ngver + " - Kernel branch selection"))
        self.addForm("Fifth", myTUI5, name= (ngver + " - Linux distribution selection"))
        self.addForm("Sixth", myTUI6, name= (ngver + " - Image type selection"))
        self.addForm("Summary", SummaryTUI, name= (ngver + " - Summary of user selected build options"))

class myTUI(npyscreen.ActionFormMinimal):
    def activate(self):
        self.parentApp.setNextForm("First")
        self.edit()

    def create(self):
        # non-selectable text
        self.choiceDescription0 = self.add(npyscreen.FixedText, editable=False,
                              value="* The following screens allow the user to configure the Armbian-NG build process.")
        self.choiceDescription1 = self.add(npyscreen.FixedText, editable=False,
                              value="* Option selection is done by moving to an option with <Tab> or the arrow keys,")
        self.choiceDescription1a = self.add(npyscreen.FixedText, editable=False,
                              value="  then selecting that option with <Enter>.")
        self.choiceDescription2 = self.add(npyscreen.FixedText, editable=False,
                              value="* The default option is indicated on each screen.")
        self.choiceDescription3 = self.add(npyscreen.FixedText, editable=False,
                              value="* To move from one screen to the next, select <OK>.")
    def on_ok(self):
        self.parentApp.switchForm("First")

class myTUI1(npyscreen.ActionFormMinimal):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("Second")

    def create(self):
        # non-selectable text
        self.choiceDescription1 = self.add(npyscreen.FixedText, editable=False,
                              value="Select what to build and press <Enter>")
        self.choiceDescription2 = self.add(npyscreen.FixedText, editable=False,
                              value="Default is to build full OS image")
        # leave an empty line
        self.nextrely += 1
        # get user input
        self.kernelOnly = self.add(npyscreen.MultiLine, relx=20,
                              values=["U-boot and kernel packages only", "Full OS image for flashing"])

    def on_ok(self):
        # send input value to Summary form and move to next form
        toSummary = self.parentApp.getForm("Summary")
        toSummary.ko.value = self.kernelOnly.values[self.kernelOnly.value] # value is an index into values list
        self.parentApp.switchForm("Second")

class myTUI2(npyscreen.ActionFormMinimal):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("Third")

    def create(self):
        # non-selectable text
        self.choiceDescription1 = self.add(npyscreen.FixedText, editable=False,
                              value="Select kernel configuration editing option and press <Enter>")
        self.choiceDescription2 = self.add(npyscreen.FixedText, editable=False,
                              value="Default is to not change the kernel configuration")
        # leave an empty line
        self.nextrely += 1
        # get user input
        self.kernelConfigEdit = self.add(npyscreen.MultiLine, relx=20,
                              values=["Do not change the default kernel configuration", "Show a kernel configuration menu before compiling"])

    def on_ok(self):
        # send input value to Summary form and move to next form
        toSummary = self.parentApp.getForm("Summary")
        toSummary.kc.value = self.kernelConfigEdit.values[self.kernelConfigEdit.value] # value is an index into values list
        self.parentApp.switchForm("Third")

class myTUI3(npyscreen.ActionFormMinimal):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("Fourth")

    def create(self):
        # non-selectable text
        self.choiceDescription1 = self.add(npyscreen.FixedText, editable=False,
                              value="Select target board configuration file and press <Enter>")
        self.choiceDescription2 = self.add(npyscreen.FixedText, editable=False,
                              value=".conf = officially supported target board")
        self.choiceDescription3 = self.add(npyscreen.FixedText, editable=False,
                              value=".csc  = community supported target board")
        self.choiceDescription2 = self.add(npyscreen.FixedText, editable=False,
                              value=".wip  = work in progress")
        self.choiceDescription2 = self.add(npyscreen.FixedText, editable=False,
                              value=".eos  = support ended")
        self.choiceDescription2 = self.add(npyscreen.FixedText, editable=False,
                              value=".tvb  = TV Box")
        # leave an empty line
        self.nextrely += 1
        # get user input
        self.favFile = self.add(npyscreen.TitleFilenameCombo,
                                name="Please choose a build target file, use arrow keys to scroll", label=True)

    def on_ok(self):
        # send input value to Summary form and move to next form
        toSummary = self.parentApp.getForm("Summary")
        toSummary.tf.value = self.favFile.value
        self.parentApp.switchForm("Fourth")

class myTUI4(npyscreen.ActionFormMinimal):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("Fifth")

    def create(self):
        # non-selectable text
        self.choiceDescription1 = self.add(npyscreen.FixedText, editable=False,
                              value="Select target kernel branch and press <Enter>")
        self.choiceDescription2 = self.add(npyscreen.FixedText, editable=False,
                              value="Default is vendor/legacy kernel")
        self.choiceDescription3 = self.add(npyscreen.FixedText, editable=False,
                              value="Exact kernel versions depend on selected target board")
        # leave an empty line
        self.nextrely += 1
        # get user input
        self.kernelVer = self.add(npyscreen.MultiLine, relx=20,
                              values=["Vendor provided / Legacy (3.xx - 4.xx)", "Mainline (4.xx - 5.xx)"])

    def on_ok(self):
        # send input value to Summary form and move to next form
        toSummary = self.parentApp.getForm("Summary")
        toSummary.kv.value = self.kernelVer.values[self.kernelVer.value] # value is an index into values list
        self.parentApp.switchForm("Fifth")

class myTUI5(npyscreen.ActionFormMinimal):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("Sixth")

    def create(self):
        # non-selectable text
        self.choiceDescription1 = self.add(npyscreen.FixedText, editable=False,
                              value="Select target Linux distribution/release and press <Enter>")
        self.choiceDescription2 = self.add(npyscreen.FixedText, editable=False,
                              value="Default is Ubuntu 18.04")
        # leave an empty line
        self.nextrely += 1
        # get user input
        self.linuxDistVer = self.add(npyscreen.MultiLine, relx=20,
                              values=["Debian Stretch 9.x", 
                                      "Ubuntu Bionic 18.04",
                                      "Arch Linux",
                                      "Alpine Linux"])

    def on_ok(self):
        # send input value to Summary form and move to next form
        toSummary = self.parentApp.getForm("Summary")
        toSummary.ld.value = self.linuxDistVer.values[self.linuxDistVer.value] # value is an index into values list
        self.parentApp.switchForm("Sixth")

class myTUI6(npyscreen.ActionFormMinimal):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm("Summary")

    def create(self):
        # non-selectable text
        self.choiceDescription1 = self.add(npyscreen.FixedText, editable=False,
                              value="Select Linux image type (desktop/server) and press <Enter>")
        self.choiceDescription2 = self.add(npyscreen.FixedText, editable=False,
                              value="Default is minimal server image")
        # leave an empty line
        self.nextrely += 1
        # get user input
        self.distImageType = self.add(npyscreen.MultiLine, relx=20,
                              values=["Minimal Linux server image, console interface", 
                                      "Full Linux desktop image, graphical interface"])

    def on_ok(self):
        # send input value to Summary form and move to next form
        toSummary = self.parentApp.getForm("Summary")
        toSummary.it.value = self.distImageType.values[self.distImageType.value] # value is an index into values list
        self.parentApp.switchForm("Summary")

class SummaryTUI(npyscreen.ActionFormMinimal):
    def activate(self):
        self.edit()
        self.parentApp.setNextForm(None)

    def create(self):
        # display selected options
        self.ko = self.add(npyscreen.TitleFixedText, editable=False, name="Build option selection:        ")
        self.kc = self.add(npyscreen.TitleFixedText, editable=False, name="Kernel config option selection:")
        self.tf = self.add(npyscreen.TitleFixedText, editable=False, name="Target board file selection:   ")
        self.kv = self.add(npyscreen.TitleFixedText, editable=False, name="Kernel version selection:      ")
        self.ld = self.add(npyscreen.TitleFixedText, editable=False, name="Linux distribution selection:  ")
        self.it = self.add(npyscreen.TitleFixedText, editable=False, name="Image type selection:          ")
        
    def on_ok(self):
        self.parentApp.setNextForm(None)






    

