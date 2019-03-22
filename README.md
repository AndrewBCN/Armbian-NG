# Armbian-NG
Armbian-NG is a project with a similar purpose to Armbian's: generating Debian or Ubuntu images that can be directly booted on ARM hardware.

The key differences between Armbian and Armbian-NG are:
- Armbian is written in bash. While bash works well for small scripts, the Armbian build scripts have essentially reached a size where using a more advanced programming language would prove advantageous. So Armbian-NG is written in Python, using Sultan to interface with the shell.
- Armbian runs on x86-64 hardware and requires cross-compilation toolchains. Armbian-NG runs natively on Aarch64 hardware and uses native compilation toolchains.
- Armbian can generate images for both 32-bit and 64-bit ARM hardware. Armbian-NG only supports the generation of images for 64-bit ARM hardware (Aarch64).
- Armbian-NG can optionally use distcc to accelerate kernel compilation.
