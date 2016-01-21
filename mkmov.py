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

Interface is by command line. Fully working examples can be found in: run_mkmov_examples.sh

Usage:
    mkmov.py -h
    mkmov.py [--min MINIMUM --max MAXIMUM --preview -o OUTPATH --lmask LANDVAR --fps FRATE --cmap PLTCMAP --clev LEVELS --4dvar DEPTHLVL --figwth WIDTH --fighgt HEIGHT] VARIABLE_NAME FILE_NAME...
    mkmov.py --stitch [-o OUTPATH --fps FRATE] FILE_NAMES...

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
    --lmask LANDVAR             : land value to mask out (will draw a solid black contour around the land points)
    --fps FRATE                 : frames rate in final movie (default is 15). Suggest keeping values above 10.
    --cmap PLTCMAP              : matplotlib color map to contourf with. See [1] for options.
    --clev LEVELS               : number of colour levels to have on the contour map (default is 50).
    --4dvar DEPTHLVL            : passing 4d variable of the form (time,depth,spatialdim1,spatialdim2), DEPTHLVL is the depth/height level you would like to plot (default is level 0).
    --figwth WIDTH              : figure width (nb: if you select a width then you must also specify height)
    --fighgt HEIGHT             : figure height (nb: if you select a height then you must also specify width)
    --stitch                    : stitch png files together with ffmpeg (files must be the same dimensions)

