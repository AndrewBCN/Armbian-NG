## Requirements
To build a bootable Armbian image using Armbian-NG, you'll need:

- An Aarch64 (64-bit ARM) SBC, TV box or laptop **running Ubuntu 18.04** (e.g. a $25 Amlogic S905X TV box previously installed with Armbian Ubuntu bionic).
- 20GB of free preferably solid state storage (e.g. a $5 32GB A1 micro SD card).
- Obviously, an Internet connection.

## Getting started

- Login to your Aarch64 machine and in a terminal, type:

>	df

- Check that you have at least 15GB, preferably 20GB of free disk space. Now, install git, python3, and a few more packages needed to build the Linux kernel:

>	sudo apt update

>	sudo apt upgrade

>	sudo apt install git python3 python3-pip python3-setuptools python3-wheel

>	sudo apt install build-essential autoconf libtool cmake pkg-config git python-dev swig3.0 libpcre3-dev nodejs-dev gawk wget diffstat bison flex

>	sudo apt install device-tree-compiler libncurses5-dev

- Create a development directory and change to it:

>	mkdir development; cd development

- Clone the Armbian-NG repository:

>	git clone \-\-depth 1 https://github.com/AndrewBCN/Armbian-NG.git

- Change to the Armbian-NG directory:

>	cd Armbian-NG

- Launch the Armbian-NG image build process:

>	python3 build.py

