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


def extract_fecha(cadena):
    if(cadena == None):
        return cadena
    return re.search("[0-9]{2}\/[0-9]{2}\/[0-9]{4}", cadena).group(0)


def getFechaFromStrUnix(cadena, formato):
    unix = re.search("[0-9]+", cadena).group(0)
    fecha = datetime.datetime.fromtimestamp(int(unix) / 1000).strftime(formato)
    return fecha


def obtener_lista_fechas_hasta_hoy(from_date, formato):
    """ Retorna una lista de cadenas con 
    las fechas desde 'from_date' hasta hoy, incrementando por 1 día
    y con el formato 'formato' """
    d_from = datetime.datetime.strptime(from_date, formato)
    d_end = datetime.datetime.today()
    step = datetime.timedelta(days=1)
    result = []
    while d_from < d_end:
        result.append(d_from.strftime(formato))
        d_from += step
    return result


def save_pdf(response, filename, directorio):
    filename = urllib.parse.unquote(filename)
    Log.msg("Descargando: " + filename)
    dir_files = directorio
    if not os.path.exists(dir_files):
        os.makedirs(dir_files)
    if not os.path.exists(dir_files + 'temp/'):
        os.makedirs(dir_files + 'temp/')
    path_tmp = dir_files + 'temp/' + filename
    path_real = dir_files + filename
    with open(path_tmp, 'wb') as f:
        f.write(response.body)

    newHash = md5(path_tmp)
    if not file_old_exists(newHash, path_real):
        os.rename(path_tmp, path_real)
        Log.ok("Nuevo archivo guardado!: " + path_real)
    else:
        Log.msg("Ignorando nuevo archivo" + path_tmp)


def file_old_exists(new_hash, path):
    my_file = Path(path)
    if my_file.is_file():
        old_hash = md5(path)
        Log.log("OldHash: " + old_hash)
        Log.log("NewHash: " + new_hash)
        return old_hash == new_hash
    else:
        return False


def delete_temporal_files(path):
    shutil.rmtree(path)
    Log.ok("Archivos temporales borrados! \n")


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
