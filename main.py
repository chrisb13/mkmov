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
MkMov v0.1
This is a python script for making movies from a netCDF file.

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

#possible new format for arg passer...
# """
# MkMov v0.1
# Usage: sphinx-quickstart [options] [projectdir]

# Options:
  # --version             show program's version number and exit
  # -h, --help            show this help message and exit

  # Program options:
    # --sep                       if specified, separate source and build dirs
    # --wpath=DOT            if specified, path to place plots in before stiching, will not be removed

  # Matplotlib options:
    # -p PROJECT, --project=PROJECT
                        # project name
    # -a AUTHOR, --author=AUTHOR
                        # author names
    # -v VERSION          version of project
    # -r RELEASE, --release=RELEASE
                        # release of project
    # -l LANGUAGE, --language=LANGUAGE
                        # document language
    # --suffix=SUFFIX     source file suffix
    # --master=MASTER     master document name
    # --epub              use epub

  # Basemap options:
    # --ext-autodoc       enable autodoc extension
    # --ext-doctest       enable doctest extension
    # --ext-intersphinx   enable intersphinx extension
    # --ext-todo          enable todo extension
# """


from docopt import docopt
arguments = docopt(__doc__)
import sys,os
from cb2logger import *
import imp
import tempfile
import subprocess
import glob

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

    try:
        imp.find_module('numpy')
    except ImportError:
        lg.error("You don't have the numpy library!")
        sys.exit("You don't have the numpy library!")


def dispay_passed_args(workingfolder):
    """function to print out the passed arguments to the logger

    :workingfolder: @todo
    :returns: @todo
    """
    lg.info("-----------------------------------------------------------------")
    lg.info("MkMov has been run with the following options...")

    lg.info("File we are making a movie of: "+ os.path.basename(arguments['FILE_NAME']))

    lg.info("Variable we are making a movie of: "+ arguments['VARIABLE_NAME'])

    lg.info("Our working directory is: "+ workingfolder)

    lg.info("")
    lg.info("Optional settings:")
    #for optional parameters...
    # if 'FILE_PATH' in arguments.keys():
    # if 'VARIABLE_NAME' in arguments.keys():

    lg.info("-----------------------------------------------------------------")
    return


def create_plot(name_of_array,timedimen,workingfolder):
    """function to create plots.
    
    :name_of_array: @todo
    :timedimen: @todo
    :workingfolder: @todo
    :returns: @todo
    """

    plt.close('all')
    fig=plt.figure()

    #this is dodge...
    x,y=np.meshgrid(np.arange(np.shape(name_of_array)[2]),np.arange(np.shape(name_of_array)[1]))
    minvar=np.min(name_of_array)
    maxvar=np.max(name_of_array)
    for tstep in np.arange(np.shape(name_of_array)[timedimen]):
        lg.debug("Working timestep: " + str(tstep))

        ax=fig.add_subplot(111)

        ax.set_title(arguments['VARIABLE_NAME'])
        #ax.set_xlabel('msg')
        #ax.set_ylabel('msg')

        name_of_array= np.ma.masked_where(
            name_of_array==0.,
            name_of_array) 

        cs1=plt.contourf(x,y,name_of_array[tstep,:,:],levels=np.linspace(minvar,maxvar,30))

        #land mask...
        cs2=ax.contour(x,y,name_of_array[tstep,:,:].mask,levels=[-1,0],linewidths=1,colors='black')

        plt.colorbar(cs1)
        #plt.show()
    
        fig.savefig(workingfolder+'/moviepar'+str(tstep).zfill(5)+'.png',dpi=300)
        #fig.savefig('./.pdf',format='pdf')
        fig.clf()
        del ax
    print workingfolder

    #ollie's command didn't work on storm
    #ffmpeg -framerate 10 -y -i plot_%04d.png -s:v 1920x1080 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p movie.mp4

    os.chdir(workingfolder)
    subprocess.call('ffmpeg -r 15 -qscale 3 -y -an -i ' + 'moviepar%05d.png '+os.path.basename(arguments['FILE_NAME']) + '.mov',shell=True)

    #remove png
    if os.path.isfile(workingfolder+os.path.basename(arguments['FILE_NAME']) + '.mov'):
        ifiles=sorted(glob.glob(workingfolder + 'moviepar*.png' ))
        assert(ifiles!=[]),"glob didn't find anything!"
        for f in ifiles:
            os.remove(f)


if __name__ == "__main__": 
    LogStart('',fout=False)
    #lg.info("demo log message")
    workingfol=tempfile.mkdtemp()+'/'

    dispay_passed_args(workingfol)

    check_dependencies()

    from netCDF4 import Dataset
    import matplotlib.pyplot as plt
    import numpy as np

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

    #find unlimited dimension
    findunlim=[ifile.dimensions[dim].isunlimited() for dim in ifile.dimensions.keys()]
    dim_unlim_num=[i for i, x in enumerate(findunlim) if x]
    if len(dim_unlim_num)==0:
        lg.error("Input file: " + str(os.path.basename(file))  + " has no unlimited dimension, which dim is time?")
        sys.exit("Input file: " + str(os.path.basename(file))  + " has no unlimited dimension, which dim is time?")
    elif len(dim_unlim_num)>1:
        lg.error("Input file: " + str(os.path.basename(file))  + " has more than one unlimited dimension.")
        sys.exit("Input file: " + str(os.path.basename(file))  + " has more than one unlimited dimension.")
    else:
        timename=ifile.dimensions.keys()[dim_unlim_num[0]]
        var_timedim=[i for i, x in enumerate(ifile.variables[variable].dimensions) if x==timename][0]

    varone=ifile.variables[variable][:]

    create_plot(varone,var_timedim,workingfol)


    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
