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
        "clint"         # command line interface tools
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
                puts(colored.purple('Build time: approximately ' + b + ' minutes'))

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

