#!/usr/bin/env python 
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
MkMov v0.3
This is a python script for making movies. In can be used in two ways:
    1] from a netCDF file
    2] from a list of png files (use --stitch option)

Interface is by command line.

Usage:
    mkmov.py -h
    mkmov.py [--min MINIMUM --max MAXIMUM --preview -o OUTPATH] VARIABLE_NAME FILE_NAME...
    mkmov.py --stitch [-o OUTPATH] FILE_NAMES...

Arguments:
    VARIABLE_NAME   variable name
    FILE_NAME       path to NetCDF file to make movie, can also be a list of files (dimensions must be the same)
    FILE_NAMES      list of files to stich with ffmpeg 

Options:
    -h,--help                   : show this help message
    --min MINIMUM               : the minimum value for the contour map 
                                    (nb: if you select a min, you must select a max.)
    --max MAXIMUM               : the maximum value for the contour map
                                    (nb: if you select a max, you must select a min.)
    --preview                   : show a preview of the plot (will exit afterwards).
    -o OUTPATH                  : path/to/folder/to/put/movie/in/moviename.mov  (needs to be absolute path, no relative paths)
    --stitch                    : stitch png files together with ffmpeg (files must be the same dimensions)

Examples: 

python mkmov.py --help

python mkmov.py tos /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/1989/cordex24-ERAI01_1d_19890101_19890105_grid_T_2D.nc 

python mkmov.py tos /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc 

python mkmov.py --min -1 --max 1 --preview zos /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc 

python mkmov.py --stitch -o ~/temp/movie.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/nemo_cordex24_FLATFCNG_ERAI01_sepfinder/19940101_sepfinderplots/moviepar0000*

Tests:

