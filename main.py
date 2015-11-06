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

Example: python main.py /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/1989/cordex24-ERAI01_1d_19890101_19890105_grid_T_2D.nc tos

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
import imp

def check_dependencies():
    """function that checks we have the requireded dependencies, namely:
    * matplotlib
    * netCDF4
    * ffmpeg
    :returns: 
    """

    #This is the error message if ffmpeg is not installed...
    #The program 'ffmpeg' is currently not installed.  You can install it by typing:
        #sudo apt-get install libav-tools

    #See:
    #http://stackoverflow.com/questions/14050281/how-to-check-if-a-python-module-exists-without-importing-it
    try:
        imp.find_module('netCDF4')
    except ImportError:
        lg.error("You don't have the netCDF4 library!")
        sys.exit("You don't have the netCDF4 library!")

    try:
        imp.find_module('matplotlib')
    except ImportError:
        lg.error("You don't have the matplotlib library!")
        sys.exit("You don't have the matplotlib library!")


def create_plot(name_of_array):
    """function to create plots.
    
    :name_of_array: @todo
    :returns: @todo
    """

    plt.close('all')
    fig=plt.figure()
    ax=fig.add_subplot(1, 1,1)
    #code to plot
    ax.set_title('msg')
    ax.set_xlabel('msg')
    ax.set_ylabel('msg')
    #fig.savefig('./.png',dpi=300)
    #fig.savefig('./.pdf',format='pdf')
    plt.show()


if __name__ == "__main__": 
    LogStart('',fout=False)
    #lg.info("demo log message")

    check_dependencies()

    from netCDF4 import Dataset
    import matplotlib.pyplot as plt

    #file='/path/to/netcdf4/file.nc'
    file=arguments['FILE_NAME']
    variable=arguments['VARIABLE_NAME']

    #error check for file
    if not os.path.exists(file):
        lg.error("Input file: " + str(os.path.basename(file))  + " does not exist.")
        sys.exit("Input file: " + str(os.path.basename(file))  + " does not exist.")

    ifile=Dataset(file, 'r')

    if variable not in ifile.variables.keys():
        lg.error("Variable: " + str(variable) + " does not exist in netcdf4 file.")
        sys.exit("Variable: " + str(variable) + " does not exist in netcdf4 file.")
    #import ipdb; ipdb.set_trace()

    varone=ifile.variables[variable]

    #create_plot(varone)

    #put useful code here!

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
