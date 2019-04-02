#Armbian-NG configuration files

Just like armbian, Armbian-NG supports image building configuration files. The key difference is that Armbian-NG can parse both old-style armbian configuration files and new-style Armbian-NG configuration files.

###Old style armbian configuration files

Since armbian-build is written in bash, its configuration files basically consist of a list of bash environment variables setting commands. Example:

	FORCE_BOOTSCRIPT_UPDATE="no"

Comments are preceded by the \"\#\" character.

Old-style armbian configuration files can be parsed using the shlex library: https://docs.python.org/3/library/shlex.html#module-shlex

###New style Armbian-NG configuration files

Armbian-NG uses the Python configparser library to parse Windows[tm] INI-style files. The file format is described here: https://docs.python.org/3/library/configparser.html

The first line of a new-style Armbian-NG configuration file must include the string "Armbian-NG". For example, this comment:

	# This is an Armbian-NG configuration file

in the first line of a file indicates it is an Armbian-NG configuration file.
Note that here again comments are preceded by the \"\#\" character.