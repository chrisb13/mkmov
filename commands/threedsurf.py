from netCDF4 import Dataset
import numpy as np
import os,sys
from ._threedsurf import _LogStart
_lg=_LogStart().setup()

#needed to add this for python 3 support...
from .scf import call_ffmpeg,axisEqual3D

"""
MkMov: sub-command "3dsurf" workhorse file.
"""

def dispay_passed_args_threedsurf(arguments,workingfolder):
    """function to print out the passed arguments to the logger

    :workingfolder: @todo
    :returns: @todo
    """
    _lg.info("-----------------------------------------------------------------")
    _lg.info("MkMov has been run with the following options...")

    if len(arguments['FILE_NAME'])==1:
        _lg.info("We are making a movie of file: "+ os.path.basename(arguments['FILE_NAME'][0]))
    elif len(arguments['FILE_NAME'])>1:
        _lg.info("We are making a movie of file(s): ")
        for cnt,f in enumerate(arguments['FILE_NAME']):
            _lg.info("File num: "+str(cnt+1)+'. File is: '+ os.path.basename(f))

    _lg.info("Variable we are making a movie of: "+ arguments['VARIABLE_NAME'])

    _lg.info("Our working directory is: "+ workingfolder)

    _lg.info("")
    _lg.info("Optional settings:")

    if arguments['--preview']:
        _lg.info("You have opted to preview your plot before making a movie.")

    #for optional parameters...
    if (arguments['--min'] is not None) and (arguments['--max'] is not None):
        _lg.info("You have specified a min/max range of: "+arguments['--min']+', '+arguments['--max'] )

    #error check to make sure both min and max were passed
    if (arguments['--min'] is not None) and (arguments['--max'] is None):
        _lg.error("You passed min but not max")
        sys.exit("You passed min but not max")
    elif(arguments['--min'] is None) and (arguments['--max'] is not None): 
        _lg.error("You passed max but not min")
        sys.exit("You passed max but not min")

    _lg.info("-----------------------------------------------------------------")
    return

