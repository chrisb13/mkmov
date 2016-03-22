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
MkMov v0.4
This is a python package for making movies. It has three things it can do:
    [T1] movie of a netCDF file plotting contourf output (see "python mkmov.py 2d -h");
    [T2] movie of a netCDF file plotting slices of a 3d variable as a 3d cube (see "python mkmov.py 3dcube -h");
    [T3] movie of a netCDF file plotting a 2d variable as a 3d surface (see "python mkmov.py 3dsurf -h");
    [T4] stitch a list of png files into a movie ("see python mkmov.py stitch -h").

Usage: 
    mkmov.py -h --help
    mkmov.py <command> [-h --help] [<args>...]

Commands:
   2d          [T1] use a netCDF file make a contourf of a 2d field
   3dcube      [T2] use a netCDF file make a movie of a 3d field as a 3d cube
   3dsurf      [T3] use a netCDF file make a movie of a 2d field as a 3d surface
   stitch      [T4] stitch files together using ffmpeg
   examples    show some examples of commands that work 'out of the box'

See 'python mkmov.py help <command>' for more information on a specific command.

Options:
    -h,--help                   : show this help message
"""

TWOD=\
"""
MkMov: sub-command "2d" help.
    [T1] movie of a netCDF file plotting contourf output.

Usage: 
    mkmov.py [--min MINIMUM --max MAXIMUM --preview --bias TIMENAME --bcmapcentre -o OUTPATH --lmask LANDVAR --lmask2 LANDVAR2 --lmaskfld --fps FRATE --cmap PLTCMAP --clev LEVELS --4dvar DEPTHLVL --figwth WIDTH --fighgt HEIGHT --x XVARIABLE --y YVARIABLE --killsplash] VARIABLE_NAME FILE_NAME...

Arguments:
    VARIABLE_NAME   variable name
    FILE_NAME       path to NetCDF file to make movie, can also be a list of files (dimensions must be the same)
    FILE_NAMES      list of files to stich with ffmpeg 

Options:
    -h,--help                   : show this help message
    --min MINIMUM               : the minimum value for the contour map (nb: if you select a min, you must select a max.)
    --max MAXIMUM               : the maximum value for the contour map (nb: if you select a max, you must select a min.)
    --preview                   : show a preview of the plot (will exit afterwards).
    --bias TIMENAME             : create a movie with bias from the mean (this requires NCO tools to be installed). Need to pass the name of the time dimension so we can use NCO tools.
    --bcmapcentre               : bias movie with centre around zero (need to also specify --cmap AND --bias)
    -o OUTPATH                  : path/to/folder/to/put/movie/in/moviename.mov  (needs to be absolute path, no relative paths)
    --lmask LANDVAR             : land value to mask out (will draw a solid black contour around the land points)
    --lmask2 LANDVAR2           : second land value to mask out (weird case where MOM6 has two landmask values! This option is unusual! (nb: if you select lmask2, you must specify lmask)
    --lmaskfld                  : fill in landmask (as specified in lmask. nb: if you select lmaskfld, you must specify lmask)
    --fps FRATE                 : frames rate in final movie (default is 15). Suggest keeping values above 10.
    --cmap PLTCMAP              : matplotlib color map to contourf with. See [1] for options.
    --clev LEVELS               : number of colour levels to have on the contour map (default is 50).
    --4dvar DEPTHLVL            : passing 4d variable of the form (time,depth,spatialdim1,spatialdim2), DEPTHLVL is the depth/height level you would like to plot (default is level 0).
    --figwth WIDTH              : figure width (nb: if you select a width then you must also specify height)
    --fighgt HEIGHT             : figure height (nb: if you select a height then you must also specify width)
    --x XVARIABLE               : variable to plot on the x-axis (nb: if you specify a xvariable, you must select a yvariable.)
    --y YVARIABLE               : variable to plot on the y-axis (nb: if you specify a yvariable, you must select a xvariable.)
    --killsplash                : do not display splash screen advertisement for MkMov at end of movie
    --stitch                    : stitch png files together with ffmpeg (files must be the same dimensions). Use absolute not relative path.

References:
    [1] http://matplotlib.org/examples/color/colormaps_reference.html
"""

cube3d = \
"""
MkMov: sub-command "3dcube" help.
    [T2] movie of a netCDF file plotting slices of a 3d variable as a 3d cube.

Usage: basic.py 3dcube [options] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].
"""

surf3d = \
"""
MkMov: sub-command "3dsurf" help.
    [T3] movie of a netCDF file plotting a 2d variable as a 3d surface.

Usage: basic.py 3dsurf [options] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].
"""

STITCH = \
"""
MkMov: sub-command "stitch" help.
    [T4] stitch a list of png files into a movie ("see python mkmov.py stitch -h").