python mkmov.py zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 -o $(pwd)/zos_example.mov zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --stitch -o $(pwd)/stitchmov.mov $(pwd)/examples/StitchMePlots/*.png

"""

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

    #This is the error message if ffmpeg is not installed...
    #The program 'ffmpeg' is currently not installed.  You can install it by typing:
        #sudo apt-get install libav-tools
    try:
        FNULL = open(os.devnull, 'w')
        subprocess.call(["ffmpeg", "--version"],stdout=FNULL, stderr=subprocess.STDOUT)
    except OSError as e:
        lg.error("You don't have ffmpeg installed!")
        sys.exit("You don't have ffmpeg installed!")

    lg.info("Good news: you seem to have all the right software installed!")

def dispay_passed_args(workingfolder):
    """function to print out the passed arguments to the logger

    :workingfolder: @todo
    :returns: @todo
    """
    lg.info("-----------------------------------------------------------------")
    lg.info("MkMov has been run with the following options...")

    if arguments['FILE_NAME']!=[]:
        if len(arguments['FILE_NAME'])==1:
            lg.info("We are making a movie of file: "+ os.path.basename(arguments['FILE_NAME'][0]))
        elif len(arguments['FILE_NAME'])>1:
            lg.info("We are making a movie of file(s): ")
            for cnt,f in enumerate(arguments['FILE_NAME']):
                lg.info("File num: "+str(cnt+1)+'. File is: '+ os.path.basename(f))

        lg.info("Variable we are making a movie of: "+ arguments['VARIABLE_NAME'])

        lg.info("Our working directory is: "+ workingfolder)

        lg.info("")
        lg.info("Optional settings:")

        #for optional parameters...
        if (arguments['--min'] is not None) and (arguments['--max'] is not None):
            lg.info("You have specified a min/max range of: "+arguments['--min']+', '+arguments['--max'] )

        if arguments['--preview']:
            lg.info("You have opted to preview your plot before making a movie.")

        if arguments['-o']:
            lg.info("You have specified you want your movie to live in: " + arguments['-o'])
        lg.info("-----------------------------------------------------------------")
    elif arguments['FILE_NAMES']!=[]:
        lg.info("We are making a movie from your passed list of png files.")
        lg.info("Our working directory is: "+ workingfolder)
        lg.info("")
        lg.info("Optional settings:")

        if arguments['-o']:
            lg.info("You have specified you want your movie to live in: " + arguments['-o'])
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
        """function to do some sanity checks on the files and find out where the time dim is.
        
        """
        lg.info("Lights! Looking at your netCDF files...")
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
        
    def camera(self,minvar=None,maxvar=None,plotpreview=False):
        """function to create plots.
        
        :workingfolder: @todo
        :returns: @todo
        """
        lg.info("Camera! Creating your plots...")
        #get max and min values for timeseries. This is expensive :(
        if (minvar is None) and (maxvar is None):
            mins=[]
            maxs=[]
            for f in self.filelist:
                ifile=Dataset(f, 'r')
                name_of_array=ifile.variables[self.variable_name][:]

                mins.append(np.min(name_of_array))
                maxs.append(np.max(name_of_array))
                ifile.close()

            self.minvar=np.min(mins)
            self.maxvar=np.max(maxs)

        if minvar or maxvar is not None:
            #user specified the range
            self.minvar=float(minvar)
            self.maxvar=float(maxvar)

        framecnt=1
        for f in self.filelist:
            ifile=Dataset(f, 'r')
            name_of_array=ifile.variables[self.variable_name][:]

            plt.close('all')
            fig=plt.figure()

            x,y=np.meshgrid(np.arange(np.shape(name_of_array)[self.timedim+2]),np.arange(np.shape(name_of_array)[self.timedim+1]))

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

                cs1=plt.contourf(x,y,name_of_array[tstep,:,:],levels=np.linspace(self.minvar,self.maxvar,30))

                #land mask...
                cs2=ax.contour(x,y,name_of_array[tstep,:,:].mask,levels=[-1,0],linewidths=1,colors='black')

                plt.colorbar(cs1)
                #plt.show()

                if plotpreview:
                    plt.show()
                    lg.info("Okay, we've shown you your plot, exiting...")
                    sys.exit("Okay, we've shown you your plot, exiting...")
            
                fig.savefig(self.workingfolder+'/moviepar'+str(framecnt).zfill(5)+'.png',dpi=300)
                #fig.savefig('./.pdf',format='pdf')
                fig.clf()
                del ax
                framecnt+=1

            ifile.close()

        #attemp at adding logo at end.
        logo=os.path.dirname(os.path.realpath(__file__))+'/img/'+'mkmov_logo001_splash.png'
        #logo=os.path.dirname(os.path.realpath(__file__))+'/img/'+'mkmovlogo001_resize.png'
        for more in range(20):
            os.symlink(logo,self.workingfolder+'moviepar'+str(framecnt).zfill(5)+'.png')
            framecnt+=1
        #gave up, these could be helpful though:
        #http://superuser.com/questions/628827/can-ffmpeg-encode-video-from-frames-of-different-sizes
        #http://superuser.com/questions/803314/ffmpeg-combine-pngs-of-different-size-into-movie

        #doesn't seem to be supported by my version :(
        #http://ksloan.net/watermarking-videos-from-the-command-line-using-ffmpeg-filters/

    def action(self):
        """function to stitch the movies together!
        
        :returns: @todo
        """
        lg.info("Action! Stitching your plots together with ffmpeg...")

        #ollie's command didn't work on storm
        #ffmpeg -framerate 10 -y -i plot_%04d.png -s:v 1920x1080 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p movie.mp4


        FNULL = open(os.devnull, 'w')

        lg.info("Stitching frames together (might take a bit if you have lots of frames)...")
        if arguments['-o']:
            os.chdir(self.workingfolder)
            subprocess.call('ffmpeg -r 15  -y -an -i ' + 'moviepar%05d.png '+arguments['-o'],shell=True,stdout=FNULL, stderr=subprocess.STDOUT)
        else:
            os.chdir(self.workingfolder)
            subprocess.call('ffmpeg -r 15  -y -an -i ' + 'moviepar%05d.png '+'movie.mov',shell=True,stdout=FNULL, stderr=subprocess.STDOUT)

        #remove png
        if os.path.isfile(self.workingfolder+'movie.mov') or os.path.isfile(arguments['-o']):
            ifiles=sorted(glob.glob(self.workingfolder+ 'moviepar*.png' ))
            assert(ifiles!=[]),"glob didn't find anything!"
            for f in ifiles:
                os.remove(f)

            lg.info("MkMov SUCCESS, check it out: "+self.workingfolder+'movie.mov')
        else:
            lg.info("MkMov FAIL")
            lg.error("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")
            sys.exit("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")

def stitch_action(workingfolder):
    """function to stitch files together using ffmpeg

    :workingfolder: directory where we will create some symlinks
    :returns: @todo
    """
    framecnt=1
    for infile in arguments['FILE_NAMES']:
        os.symlink(infile,workingfolder+'moviepar'+str(framecnt).zfill(5)+'.png')

        framecnt+=1

    #adding logo at end.
    logo=os.path.dirname(os.path.realpath(__file__))+'/img/'+'mkmov_logo001_splash.png'
    for more in range(20):
        os.symlink(logo,workingfolder+'moviepar'+str(framecnt).zfill(5)+'.png')
        framecnt+=1

    lg.info("Stitching frames together (might take a bit if you have lots of frames)...")
    FNULL = open(os.devnull, 'w')
    if arguments['-o']:
        os.chdir(workingfolder)
        subprocess.call('ffmpeg -r 15  -y -an -i ' + 'moviepar%05d.png '+arguments['-o'],shell=True,stdout=FNULL, stderr=subprocess.STDOUT)
        
    else:
        os.chdir(workingfolder)
        subprocess.call('ffmpeg -r 15  -y -an -i ' + 'moviepar%05d.png '+'movie.mov',shell=True,stdout=FNULL, stderr=subprocess.STDOUT)

    #remove png
    if os.path.isfile(workingfolder+'movie.mov') or os.path.isfile(arguments['-o']):
        ifiles=sorted(glob.glob(workingfolder+ 'moviepar*.png' ))
        assert(ifiles!=[]),"glob didn't find any symlinks to remove anything!"
        for f in ifiles:
            os.remove(f)

        if os.path.isfile(workingfolder+'movie.mov'):
            lg.info("MkMov SUCCESS, check it out: "+workingfolder+'movie.mov')

        if arguments['-o']:
            if os.path.isfile(arguments['-o']):
                lg.info("MkMov SUCCESS, check it out: "+arguments['-o'])
    else:
        lg.info("MkMov FAIL")
        lg.error("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")
        sys.exit("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")

if __name__ == "__main__": 
    LogStart('',fout=False)
    #print arguments
    workingfol=tempfile.mkdtemp()+'/'

    dispay_passed_args(workingfol)

    check_dependencies()

    #We are in making movie mode...
    #main.py [--min MINIMUM --max MAXIMUM --preview] VARIABLE_NAME FILE_NAME...
    if arguments['FILE_NAME']!=[]:
        from netCDF4 import Dataset
        if not arguments['--preview']:
            #for travis-ci
            import matplotlib
            matplotlib.use('Agg')
        import matplotlib.pyplot as plt
        import numpy as np

        movmk=MovMaker(arguments['FILE_NAME'],arguments['VARIABLE_NAME'],workingfol)

        #aah I've always wanted to say this!
        movmk.lights()
        movmk.camera(minvar=arguments['--min'],maxvar=arguments['--max'],plotpreview=arguments['--preview'])
        movmk.action()
    #We are in stitching mode
    #main.py --stitch  FILE_NAMES...
    elif arguments['FILE_NAMES']!=[]:
        stitch_action(workingfol)

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
