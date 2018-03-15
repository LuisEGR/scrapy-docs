import re
import datetime
import os
import urllib
import hashlib
import shutil
from clint.textui import colored, puts
from pathlib import Path
from colorama import Fore, Style
from bson.binary import Binary

class Log:
    @staticmethod
    def error(text):
        print(Fore.RED + Style.BRIGHT + text + Fore.RESET + Style.RESET_ALL)

    @staticmethod
    def warning(text):
        print(Fore.YELLOW + Style.DIM + text + Fore.RESET + Style.RESET_ALL)

    @staticmethod
    def ok(text):
        # puts(colored.green(text))
        print(Fore.GREEN + Style.BRIGHT +
              text + Fore.RESET + Style.RESET_ALL)

    @staticmethod
    def log(text):
        print(Style.DIM + text + Style.RESET_ALL)

    @staticmethod
    def msg(text):
        print(Fore.CYAN + Style.NORMAL + text + Fore.RESET)
