#!/usr/bin/env python3
#
# Copyright (c) 2019 AndrewBCN Andre Derrick Balsa (andrebalsa@gmail.com)
#
# This file is licensed under the terms of the GNU General Public
# License version 3. This program is licensed "as is" without any
# warranty of any kind, whether express or implied.
#
# build.py - Build an Armbian image bootable on Aarch64 hardware
#
# This file is a part of the Armbian-NG project
# https://github.com/AndrewBCN/Armbian-NG

# check Armbian-NG as well as standard Armbian documentation for more info

import os
import sys
import subprocess

def installmodules():

    print("Downloading and installing various Python packages, please wait...")
    
    # packages to install
    packages_to_install = [
        "wheel",        # needed by other things
        "setuptools",   # ditto
        "args",         # ditto
        "pyfiglet",     # print nice banners
        "clint"         # command line interface tools
        ]
    for package in packages_to_install:
        subprocess.run(['pip3', 'install', package])
    
    print("Done installing Python packages!")

def printbanner():
    
    from pyfiglet import Figlet
    f = Figlet(font='slant')
    print(f.renderText('Armbian-NG'))

def main():

    print("Welcome to Armbian-NG!")
    
    # Check the underlying architecture, must be Aarch64, if not, print message and exit
    arch = os.uname()
    
    if not arch.machine == "aarch64":
        print('Armbian-NG must be built on an ARM 64-bit machine (Aarch64)')
        sys.exit(1)
        
    # Install needed Python 3 packages
    installmodules()
    
    # Display Armbian-NG banner
    printbanner()

    # Make modules in lib visible
    sys.path.append('./lib/')
    
#    import armbian-ng-functions
#    check-requirements()
#    build-kernel()
#    build-u-boot()
#    build-rootfs()
#    build-boot()
#    build-image()
    print("Armbian-NG done!")

if __name__ == '__main__':
    main()
