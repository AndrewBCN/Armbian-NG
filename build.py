#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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
import time

def checkarch():
    
    arch = os.uname()
    
    if not arch.machine == "aarch64":
        print('Build host architecture is ', arch.machine) 
        print('Armbian-NG must be built on an ARM 64-bit host (Aarch64)')
        sys.exit(1)

def installmodules():
    
    print("Downloading and installing various Python packages, please wait...")
    
    # ordered list of packages to install
    packages_to_install = [
        "wheel",        # needed by other things
        "setuptools",   # ditto
        "args",         # ditto
        "distro",       # reports detailed host Linux distribution information
        "pyfiglet",     # prints nice banners
        "clint"         # command line interface tools
        ]
    
    for package in packages_to_install:
        try:
            globals()[package] = __import__(package)  
            print(package,'was already installed')
        except ModuleNotFoundError:
            print('Installing', package)
            subprocess.run(['pip3', 'install', package])
            globals()[package] = __import__(package)
        
    print("Done installing Python packages!")

def checklinuxdistro():
    
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
    
    from pyfiglet import Figlet
    f = Figlet(font='slant')
    print(f.renderText('Armbian-NG'))

def main():

    print("Welcome to Armbian-NG!")
    
    # Start stopwatch
    start = time.time()
    
    # Check the underlying architecture, must be Aarch64, if not, print message and exit
    checkarch()
    
    # Install needed Python 3 packages and make them global
    installmodules()
    
    # Check build host Linux distribution
    checklinuxdistro()

    # Display Armbian-NG banner
    printbanner()
    
    # Tell user we are getting started
    from clint.textui import puts, colored, indent
    
    with indent(4, quote='>>>'):
        puts(colored.red('Armbian-NG started!'))
    
    # Make modules in lib visible
    sys.path.append('./lib/')
    
#    import armbian-ng-functions
#    check-requirements()
#    build-kernel()
#    build-u-boot()
#    build-rootfs()
#    build-boot()
#    build-image()
    
    # Tell user we are done and stop stopwatch
    with indent(4, quote='>>>'):
        puts(colored.red('Armbian-NG done!'))
    end = time.time()
    
    # Report build time in minutes
    buildtime = round((end-start)/60)
    if buildtime == 0:
        with indent(4, quote='>>>'):
            puts(colored.cyan('Build time: less than a minute'))
    else:
        if buildtime < 2:
            with indent(4, quote='>>>'):
                puts(colored.green('Build time: less than a couple of minutes'))                     
        else:
            with indent(4, quote='>>>'):
                puts(colored.purple('Build time: approximately ' + buildtime + ' minutes'))
                     
if __name__ == '__main__':
    main()
