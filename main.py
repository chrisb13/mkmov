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
MkMov v0.2
This is a python script for making movies from a netCDF file. Interface is by command line.

Examples: 
python main.py --help
python /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/1989/cordex24-ERAI01_1d_19890101_19890105_grid_T_2D.nc tos main.py 
python /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc tos main.py 

Usage:
    main.py -h
    main.py VARIABLE_NAME FILE_NAME...

Arguments:
    VARIABLE_NAME   variable name
    FILE_NAME       path to NetCDF file to make movie, can also be a list of files (dimensions must be the same)

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

    for f in arguments['FILE_NAME']:
        lg.info("File we are making a movie of file(s): "+ os.path.basename(f))

    lg.info("Variable we are making a movie of: "+ arguments['VARIABLE_NAME'])

    lg.info("Our working directory is: "+ workingfolder)

    lg.info("")
    lg.info("Optional settings:")
    #for optional parameters...
    # if 'FILE_PATH' in arguments.keys():
    # if 'VARIABLE_NAME' in arguments.keys():

    lg.info("-----------------------------------------------------------------")
    return



class MovMaker(object):
    """
    Class to create movie based on file list and variable name.

    Parameters
    ----------
    :filelist:
    variable_name: 
    :workingfolder: @todo

    Returns
    -------
    
    Notes
    -------
    

    Example
    --------
    >>> 
    >>> 
    """

    def __init__(self, filelist,variable_name,workingfolder):
        #super(MovMaker, self).__init__()
        self.filelist,self.variable_name = filelist,variable_name
        self.workingfolder=workingfolder

    def lights(self):
        var_timedims=[]

        #error checks files, are all similar
        for f in self.filelist:
            if not os.path.exists(f):
                lg.error("Input file: " + str(os.path.basename(f))  + " does not exist.")
                sys.exit("Input file: " + str(os.path.basename(f))  + " does not exist.")

            ifile=Dataset(f, 'r')

            if self.variable_name not in ifile.variables.keys():
                lg.error("Variable: " + str(self.variable_name) + " does not exist in netcdf4 file.")
                sys.exit("Variable: " + str(self.variable_name) + " does not exist in netcdf4 file.")

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
                var_timedim=[i for i, x in enumerate(ifile.variables[self.variable_name].dimensions) if x==timename][0]
                var_timedims.append(var_timedim)
            ifile.close()

        #check all unlimited dimensions are in the same place across all files..
        if var_timedims[1:]==var_timedims[:-1]:
            self.timedim=var_timedims[0]
        else:
            lg.error("(Unlimited) 'time' dimension was not the same across all files, fatal error.")
            sys.exit("(Unlimited) 'time' dimension was not the same across all files, fatal error.")
        return
        
    def camera(self):
        """function to create plots.
        
        :workingfolder: @todo
        :returns: @todo
        """
        framecnt=1
        for f in self.filelist:
            ifile=Dataset(f, 'r')
            name_of_array=ifile.variables[self.variable_name][:]

            plt.close('all')
            fig=plt.figure()

            #this is currently dodge...
            x,y=np.meshgrid(np.arange(np.shape(name_of_array)[2]),np.arange(np.shape(name_of_array)[1]))

            minvar=np.min(name_of_array)
            maxvar=np.max(name_of_array)
            for tstep in np.arange(np.shape(name_of_array)[self.timedim]):
                lg.debug("Working timestep: " + str(framecnt)+ " frames in: " +self.workingfolder)

                ax=fig.add_subplot(111)

                ax.set_title(self.variable_name+' frame num is: ' +str(framecnt))
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
            
                fig.savefig(self.workingfolder+'/moviepar'+str(framecnt).zfill(5)+'.png',dpi=300)
                #fig.savefig('./.pdf',format='pdf')
                fig.clf()
                del ax
                framecnt+=1

    def action(self):
        """function to stitch the movies together!
        
        :returns: @todo
        """

        #ollie's command didn't work on storm
        #ffmpeg -framerate 10 -y -i plot_%04d.png -s:v 1920x1080 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p movie.mp4

        os.chdir(self.workingfolder)
        subprocess.call('ffmpeg -r 15 -qscale 3 -y -an -i ' + 'moviepar%05d.png '+'movie.mov',shell=True)

        #remove png
        if os.path.isfile(self.workingfolder+'movie.mov'):
            ifiles=sorted(glob.glob(self.workingfolder+ 'moviepar*.png' ))
            assert(ifiles!=[]),"glob didn't find anything!"
            for f in ifiles:
                os.remove(f)

            lg.info("MkMov SUCCESS, check it out: "+self.workingfolder+'movie.mov')
        else:
            lg.info("MkMov FAIL")
            lg.error("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")
            sys.exit("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")

if __name__ == "__main__": 
    LogStart('',fout=False)
    #lg.info("demo log message")
    workingfol=tempfile.mkdtemp()+'/'

    dispay_passed_args(workingfol)

    check_dependencies()

    from netCDF4 import Dataset
    import matplotlib.pyplot as plt
    import numpy as np

    movmk=MovMaker(arguments['FILE_NAME'],arguments['VARIABLE_NAME'],workingfol)

    #aah I've always wanted to say this!
    movmk.lights()
    movmk.camera()
    movmk.action()

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
