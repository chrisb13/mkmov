#   Author: Christopher Bull. 
#   Affiliation: Climate Change Research Centre and ARC Centre of Excellence for Climate System Science.
#                Level 4, Mathews Building
#                University of New South Wales
#                Sydney, NSW, Australia, 2052
#   Contact: z3457920@student.unsw.edu.au
#   www:     christopherbull.com.au
#   Date created: Fri, 06 Nov 2015 11:24:32
#   Machine created on: ccrc165
#


#see: https://github.com/docopt/docopt
#round brackets mean required square are optional

#download docopt from...
#https://raw.githubusercontent.com/docopt/docopt/master/docopt.py


"""
This ia python script for making movies

Usage:
    main.py -h
    main.py FILE_NAME VARIABLE_NAME 

Arguments:
    FILE_NAME       path to NetCDF file to make movie
    VARIABLE_NAME   variable name

Options:
    -h,--help          : show this help message
"""
from docopt import docopt
arguments = docopt(__doc__)
import sys,os
from cb2logger import *

def check_dependencies():
    """function that checks we have the requireded dependencies, namely:
    * matplotlib
    * netCDF4
    * ffmpeg
    :returns: @todo
    """

    #This is the error message if ffmpeg is not installed...
    #The program 'ffmpeg' is currently not installed.  You can install it by typing:
        #sudo apt-get install libav-tools

    #See:
    #http://stackoverflow.com/questions/14050281/how-to-check-if-a-python-module-exists-without-importing-it





if __name__ == "__main__": 
    LogStart('',fout=False)
    lg.info("demo log message")

    file='/path/to/netcdf4/file.nc'
    if not os.path.exists(file):
        lg.error("Input file: " + str(file) + " does not exist.")
        sys.exit("Input file: " + str(file) + " does not exist.")

    check_dependencies()

    from netCDF4 import Dataset
    import matplotlib.pyplot as plt


    ifile=Dataset(file, 'r')
    #varone=ifile.variables['']
    #put useful code here!

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