Example tests (should work 'out of the box'):
python mkmov.py zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 -o $(pwd)/zos_example.mov zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 --lmask 0 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 --lmask 0 --fps 10 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 --lmask 0 --fps 10 --cmap jet zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 --lmask 0 --fps 10 --cmap autumn --clev 60 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 --lmask 0 --figwth 10 --fighgt 12 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --stitch -o $(pwd)/stitchmov.mov $(pwd)/examples/StitchMePlots/*.png
python mkmov.py --stitch -o $(pwd)/stitchmov.mov --fps 10 $(pwd)/examples/StitchMePlots/*.png

References:
    [1] http://matplotlib.org/examples/color/colormaps_reference.html
"""

from docopt import docopt
arguments = docopt(__doc__)
import sys,os
from cb2logger import *
import imp
import tempfile
import subprocess

import glob

def mkdir(p):
    """make directory of path that is passed"""
    try:
       os.makedirs(p)
       lg.info("output folder: "+p+ " does not exist, we will make one.")
    except OSError as exc: # Python >2.5
       import errno
       if exc.errno == errno.EEXIST and os.path.isdir(p):
          pass
       else: raise

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

        #error check to make sure both min and max were passed
        if (arguments['--min'] is not None) and (arguments['--max'] is None):
            lg.error("You passed min but not max")
            sys.exit("You passed min but not max")
        elif(arguments['--min'] is None) and (arguments['--max'] is not None): 
            lg.error("You passed max but not min")
            sys.exit("You passed max but not min")

        if arguments['--preview']:
            lg.info("You have opted to preview your plot before making a movie.")

        if arguments['-o']:
            lg.info("You want your movie to live in: " + arguments['-o'])

        if arguments['--lmask']:
            lg.info("You want to mask out the following values: " + arguments['--lmask'])

        if arguments['--fps']:
            lg.info("You have said your final movie will be: " + \
                    str(int(arguments['--fps']))+"  frames per second.")

        if arguments['--cmap']:
            lg.info("You have said you would like to contourf with the following matplotlib colour map: " + \
                    arguments['--cmap'])

        if arguments['--clev']:
            lg.info("You have said you would like to contourf with the following number of levels: " + \
                    str(int(arguments['--clev'])))

        if arguments['--4dvar']:
            lg.info("You have passed a 4 dimensional variable (time,depth,spatialdim1,spatialdim2) and would like to plot DEPTHLVL: " + \
                    str(int(arguments['--4dvar'])))

        if (arguments['--figwth'] is not None) and (arguments['--fighgt'] is not None):
            lg.info("You have specified figure dimensions of: "+arguments['--figwth']+', '+arguments['--fighgt'] + ' (width,height).')

        #error check to make sure both figwith and fighgt were passed
        if (arguments['--figwth'] is not None) and (arguments['--fighgt'] is None):
            lg.error("You passed figwth but not fighgt")
            sys.exit("You passed figwth but not fighgt")
        elif(arguments['--figwth'] is None) and (arguments['--fighgt'] is not None): 
            lg.error("You passed fighgt but not figwth")
            sys.exit("You passed fighgt but not figwth")

        lg.info("-----------------------------------------------------------------")
    elif arguments['FILE_NAMES']!=[]:
        lg.info("We are making a movie from your passed list of png files.")
        lg.info("Our working directory is: "+ workingfolder)
        lg.info("")
        lg.info("Optional settings:")

        if arguments['-o']:
            lg.info("You have specified you want your movie to live in: " + arguments['-o'])

        if arguments['--fps']:
            lg.info("You have said your final movie will be: " + \
                    str(int(arguments['--fps']))+"  frames per second.")

        lg.info("-----------------------------------------------------------------")
    return

def call_ffmpeg(pngfolder):
    """function that actually calls ffmpeg to stitch all the png together
    
    :pngfolder: folder where all the pngs are that we are stitching together
    :returns: None (except for a movie!)
    """
    #ollie's command didn't work on storm
    # os.chdir(pngfolder)
    # subprocess.call('ffmpeg -framerate 10 -y -i moviepar%05d.png -s:v 1920x1080 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p movie.mp4')

    # ffmpeg ideas:
    # ffmpeg -r 15 -i moviepar%05d.png -b 5000k -vcodec libx264 -y -an movie.mov

    lg.info("Stitching frames together (might take a bit if you have lots of frames)...")

    FNULL = open(os.devnull, 'w')

    if arguments['--fps']:
        fps=str(int(arguments['--fps']))
    else:
        fps=str(15)

    quality='20'
    if arguments['-o']:
        os.chdir(pngfolder)
        subprocess.call('ffmpeg -r '+fps+' -i moviepar%05d.png -vb '+quality+'M -y -an '+arguments['-o'],shell=True,stdout=FNULL, stderr=subprocess.STDOUT)
    else:
        os.chdir(pngfolder)
        subprocess.call('ffmpeg -r '+fps+' -i moviepar%05d.png -vb '+quality+'M -y -an movie.mov',shell=True,stdout=FNULL, stderr=subprocess.STDOUT)

    #qscale doesn't work on some versions of ffmpeg... Check if we have a file, if not, try no qscale arg
    # nofile=False
    # if not os.path.isfile(pngfolder+'movie.mov'):
        # nofile=True
    
    # if arguments['-o']:
        # if not os.path.isfile(arguments['-o']):
            # nofile=True

    # if nofile:
        # qscale=' '
        # if arguments['-o']:
            # os.chdir(pngfolder)
            # subprocess.call('ffmpeg -r '+fps+qscale+'-y -an -i ' + 'moviepar%05d.png '+arguments['-o'],shell=True,stdout=FNULL, stderr=subprocess.STDOUT)
        # else:
            # os.chdir(pngfolder)
            # subprocess.call('ffmpeg -r '+fps+qscale+'-y -an -i ' + 'moviepar%05d.png '+'movie.mov',shell=True,stdout=FNULL, stderr=subprocess.STDOUT)

    #remove png
    if os.path.isfile(pngfolder+'movie.mov') or os.path.isfile(arguments['-o']):
        ifiles=sorted(glob.glob(pngfolder+ 'moviepar*.png' ))
        assert(ifiles!=[]),"glob didn't find any symlinks to remove anything!"
        for f in ifiles:
            os.remove(f)

        if os.path.isfile(pngfolder+'movie.mov'):
            lg.info("MkMov SUCCESS, check it out: "+pngfolder+'movie.mov')

        if arguments['-o']:
            if os.path.isfile(arguments['-o']):
                lg.info("MkMov SUCCESS, check it out: "+arguments['-o'])
    else:
        lg.info("MkMov FAIL")
        lg.error("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")
        sys.exit("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")


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

            #what shape is the passed variable? Do some error checks
            self.var_len=len(ifile.variables[self.variable_name].shape)
            if self.var_len==2:
                if len(arguments['FILE_NAMES'])==1:
                    #h'm haven't actually tried this! 
                    lg.error("Variable: " + str(self.variable_name) + " has only two dimensions and you only fed mkmov one file so I don't know where your time dimension is.")
                elif len(arguments['FILE_NAMES'])>1: #have tested this on AVISO works okay
                    pass
                    
            #the 'obvious' case; one file with one time dim and two spatial dims
            if self.var_len==3: 
                pass

            #tricky, which dims are time/random_dim/spatial1/spatial2?
            if self.var_len==4:
                if arguments['--4dvar']:
                    lg.debug("Variable: " + str(self.variable_name) + " has four dimensions. Following your argument, we will plot depth level: "+arguments['--4dvar'] )
                    self.depthlvl=int(arguments['--4dvar'])
                else:
                    lg.warning("Variable: " + str(self.variable_name) + " has four dimensions. MkMov will assume the second dim is depth/height and plot the first level.")
                    self.depthlvl=0

            #find unlimited dimension
            findunlim=[ifile.dimensions[dim].isunlimited() for dim in ifile.dimensions.keys()]
            dim_unlim_num=[i for i, x in enumerate(findunlim) if x]
            if len(dim_unlim_num)==0:
                lg.warning("Input file: " + str(os.path.basename(f))  + " has no unlimited dimension, which dim is time?")
                # sys.exit("Input file: " + str(os.path.basename(f))  + " has no unlimited dimension, which dim is time?")
            elif len(dim_unlim_num)>1:
                lg.warning("Input file: " + str(os.path.basename(f))  + " has more than one unlimited dimension.")
                # sys.exit("Input file: " + str(os.path.basename(f))  + " has more than one unlimited dimension.")
            else:
                timename=ifile.dimensions.keys()[dim_unlim_num[0]]
                var_timedim=[i for i, x in enumerate(ifile.variables[self.variable_name].dimensions) if x==timename][0]
                var_timedims.append(var_timedim)
                ifile.close()
                continue #NOTE I'm a continue!

            #okay so we didn't find time as an unlimited dimension, perhaps it has a sensible name?
            if 'time' in ifile.dimensions.keys():
                timename='time'
            elif 't' in ifile.dimensions.keys():
                timename='t'
            elif 'Time' in ifile.dimensions.keys():
                timename='Time'
            else:
                timename=''

            if timename!='':
                lg.info("Good news, we think we found the time dimension it's called: " + timename )
                var_timedim=[i for i, x in enumerate(ifile.variables[self.variable_name].dimensions) if x==timename][0]
                var_timedims.append(var_timedim)

            ifile.close()

        #check all time dimensions are in the same place across all files..
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
        def getdata():
            """function that grabs the data
            :returns: nparray
            """
            if self.var_len==4:
                var_nparray=ifile.variables[self.variable_name][:,self.depthlvl,:,:]
            else:
                var_nparray=ifile.variables[self.variable_name][:]
        
            return var_nparray

        lg.info("Camera! Creating your plots...")

        #get max and min values for timeseries. This is expensive :(
        if (minvar is None) and (maxvar is None):
            mins=[]
            maxs=[]
            for f in self.filelist:
                ifile=Dataset(f, 'r')
                name_of_array=getdata()

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
            name_of_array=getdata()

            plt.close('all')

            if (arguments['--figwth'] is not None) and (arguments['--fighgt'] is not None):
                #width then height
                fig=plt.figure(figsize=(float(arguments['--figwth']),float(arguments['--fighgt'])))
            else:
                fig=plt.figure()

            x,y=np.meshgrid(np.arange(np.shape(name_of_array)[self.timedim+2]),\
                    np.arange(np.shape(name_of_array)[self.timedim+1]))

            minvar=np.min(name_of_array)
            maxvar=np.max(name_of_array)

            #h'm the following loop has a problem, because if tstep isn't in dim 0 we are screwed! (probably needs some fancy syntax to slice out of name_of_array (hard without google)
            if self.timedim!=0:
                lg.error("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")
                sys.exit("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")

            for tstep in np.arange(np.shape(name_of_array)[self.timedim]):
                lg.debug("Working timestep: " + str(framecnt)+ " frames in: " +self.workingfolder)

                ax=fig.add_subplot(111)

                ax.set_title(self.variable_name+' frame num is: ' +str(framecnt))
                #ax.set_xlabel('msg')
                #ax.set_ylabel('msg')

                if arguments['--lmask']:
                    name_of_array= np.ma.masked_where(
                        name_of_array==float(arguments['--lmask']),
                        name_of_array) 

                    #land mask...
                    cs2=ax.contour(x,y,name_of_array[tstep,:,:].mask,levels=[-1,0],linewidths=1,colors='black')


                if arguments['--clev']:
                    cnt_levelnum=int(arguments['--clev'])
                else:
                    cnt_levelnum=50

                if not arguments['--cmap']:
                    cs1=plt.contourf(x,y,name_of_array[tstep,:,:],\
                            levels=np.linspace(self.minvar,self.maxvar,cnt_levelnum))
                else:
                    cs1=plt.contourf(x,y,name_of_array[tstep,:,:],\
                            levels=np.linspace(self.minvar,self.maxvar,cnt_levelnum),\
                            cmap=arguments['--cmap'])

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
        nologo=False
        for more in range(20):
            try:
                os.symlink(logo,self.workingfolder+'moviepar'+str(framecnt).zfill(5)+'.png')
            except OSError:
                nologo=True
                break
            framecnt+=1

        if nologo:
            #on some file systems, like some network shares,  we can't make symlinks ..
            lg.warning("Couldn't insert the logo at the end, sorry!")


    def action(self):
        """function to stitch the movies together!
        
        :returns: @todo
        """
        lg.info("Action! Stitching your plots together with ffmpeg...")

        call_ffmpeg(self.workingfolder)

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
    nologo=False
    for more in range(20):
        try:
            os.symlink(logo,workingfolder+'moviepar'+str(framecnt).zfill(5)+'.png')
        except OSError:
            nologo=True
            break
        framecnt+=1

    if nologo:
        #on some file systems, like some network shares,  we can't make symlinks ..
        lg.warning("Couldn't insert the logo at the end, sorry!")

    call_ffmpeg(workingfolder)

if __name__ == "__main__": 
    LogStart('',fout=False)
    # print arguments
    if not arguments['-o']:
        workingfol=tempfile.mkdtemp()+'/'
    else:
        workingfol=os.path.dirname(arguments['-o'])+'/mkmovTEMPFOL4_'+\
                os.path.basename(arguments['-o'])[:-4]+'/'
        if os.path.exists(workingfol):
            lg.error("Working folder: " + workingfol+". already exists, has mkmov failed previously? Please remove and restart.")
            sys.exit("Working folder: " + workingfol+". already exists, has mkmov failed previously? Please remove and restart.")
        mkdir(workingfol)

    dispay_passed_args(workingfol)

    check_dependencies()

    #We are in making movie mode...
    #main.py [OPTIONS] VARIABLE_NAME FILE_NAME...
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

    #remove working folder
    if arguments['-o']:
        if os.path.exists(workingfol):
            if not os.listdir(workingfol):
                os.rmdir(workingfol)
                lg.info("Working folder: " + workingfol +" removed.")
            else:
                lg.warning("Working directory: " + workingfol+" not empty, please remove manually")
    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
