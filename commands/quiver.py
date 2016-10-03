import sys
import os
from netCDF4 import Dataset
import numpy as np
import subprocess
import math
import copy

from mpl_toolkits.axes_grid1 import make_axes_locatable

from ._quiver import _LogStart
_lg=_LogStart().setup()

from .scf import call_ffmpeg

"""
MkMov: sub-command "quiver" workhorse file.
"""

def interpolate_uv(uvelocity,vvelocity):
    """function to interpolate U/V points onto T-points
    
    I'm sure this could be more efficient!

    :uvelocity: one level NEMO array uvelocity on U-point
    :vvelocity: one level NEMO array vvelocity on V-point
    :returns: u/v at t point
    """
    u=np.zeros_like(uvelocity)
    v=np.zeros_like(vvelocity)

    jlen=np.arange(np.shape(uvelocity)[0])
    ilen=np.arange(np.shape(uvelocity)[1])

    for jj in jlen:
        for ii in ilen:

            #square and interpolate
            ua =0.5*(uvelocity[jj,ii] + uvelocity[jj-1,ii])  # U^2 from U-point to T-point
            va = 0.5*(vvelocity[jj,ii] + vvelocity[jj,ii-1]) # V^2 from V-point to T-point

            u[jj,ii] = ua
            v[jj,ii] = va


    return u,v


def dispay_passed_args_quiver(arguments,workingfolder):
    """function to print out the passed arguments to the logger

    :workingfolder: @todo
    :returns: @todo
    """
    _lg.info("-----------------------------------------------------------------")
    _lg.info("MkMov has been run with the following options...")

    if len(arguments['FILE_NAME'])==1:

        _lg.error("You need to pass at least two files.")
        sys.exit("You need to pass at least two files.")

    # elif len(arguments['FILE_NAME'])>1:
        # _lg.info("We are making a movie of file(s): ")
        # for cnt,f in enumerate(arguments['FILE_NAME']):
            # _lg.info("File num: "+str(cnt+1)+'. File is: '+ os.path.basename(f))

    _lg.info("Variable we are making a quiver movie of: "+ arguments['VAR_X'] + " and "+arguments['VAR_Y'] )

    _lg.info("Our working directory is: "+ workingfolder)

    _lg.info("")
    _lg.info("Optional settings:")

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

    if arguments['--tfilevar'] is not None:
        if arguments['--tfile'] is None:
            _lg.error("You must specify tfile")
            sys.exit("You must specify tfile")

    if arguments['--tfile']:
        _lg.info("You have said you would like to plot a landmask from the following T-file (NEMO only):" + \
                arguments['--tfile'])

        if arguments['--tfilevar'] is None:
            _lg.error("You must specify tfilevar")
            sys.exit("You must specify tfilevar")

        _lg.info("The landmask will be plotted from variable: " + arguments['--tfilevar'])

    if arguments['--cmap']:
        _lg.info("You have said you would like to contourf with the following matplotlib colour map: " + \
                arguments['--cmap'])

    if arguments['--4dvar']:
        _lg.info("You have passed a 4 dimensional variable (time,depth,spatialdim1,spatialdim2) and would like to plot DEPTHLVL: " + \
                str(int(arguments['--4dvar'])))

    if arguments['--lmask']:
        _lg.info("You want to mask out the following values: " + arguments['--lmask'])


    if arguments['--preview']:
        _lg.info("You have opted to preview your plot before making a movie.")

    if (arguments['--x2d'] is not None) and (arguments['--y2d'] is not None):
        _lg.info("You have specified a x and yvariable for an unstructured grid: "+arguments['--x2d']+', '+arguments['--y2d'] )

    #error check to make sure both x and y variables were passed
    if (arguments['--x2d'] is not None) and (arguments['--y2d'] is None):
        _lg.error("You passed xvariable but not a yvariable")
        sys.exit("You passed xvariable but not a yvariable")

    elif(arguments['--x2d'] is None) and (arguments['--y2d'] is not None): 
        _lg.error("You passed yvariable but not a xvariable")
        sys.exit("You passed yvariable but not a xvariable")

    if arguments['--fixdateline']:
        _lg.info("You want to fill in the land mask you specified in lmask.")

        if (arguments['--x2d'] is None) and (arguments['--y2d'] is None):
            _lg.error("This option can only be used when you have specified a --x2d and --y2d")
            sys.exit("This option can only be used when you have specified a --x2d and --y2d")

    if np.mod(len(arguments['FILE_NAME']),2)!=0:
        _lg.error("please pass an even number of files (half U and half V).")
        sys.exit("please pass an even number of files (half U and half V).")

    _lg.info("-----------------------------------------------------------------")
    return


