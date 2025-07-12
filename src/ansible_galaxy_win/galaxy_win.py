import sys, types

import locale
locale.getlocale = lambda: ('en_US', 'UTF-8')

dummy_termios = types.ModuleType("termios")

# Constants (values are placeholders)
dummy_termios.IFLAG = 0
dummy_termios.OFLAG = 1
dummy_termios.CFLAG = 2
dummy_termios.LFLAG = 3
dummy_termios.ISPEED = 4
dummy_termios.OSPEED = 5
dummy_termios.CC = 6

dummy_termios.VINTR = 0
dummy_termios.VQUIT = 1
dummy_termios.VERASE = 2
dummy_termios.VKILL = 3
dummy_termios.VEOF = 4
dummy_termios.VTIME = 5
dummy_termios.VMIN = 6
dummy_termios.VSWTC = 7
dummy_termios.VSTART = 8
dummy_termios.VSTOP = 9
dummy_termios.VSUSP = 10
dummy_termios.VEOL = 11
dummy_termios.VREPRINT = 12
dummy_termios.VDISCARD = 13
dummy_termios.VWERASE = 14
dummy_termios.VLNEXT = 15
dummy_termios.VEOL2 = 16

dummy_termios.B0 = 0
dummy_termios.B50 = 50
dummy_termios.B75 = 75
dummy_termios.B110 = 110
dummy_termios.B134 = 134
dummy_termios.B150 = 150
dummy_termios.B200 = 200
dummy_termios.B300 = 300
dummy_termios.B600 = 600
dummy_termios.B1200 = 1200
dummy_termios.B1800 = 1800
dummy_termios.B2400 = 2400
dummy_termios.B4800 = 4800
dummy_termios.B9600 = 9600
dummy_termios.B19200 = 19200
dummy_termios.B38400 = 38400

dummy_termios.TCSANOW = 0
dummy_termios.TCSADRAIN = 1
dummy_termios.TCSAFLUSH = 2

# Functions (no-op or dummy returns)
def tcgetattr(fd):
    return [
        0, 0, 0, 0, 0, 0,  # iflag, oflag, cflag, lflag, ispeed, ospeed
        [0] * 32           # cc (control characters array)
    ]

def tcsetattr(fd, when, attributes):
    pass

def tcflush(fd, queue):
    pass

def tcdrain(fd):
    pass

def tcflow(fd, action):
    pass

def tcsendbreak(fd, duration):
    pass

# Assign functions
dummy_termios.tcgetattr = tcgetattr
dummy_termios.tcsetattr = tcsetattr
dummy_termios.tcflush = tcflush
dummy_termios.tcdrain = tcdrain
dummy_termios.tcflow = tcflow
dummy_termios.tcsendbreak = tcsendbreak

sys.modules["termios"] =dummy_termios

pointless_imports = ["fcntl", "fork"]

for dummy in ["fcntl", "fork", "grp", "pwd"]:
    sys.modules[dummy] = types.ModuleType(dummy)

import multiprocessing
fake_context = types.SimpleNamespace()
fake_context.parent_process = lambda: "FAKE"
multiprocessing.get_context = lambda method=None: fake_context

import ctypes
import ctypes.util

# Save original
original_load_library = ctypes.cdll.LoadLibrary

# Define a fake libc object
class FakeLibC:
    def __getattr__(self, name):
        print(f"[FAKE_LIBC] Called function: {name}")
        return lambda *args, **kwargs: 0  # dummy function that returns 0

# Patch it
ctypes.cdll.LoadLibrary = lambda libname: FakeLibC() if libname == ctypes.util.find_library('c') else original_load_library(libname)

import os
os.path.sep = '/'

from ansible.cli.galaxy import main as galaxy_main

args = [
    '',
    'collection',
    'download',
    'community.general'
]

g = galaxy_main(args=args)
g.execute_download()