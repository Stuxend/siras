#!/usr/bin/python

from termcolor import cprint
from pyfiglet import figlet_format
import sys

from colorama import init
init(strip=not sys.stdout.isatty())  # strip colors if stdout is redirected


def home():
    cprint(figlet_format(' siras '))