Usage: 
    mkmov.py stitch -h
    mkmov.py stitch [-o OUTPATH --fps FRATE --killsplash] FILE_NAMES...

Arguments:
    FILE_NAMES      list of files to stitch with ffmpeg 

Options:
    -h --help                   : Show this screen.
    -o OUTPATH                  : path/to/folder/to/put/movie/in/moviename.mov  (needs to be absolute path, no relative paths)
    --fps FRATE                 : frames rate in final movie (default is 15). Suggest keeping values above 10.
    --killsplash                : do not display splash screen advertisement for MkMov at end of movie
"""

EXAMPLES=\
"""
python mkmov.py 2d zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 -o $(pwd)/zos_example.mov zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --fps 10 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --fps 10 --cmap jet zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --fps 10 --cmap autumn --clev 60 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --figwth 10 --fighgt 12 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --figwth 10 --fighgt 12 --killsplash zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py stitch -o $(pwd)/stitchmov.mov $(pwd)/examples/StitchMePlots/*.png
python mkmov.py stitch -o $(pwd)/stitchmov.mov --fps 10 $(pwd)/examples/StitchMePlots/*.png
python mkmov.py stitch -o $(pwd)/stitchmov.mov --fps 10 --killsplash $(pwd)/examples/StitchMePlots/*.png
"""

from docopt import docopt
# arguments = docopt(__doc__)


import mkmov.commands as sc

import sys,os
from cb2logger import *
import imp
import tempfile
import subprocess

import glob

#for cmap_center_point_adjust function
import math
import copy
from matplotlib import colors
import matplotlib


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

        #create bias files
        if arguments['--bias']:
            #following example in http://linux.die.net/man/1/ncdiff
            ncout='ncra '+' '.join(self.filelist)+' '+workingfol+'mean.nc'
            lg.info("Creating mean file: " + ncout)
            subprocess.call(ncout,shell=True)

            ncout='ncwa -O -a '+arguments['--bias']+' '+workingfol+'mean.nc '+workingfol+'mean_notime.nc'
            lg.info("Removing time dimension from mean file: " + ncout)
            subprocess.call(ncout,shell=True)

            difffol=workingfol+'difffiles/'
            mkdir(workingfol+'difffiles/')
            newfilelist=[]
            cnt=0
            for f in self.filelist:
                ncout='ncdiff '+' '+f+' '+workingfol+'mean_notime.nc '+difffol+os.path.basename(f)[:-3]+'_diff_'+str(cnt).zfill(5)+'.nc'
                lg.info("Creating anomaly file: " + ncout)
                subprocess.call(ncout,shell=True)
                newfilelist.append(difffol+os.path.basename(f)[:-3]+'_diff_'+str(cnt).zfill(5)+'.nc')
                cnt+=1

            self.filelist=newfilelist
                
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

            ifile_dim_keys=list(dict(ifile.dimensions).keys())

            #find unlimited dimension
            findunlim=[ifile.dimensions[dim].isunlimited() for dim in ifile_dim_keys]
            dim_unlim_num=[i for i, x in enumerate(findunlim) if x]
            if len(dim_unlim_num)==0:
                lg.warning("Input file: " + str(os.path.basename(f))  + " has no unlimited dimension, which dim is time?")
                # sys.exit("Input file: " + str(os.path.basename(f))  + " has no unlimited dimension, which dim is time?")
            elif len(dim_unlim_num)>1:
                lg.warning("Input file: " + str(os.path.basename(f))  + " has more than one unlimited dimension.")
                # sys.exit("Input file: " + str(os.path.basename(f))  + " has more than one unlimited dimension.")
            else:
                timename=ifile_dim_keys[dim_unlim_num[0]]
                var_timedim=[i for i, x in enumerate(ifile.variables[self.variable_name].dimensions) if x==timename][0]
                var_timedims.append(var_timedim)
                ifile.close()
                continue #NOTE I'm a continue!

            #okay so we didn't find time as an unlimited dimension, perhaps it has a sensible name?
            if 'time' in ifile_dim_keys:
                timename='time'
            elif 't' in ifile_dim_keys:
                timename='t'
            elif 'Time' in ifile_dim_keys:
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

            #not ideal really, this thing being in the loop
            if (arguments['--x'] is not None) and (arguments['--y'] is not None):
                ifile=Dataset(f, 'r')
                xvar=ifile.variables[arguments['--x']][:]
                yvar=ifile.variables[arguments['--y']][:]
                x,y=np.meshgrid(xvar,yvar)
            else:
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

                    #weird case where we have two landmasks... (i.e. MOM5_010)
                    if arguments['--lmask2']:
                        name_of_array= np.ma.masked_where(
                            name_of_array==float(arguments['--lmask2']),
                            name_of_array) 

                    if not arguments['--lmaskfld']:
                        #land mask...
                        cs2=ax.contour(x,y,name_of_array[tstep,:,:].mask,levels=[-1,0],linewidths=1,colors='black')
                    else:
                        cs2=ax.contourf(x,y,name_of_array[tstep,:,:].mask,levels=[-1,0,1],colors=('#B2D1FF','#858588'),alpha=.9) #landmask


                if arguments['--clev']:
                    cnt_levelnum=int(arguments['--clev'])
                else:
                    cnt_levelnum=50

                if not arguments['--cmap']:
                    cs1=plt.contourf(x,y,name_of_array[tstep,:,:],\
                            levels=np.linspace(self.minvar,self.maxvar,cnt_levelnum))
                else:

                    if arguments['--bcmapcentre']:
                        #will plot colourmap centred around zero
                        oldcmap=matplotlib.cm.get_cmap(arguments['--cmap'])
                        shiftd=cmap_center_point_adjust(oldcmap,[self.minvar,self.maxvar],0)
                        cs1=plt.contourf(x,y,name_of_array[tstep,:,:],\
                                levels=np.linspace(self.minvar,self.maxvar,cnt_levelnum),\
                                cmap=shiftd)
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

        if not arguments['--killsplash']:
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

    if not arguments['--killsplash']:
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

def workingfol_func():
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
            lg.error("Working folder: " + workingfol+". already exists, has mkmov failed previously? Please remove and restart.")
            sys.exit("Working folder: " + workingfol+". already exists, has mkmov failed previously? Please remove and restart.")
        mkdir(workingfol)

    return

def greet(args):
    print(args)

if __name__ == "__main__": 
    LogStart('',fout=False)


    arguments_top = docopt(__doc__, options_first=True)

    if arguments_top['<command>'] == '2d':
        arguments=docopt(TWOD)

        workingfol_func()

        # import ipdb
        # ipdb.set_trace()
        # sc.dispay_passed_args(arguments,workingfol)
    elif arguments_top['<command>'] == '3dcube':
        greet(docopt(cube3d))
    elif arguments_top['<command>'] == '3dsurf':
        greet(docopt(surf3d))
    elif arguments_top['<command>'] == 'stitch':
        greet(docopt(STITCH))
    elif arguments_top['<command>'] == 'examples':
        print(EXAMPLES)
    #display help messages
    #this needs to be above, what comes next...
    elif arguments_top['<command>'] == 'help' and len(arguments_top['<args>'])==0:
        subprocess.call(['python','mkmov.py', '--help'])
    elif arguments_top['<command>'] == 'help' and (arguments_top['<args>'][0] in '2d 3dcube 3dsurf stitch examples'.split()):
        subprocess.call(['python','mkmov.py', arguments_top['<args>'][0],'--help'])
    elif arguments_top['<command>'] == 'help' and not (arguments_top['<args>'][0] in '2d 3dcube 3dsurf stitch examples'.split()):
        print "I don't recognise that sub-command"
    else:
        print "error"





    # dispay_passed_args(workingfol)

    # check_dependencies()

    # #We are in making movie mode...
    # #main.py [OPTIONS] VARIABLE_NAME FILE_NAME...
    # if arguments['FILE_NAME']!=[]:
        # from netCDF4 import Dataset
        # if not arguments['--preview']:
            # #for travis-ci
            # import matplotlib
            # matplotlib.use('Agg')
        # import matplotlib.pyplot as plt
        # import numpy as np

        # movmk=MovMaker(arguments['FILE_NAME'],arguments['VARIABLE_NAME'],workingfol)

        # #aah I've always wanted to say this!
        # movmk.lights()
        # movmk.camera(minvar=arguments['--min'],maxvar=arguments['--max'],plotpreview=arguments['--preview'])
        # movmk.action()
    # #We are in stitching mode
    # #main.py --stitch  FILE_NAMES...
    # elif arguments['FILE_NAMES']!=[]:
        # stitch_action(workingfol)

    # #remove working folder
    # if arguments['-o']:
        # if os.path.exists(workingfol):
            # #remove temp files from bias movie making
            # if arguments['--bias']:
                # tempfiles=\
                # sorted(glob.glob(workingfol+'*.nc'))+\
                # sorted(glob.glob(workingfol+'difffiles/*.nc'))
                # for f in tempfiles:
                    # os.remove(f)
                # os.rmdir(workingfol+'difffiles/')

            # if not os.listdir(workingfol):
                # os.rmdir(workingfol)
                # lg.info("Working folder: " + workingfol +" removed.")
            # else:
                # lg.warning("Working directory: " + workingfol+" not empty, please remove manually")

    lg.info('')
    localtime = time.asctime( time.localtime(time.time()) )
    lg.info("Local current time : "+ str(localtime))
    lg.info('SCRIPT ended')
