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
import argparse

import ngsupportfunc    # various functions used by main() below

ngversion = "0.02"

def main():

    print("Welcome to Armbian-NG!")
    
    # Start stopwatch
    start = time.time()
    
    # Parse command line
    ngsupportfunc.parsecommandline(ngversion)
    
    # Check the underlying architecture, must be Aarch64, if not, print message and exit
    ngsupportfunc.checkarch()
    
    # Install needed Python 3 packages
    ngsupportfunc.installmodules()
    
    # Check build host Linux distribution
    ngsupportfunc.checklinuxdistro()

    # Display Armbian-NG banner
    ngsupportfunc.printbanner()
    
    # Tell user we are getting started
    ngsupportfunc.armbianngmsg('Armbian-NG started!')
    
    # Make modules in lib visible
    sys.path.append('./lib/')
    
#    import armbian-ng-functions
#    check-requirements()
#    build-kernel()
#    build-u-boot()
#    build-rootfs()
#    build-boot()
#    build-image()
#    cleanup()
    
    # Tell user we are done and stop stopwatch
    ngsupportfunc.armbianngmsg('Armbian-NG done!')
    end = time.time()
    
    # Report build time in minutes
    btime = round((end-start)/60)
    ngsupportfunc.reportbuildtime(btime)
    
                     
if __name__ == '__main__':
    main()