def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    # print(l,n)
    for i in np.arange(0, len(l), n):
        i=int(i)
        n=int(n)
        yield l[i:i + n]

class MovMakerQuiver(object):
    """
    Class to create movie based on file list and variable name.

    Parameters
    ----------
    :filelist:
    :variable_x: 
    :variable_y: 
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

    def __init__(self, filelist,variable_x,variable_y,workingfolder,argu):
        self.filelist,self.variable_x,self.variable_y = filelist,variable_x,variable_y
        self.workingfolder=workingfolder
        self.arguments=argu

    def getdata(self,ifile,varname,preview=False):
        """function that grabs the data
        :returns: nparray
        """
        if not preview:
            if self.var_len==4:
                var_nparray=ifile.variables[varname][:,self.depthlvl,:,:]
            else:
                var_nparray=ifile.variables[varname][:]
        else:
            if self.var_len==4:
                var_nparray=ifile.variables[varname][0,self.depthlvl,:,:]
            else:
                var_nparray=ifile.variables[varname][0,:]
            var_nparray=np.expand_dims(var_nparray,axis=0)
    
        return var_nparray

    def lights(self):
        """function to do some sanity checks on the files and find out where the time dim is.
        
        """
        _lg.info("Lights! Looking at your netCDF files...")
        var_timedims=[]
                
        #error checks files, are all similar

        fchunked=chunks(self.filelist,len(self.filelist)/2)
        self.xfiles=next(fchunked)
        self.yfiles=next(fchunked)

        for xf,yf in zip(self.xfiles,self.yfiles):
            if not os.path.exists(xf):
                _lg.error("Input file: " + str(os.path.basename(xf))  + " does not exist.")
                sys.exit("Input file: " + str(os.path.basename(xf))  + " does not exist.")

            if not os.path.exists(yf):
                _lg.error("Input file: " + str(os.path.basename(yf))  + " does not exist.")
                sys.exit("Input file: " + str(os.path.basename(yf))  + " does not exist.")

            ifilex=Dataset(xf, 'r')
            ifiley=Dataset(yf, 'r')

            if self.variable_x not in ifilex.variables.keys():
                _lg.error("Variable: " + str(self.variable_x) + " does not exist in netcdf4 file.")
                _lg.error("Options are: " + str(ifilex.variables.keys()) )
                sys.exit("Variable: " + str(self.variable_x) + " does not exist in netcdf4 file.")

            if self.variable_y not in ifiley.variables.keys():
                _lg.error("Variable: " + str(self.variable_y) + " does not exist in netcdf4 file.")
                _lg.error("Options are: " + str(ifiley.variables.keys()) )

                sys.exit("Variable: " + str(self.variable_y) + " does not exist in netcdf4 file.")

            ifiley.close()

            #######################################################
            #  assume that the rest of the files are the same...  #
            #######################################################
            
            #what shape is the passed variable? Do some error checks
            self.var_len=len(ifilex.variables[self.variable_x].shape)
            #the 'obvious' case; one file with one time dim and two spatial dims
            if self.var_len==3: 
                pass

            #tricky, which dims are time/random_dim/spatial1/spatial2?
            if self.var_len==4:
                if self.arguments['--4dvar']:
                    _lg.debug("Variable: " + str(self.variable_x) + " has four dimensions. Following your argument, we will plot depth level: "+self.arguments['--4dvar'] )
                    self.depthlvl=int(self.arguments['--4dvar'])
                else:
                    _lg.warning("Variable: " + str(self.variable_x) + " has four dimensions. MkMov will assume the second dim is depth/height and plot the first level.")
                    self.depthlvl=0

            ifile_dim_keys=list(dict(ifilex.dimensions).keys())

            #find unlimited dimension
            findunlim=[ifilex.dimensions[dim].isunlimited() for dim in ifile_dim_keys]

            dim_unlim_num=[i for i, x in enumerate(findunlim) if x]
            if len(dim_unlim_num)==0:
                _lg.warning("Input file: " + str(os.path.basename(xf))  + " has no unlimited dimension, which dim is time?")
            elif len(dim_unlim_num)>1:
                _lg.warning("Input file: " + str(os.path.basename(xf))  + " has more than one unlimited dimension.")
            else:
                timename=ifile_dim_keys[dim_unlim_num[0]]
                var_timedim=[i for i, x in enumerate(ifilex.variables[self.variable_x].dimensions) if x==timename][0]
                var_timedims.append(var_timedim)
                ifilex.close()
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
                var_timedim=[i for i, x in enumerate(ifilex.variables[self.variable_x].dimensions) if x==timename][0]
                var_timedims.append(var_timedim)

            ifilex.close()

        #check all time dimensions are in the same place across all files..
        if var_timedims[1:]==var_timedims[:-1]:
            self.timedim=var_timedims[0]
        else:
            _lg.error("(Unlimited) 'time' dimension was not the same across all files, fatal error.")
            sys.exit("(Unlimited) 'time' dimension was not the same across all files, fatal error.")
        return
        
    def camera(self,plotpreview=False):
        """function to create plots.
        
        :workingfolder: @todo
        :returns: @todo
        """
        #this is poor form, violates pep8! but means we can pick a backend for travis-ci testing...
        import matplotlib.pyplot as plt

        _lg.info("Camera! Creating your plots...")

        self.framecnt=1

        #might have been leaking memory? 
        plt.close('all')

        if self.arguments['--cmap'] is not None:
            opts={'cmap':self.arguments['--cmap']}
        else:
            opts={}

        for xf,yf in zip(self.xfiles,self.yfiles):
        # for f in self.filelist:
            ifilex=Dataset(xf, 'r')
            ifiley=Dataset(yf, 'r')

            if not plotpreview:
                name_of_arrayx=self.getdata(ifilex,self.variable_x)
                name_of_arrayy=self.getdata(ifiley,self.variable_y)
            else:
                name_of_arrayx=self.getdata(ifilex,self.variable_x,preview=True)
                name_of_arrayy=self.getdata(ifiley,self.variable_y,preview=True)

            #h'm the following loop has a problem, because if tstep isn't in dim 0 we are screwed! (probably needs some fancy syntax to slice out of name_of_array (hard without google)
            if self.timedim!=0:
                _lg.error("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")
                sys.exit("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")
            fig=plt.figure()

            #bit dodgy really, should really use a t-file for NEMO
            if (self.arguments['--x2d'] is not None) and (self.arguments['--y2d'] is not None):
                ifile=Dataset(xf, 'r') #they should all be the same.
                x=ifile.variables[self.arguments['--x2d']][:]

                if self.arguments['--fixdateline']:
                    #fix the dateline
                    for index in np.arange(np.shape(x)[0]):
                        if len(np.where(np.sign(x[index,:])==-1)[0])==0:
                            _lg.warning("MkMov couldn't find your dateline, skipping the 'fix'.")
                            break

                        start=np.where(np.sign(x[index,:])==-1)[0][0]
                        x[index,start:]=x[index,start:]+360

                y=ifile.variables[self.arguments['--y2d']][:]
                ifile.close()
            else:
                x,y=np.meshgrid(np.arange(np.shape(name_of_arrayx[0])[1]),np.arange(np.shape(name_of_arrayx[0])[0]))

            if self.arguments['--tfile'] is not None:
                ifile=Dataset(self.arguments['--tfile'], 'r')
                lmask=ifile.variables[self.arguments['--tfilevar']][0,:] #assumes a 3d file
                lmask=np.ma.masked_where(lmask==0,lmask) 

            #assumes the x/y files have the same number of timesteps
            for tstep in np.arange(np.shape(name_of_arrayx)[self.timedim]):
                _lg.debug("Working timestep: " + str(self.framecnt)+ " frames in: " +self.workingfolder)
                ax=fig.add_subplot(111)

                name_of_arrayx_slice=name_of_arrayx[tstep,:]
                name_of_arrayy_slice=name_of_arrayy[tstep,:]

                #For NEMO interpolate U/V points onto T-point
                arrayx,arrayy=interpolate_uv(name_of_arrayx_slice,name_of_arrayy_slice)

                if self.arguments['--lmask']:
                    #mask out land points for nemo
                    arrayx=np.ma.masked_where(arrayx==0,arrayx) 
                    arrayy=np.ma.masked_where(arrayy==0,arrayy) 

                    #can look a bit funky b/c we're now on t-points..
                    # ax.contour(x,y,arrayx.mask,levels=[-1,0],linewidths=1,colors='black')

                if self.arguments['--tfile']:
                    cs2=ax.contourf(x,y,lmask.mask,levels=[-1,0,1],colors=('#B2D1FF','#858588'),alpha=.9) #landmask

                if self.arguments['--vorticity']:
                    # dv/dx - du/dy (hopefully!)
                    name_of_array=\
                    np.gradient(arrayy)[1]-np.gradient(arrayx)[0]
                    if (self.arguments['--min'] is not None) and (self.arguments['--max'] is not None):
                        cs1=plt.contourf(x,y,name_of_array,30,\
                                levels=np.linspace(\
                                float(self.arguments['--min']),\
                                float(self.arguments['--max']),30),extend='both',**opts)
                    else:
                        cs1=plt.contourf(x,y,name_of_array,30,levels=np.linspace(-.5,.5,30),extend='both',**opts)


                    ax.set_title("Plotting vorticity: "+self.variable_x+' and  '+self.variable_y+'. Frame num is: ' +str(self.framecnt))
                else:
                    # http://matplotlib.org/api/pyplot_api.html#matplotlib.pyplot.quiver
                    skip=(slice(None,None,5),slice(None,None,5))
                    mag=np.sqrt(np.square(arrayx)+np.square(arrayy))
                    if (self.arguments['--min'] is not None) and (self.arguments['--max'] is not None):
                        cs1=ax.contourf(x,y,mag,\
                                levels=np.linspace(\
                                float(self.arguments['--min']),\
                                float(self.arguments['--max']),30),extend='both',**opts)
                    else:
                        cs1=ax.contourf(x,y,mag,levels=np.linspace(0,1,30),extend='both',**opts)

                    #if we want to normalise...
                    # arrayx=arrayx/mag
                    # arrayy=arrayy/mag
                    # plt.quiver(x[skip], y[skip], arrayx[skip], arrayy[skip], pivot='mid',color='black', units='xy',headwidth=1,  headlength=4,angles='xy',scale=1)

                    ax.quiver(x[skip], y[skip], arrayx[skip], arrayy[skip], pivot='mid',color='black', units='xy',headwidth=1,  headlength=4,angles='xy',scale_units='xy')

                    ax.set_title("Plotting: "+self.variable_x+' and  '+self.variable_y+'. Frame num is: ' +str(self.framecnt))


                # Create divider for existing axes instance
                divider = make_axes_locatable(ax)
                caxis = divider.append_axes("bottom", size="5%", pad=0.25)
                
                plt.colorbar(cs1,cax=caxis,orientation='horizontal')

                if plotpreview:
                    plt.show()
                    _lg.info("Okay, we've shown you your plot, exiting...")
                    if self.arguments['-o']:
                        subprocess.call('rm -r '+self.workingfolder,shell=True)
                    sys.exit(0)
            
                fig.savefig(self.workingfolder+'/moviepar'+str(self.framecnt).zfill(5)+'.png',dpi=300)
                fig.clf()
                del ax
                self.framecnt+=1

            ifilex.close()
            ifiley.close()

    def action(self):
        """function to stitch the movies together!
        
        :returns: @todo
        """
        _lg.info("Action! Stitching your plots together with ffmpeg...")

        call_ffmpeg(self.workingfolder,outputdir=self.arguments['-o'])

    def cleanup(self):
        """function to clean up the mess we have made
        
        :returns: @todo
        """
        _lg.info("Post-processing. Cleaning up the mess we've made...")

        #remove working folder
        if arguments['-o']:
            if os.path.exists(workingfol):
                if not os.listdir(workingfol):
                    os.rmdir(workingfol)
                    _lg.info("Working folder: " + workingfol +" removed.")
                else:
                    _lg.warning("Working directory: " + workingfol+" not empty, please remove manually")




