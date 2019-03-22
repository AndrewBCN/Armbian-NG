# Armbian-NG
Armbian-NG is a project with a similar purpose to [Armbian](https://www.armbian.com/)'s: generating Debian or Ubuntu images that can be directly booted on ARM hardware.

**The key differences** between [Armbian](https://www.armbian.com/) and Armbian-NG are:
- [Armbian](https://www.armbian.com/) is written in bash. While bash works well for small scripts, the Armbian build scripts have essentially reached a size where using a more advanced programming language would prove advantageous. So Armbian-NG is written in **Python**, using [Sultan](https://sultan.readthedocs.io/en/latest/) to run shell commands and the [Cement](https://builtoncement.com/) command-line framework to interface with the user.
- [Armbian](https://www.armbian.com/) runs on x86-64 hardware and requires cross-compilation toolchains. Armbian-NG runs natively on Aarch64 hardware and uses native compilation toolchains.
- [Armbian](https://www.armbian.com/) can generate images for both 32-bit and 64-bit ARM hardware. Armbian-NG only supports the generation of images for 64-bit ARM hardware (Aarch64).
- Armbian-NG can optionally use distcc to accelerate kernel compilation.

### Documentation

Again similar to [Armbian](https://www.armbian.com/) , Armbian-NG documentation is written in markdown and stored in the docs/ subfolder, with images in docs/images. It is recommended to use the [Remarkable](https://remarkableapp.github.io/linux/download.html) markdown editor to generate Armbian-NG documentation.