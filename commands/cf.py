import imp
import os
import subprocess
import sys

from ._cf import _LogStart
_lg=_LogStart().setup()

"""
common functions (cf) used by ../mkmov.py
"""


def check_dependencies():
    """function that checks we have the requireded dependencies, namely:
    * matplotlib
    * netCDF4
    * ffmpeg
    :returns: 
    """

    #See:
    #http://stackoverflow.com/questions/14050281/how-to-check-if-a-python-module-exists-without-importing-it
    try:
        imp.find_module('netCDF4')
    except ImportError:
        _lg.error("You don't have the netCDF4 library!")
        sys.exit("You don't have the netCDF4 library!")

    try:
        imp.find_module('matplotlib')
    except ImportError:
        _lg.error("You don't have the matplotlib library!")
        sys.exit("You don't have the matplotlib library!")

    try:
        imp.find_module('numpy')
    except ImportError:
        _lg.error("You don't have the numpy library!")
        sys.exit("You don't have the numpy library!")

    #This is the error message if ffmpeg is not installed...
    #The program 'ffmpeg' is currently not installed.  You can install it by typing:
        #sudo apt-get install libav-tools
    try:
        FNULL = open(os.devnull, 'w')
        subprocess.call(["ffmpeg", "--version"],stdout=FNULL, stderr=subprocess.STDOUT)
    except OSError as e:
        _lg.error("You don't have ffmpeg installed!")
        sys.exit("You don't have ffmpeg installed!")

    _lg.info("Good news: you seem to have all the right software installed!")


def mkdir(p):
    """make directory of path that is passed"""
    try:
       os.makedirs(p)
       _lg.info("output folder: "+p+ " does not exist, we will make one.")
    except OSError as exc: # Python >2.5
       import errno
       if exc.errno == errno.EEXIST and os.path.isdir(p):
          pass
       else: raise

def workingfol_func(arguments):
    """@todo: Docstring for workingfol_func
    :returns: @todo
    """
    # print arguments
    if not arguments['-o']:
        workingfol=tempfile.mkdtemp()+'/'
    else:
        workingfol=os.path.dirname(arguments['-o'])+'/mkmovTEMPFOL4_'+\
                os.path.basename(arguments['-o'])[:-4]+'/'
        if os.path.exists(workingfol):
            _lg.error("Working folder: " + workingfol+". already exists, has mkmov failed previously? Please remove and restart.")
            sys.exit("Working folder: " + workingfol+". already exists, has mkmov failed previously? Please remove and restart.")
        mkdir(workingfol)

    return workingfol
