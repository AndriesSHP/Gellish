"""Various utilities."""
import os
import subprocess
import sys


def open_file(path):
    """Platform-independent file opener.

    Opens the file with the program that is defined by its file extension.

    This covers Windows, MacOS and Unix-like systems (Linux, FreeBSD, Solaris...)
    https://stackoverflow.com/questions/17317219/is-there-an-platform-independent-equivalent-of-os-startfile
    """
    if sys.platform == "win32":
        os.startfile(path, 'open')
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        subprocess.call([opener, path])