class MovMakerThreeDSurf(object):
    """
    Class to create movie based on file list and variable name.

    Parameters
    ----------
    :filelist:
    variable_name: 
    :workingfolder: @todo
    :argu: @todo

    Returns
    -------
    
    Notes
    -------
    

    Example
    --------
    >>> 
    >>> 
    """

    def __init__(self, filelist,variable_name,workingfolder,argu):
        self.filelist,self.variable_name = filelist,variable_name
        self.workingfolder=workingfolder
        self.arguments=argu

    def lights(self):
        """function to do some sanity checks on the files and find out where the time dim is.
        
        """
        _lg.info("Lights! Looking at your netCDF files...")
        var_timedims=[]
                
        #error checks files, are all similar
        for f in self.filelist:
            if not os.path.exists(f):
                _lg.error("Input file: " + str(os.path.basename(f))  + " does not exist.")
                sys.exit("Input file: " + str(os.path.basename(f))  + " does not exist.")

            ifile=Dataset(f, 'r')

            if self.variable_name not in ifile.variables.keys():
                _lg.error("Variable: " + str(self.variable_name) + " does not exist in netcdf4 file.")
                sys.exit("Variable: " + str(self.variable_name) + " does not exist in netcdf4 file.")

            #what shape is the passed variable? Do some error checks
            self.var_len=len(ifile.variables[self.variable_name].shape)
            if self.var_len==2:
                if len(self.arguments['FILE_NAMES'])==1:
                    #h'm haven't actually tried this! 
                    _lg.error("Variable: " + str(self.variable_name) + " has only two dimensions and you only fed mkmov one file so I don't know where your time dimension is.")
                elif len(self.arguments['FILE_NAMES'])>1: #have tested this on AVISO works okay
                    pass
                    
            #the 'obvious' case; one file with one time dim and two spatial dims
            if self.var_len==3: 
                pass

            #tricky, which dims are time/random_dim/spatial1/spatial2?
            if self.var_len==4:
                if self.arguments['--4dvar']:
                    _lg.debug("Variable: " + str(self.variable_name) + " has four dimensions. Following your argument, we will plot depth level: "+self.arguments['--4dvar'] )
                    self.depthlvl=int(self.arguments['--4dvar'])
                else:
                    _lg.warning("Variable: " + str(self.variable_name) + " has four dimensions. MkMov will assume the second dim is depth/height and plot the first level.")
                    self.depthlvl=0

            ifile_dim_keys=list(dict(ifile.dimensions).keys())

            #find unlimited dimension
            findunlim=[ifile.dimensions[dim].isunlimited() for dim in ifile_dim_keys]
            dim_unlim_num=[i for i, x in enumerate(findunlim) if x]
            if len(dim_unlim_num)==0:
                _lg.warning("Input file: " + str(os.path.basename(f))  + " has no unlimited dimension, which dim is time?")
                # sys.exit("Input file: " + str(os.path.basename(f))  + " has no unlimited dimension, which dim is time?")
            elif len(dim_unlim_num)>1:
                _lg.warning("Input file: " + str(os.path.basename(f))  + " has more than one unlimited dimension.")
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
                _lg.info("Good news, we think we found the time dimension it's called: " + timename )
                var_timedim=[i for i, x in enumerate(ifile.variables[self.variable_name].dimensions) if x==timename][0]
                var_timedims.append(var_timedim)

            ifile.close()

        #check all time dimensions are in the same place across all files..
        if var_timedims[1:]==var_timedims[:-1]:
            self.timedim=var_timedims[0]
        else:
            _lg.error("(Unlimited) 'time' dimension was not the same across all files, fatal error.")
            sys.exit("(Unlimited) 'time' dimension was not the same across all files, fatal error.")
        return

    def camera(self,minvar=None,maxvar=None):
        """function to create plots.
        
        :workingfolder: @todo
        :returns: @todo
        """
        #this is poor form, violates pep8! but means we can pick a backend for travis-ci testing...
        import matplotlib.pyplot as plt
        from matplotlib import cm
        from mpl_toolkits.mplot3d import Axes3D

        def getdata():
            """function that grabs the data
            :returns: nparray
            """
            if self.var_len==4:
                var_nparray=ifile.variables[self.variable_name][:,self.depthlvl,:,:]
            else:
                var_nparray=ifile.variables[self.variable_name][:]
        
            return var_nparray

        _lg.info("Camera! Creating your plots...")

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
        plt.close('all')
        for f in self.filelist:
            ifile=Dataset(f, 'r')
            name_of_array=getdata()

            fig=plt.figure()

            X = np.linspace(-5, 5, np.shape(name_of_array)[self.timedim+2])
            Y = np.linspace(-5, 5, np.shape(name_of_array)[self.timedim+1])
            x, y = np.meshgrid(X, Y)

            minvar=np.min(name_of_array)
            maxvar=np.max(name_of_array)

            #h'm the following loop has a problem, because if tstep isn't in dim 0 we are screwed! (probably needs some fancy syntax to slice out of name_of_array (hard without google)
            if self.timedim!=0:
                _lg.error("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")
                sys.exit("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")

            for tstep in np.arange(np.shape(name_of_array)[self.timedim]):
                _lg.debug("Working timestep: " + str(framecnt)+ " frames in: " +self.workingfolder)

                ax = fig.gca(projection='3d')

                ax.set_title(self.variable_name+' frame num is: ' +str(framecnt))

                surf = ax.plot_surface(x, y, name_of_array[tstep,:,:], rstride=1, cstride=1, cmap=cm.seismic,
                                       linewidth=0, antialiased=False,vmin=self.minvar,vmax=self.maxvar)

                cset = ax.contourf(x, y, name_of_array[tstep,:,:], zdir='z', offset=-1.6,
                                levels=np.linspace(self.minvar,self.maxvar,30),cmap=plt.cm.jet)

                fig.colorbar(surf, shrink=0.5, aspect=5)
                axisEqual3D(ax)

                if self.arguments['--preview']:
                    plt.show()
                    _lg.info("Okay, we've shown you your plot, exiting...")
                    sys.exit("Okay, we've shown you your plot, exiting...")
            
                fig.savefig(self.workingfolder+'/moviepar'+str(framecnt).zfill(5)+'.png',dpi=300)
                #fig.savefig('./.pdf',format='pdf')
                fig.clf()
                del ax
                framecnt+=1

            ifile.close()

        if not self.arguments['--killsplash']:
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
                _lg.warning("Couldn't insert the logo at the end, sorry!")


    def action(self):
        """function to stitch the movies together!
        
        :returns: @todo
        """
        _lg.info("Action! Stitching your plots together with ffmpeg...")

        call_ffmpeg(self.workingfolder,outputdir=self.arguments['-o'])
