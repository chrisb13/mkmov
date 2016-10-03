import sys
import os
from netCDF4 import Dataset
import numpy as np
import subprocess
import math
import copy

from mpl_toolkits.axes_grid1 import make_axes_locatable

from ._twodbm import _LogStart
_lg=_LogStart().setup()

from .scf import call_ffmpeg

"""
MkMov: sub-command "2dbm" workhorse file.
"""

def dispay_passed_args_twodbm(arguments,workingfolder):
    """function to print out the passed arguments to the logger

    :workingfolder: @todo
    :returns: @todo
    """
    _lg.info("-----------------------------------------------------------------")
    _lg.info("MkMov has been run with the following options...")

    if arguments['FILE_NAME']!=[]:
        if len(arguments['FILE_NAME'])==1:
            _lg.info("We are making a movie of file: "+ os.path.basename(arguments['FILE_NAME'][0]))
        elif len(arguments['FILE_NAME'])>1:
            _lg.info("We are making a movie of file(s): ")
            for cnt,f in enumerate(arguments['FILE_NAME']):
                _lg.info("File num: "+str(cnt+1)+'. File is: '+ os.path.basename(f))

        _lg.info("Longitude variable we are making a movie of: "+ arguments['X_NAME'])
        _lg.info("Latitude variable we are making a movie of: "+ arguments['Y_NAME'])

        _lg.info("Variable we are making a movie of: "+ arguments['VARIABLE_NAME'])

        _lg.info("Our working directory is: "+ workingfolder)

        _lg.info("")
        _lg.info("Optional settings:")

        if arguments['--proj']:
            _lg.info("You want your movie to have projection : " + arguments['--proj'])

        if arguments['--rotatex']:
            _lg.info("You want to have your globe spinning along the x-axis at speed: " + arguments['--rotatex'])

        if arguments['--xorigin']:
            _lg.info("You want your movie to have xcentre : " + arguments['--xorigin'])

        if arguments['--yorigin']:
            _lg.info("You want your movie to have ycentre : " + arguments['--yorigin'])

        if arguments['-o']:
            _lg.info("You want your movie to live in: " + arguments['-o'])

        _lg.info("-----------------------------------------------------------------")
    return



class MovMakerTwodBM(object):
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
        #super(MovMaker, self).__init__()
        self.filelist,self.variable_name = filelist,variable_name
        self.workingfolder=workingfolder
        self.arguments=argu

    def getdata(self,ifile,preview=False):
        """function that grabs the data
        :returns: nparray
        """
        if not preview:
            if self.var_len==4:
                var_nparray=ifile.variables[self.variable_name][:,self.depthlvl,:,:]
            else:
                var_nparray=ifile.variables[self.variable_name][:]
        else:
            if self.var_len==4:
                var_nparray=ifile.variables[self.variable_name][0,self.depthlvl,:,:]
            else:
                var_nparray=ifile.variables[self.variable_name][0,:]
            # print np.shape(var_nparray)
            var_nparray=np.expand_dims(var_nparray,axis=0)
            # print np.shape(var_nparray)
    
        return var_nparray

    def lights(self,minvar=None,maxvar=None):
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
                _lg.error("Options are: " + str(ifile.variables.keys()) )
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

        #get max and min values for timeseries. This is expensive :(
        if (minvar is None) and (maxvar is None):
            mins=[]
            maxs=[]
            for f in self.filelist:
                ifile=Dataset(f, 'r')
                name_of_array=self.getdata(ifile)

                mins.append(np.min(name_of_array))
                maxs.append(np.max(name_of_array))
                ifile.close()

            self.minvar=np.min(mins)
            self.maxvar=np.max(maxs)

        if minvar or maxvar is not None:
            #user specified the range
            self.minvar=float(minvar)
            self.maxvar=float(maxvar)

        ifile=Dataset(self.filelist[0], 'r') #they should all be the same.
        xvar=ifile.variables[self.arguments['X_NAME']][:]
        yvar=ifile.variables[self.arguments['Y_NAME']][:]
        self.x,self.y=np.meshgrid(xvar,yvar)
        ifile.close()

        # else:
            # ifile=Dataset(self.filelist[0], 'r')
            # name_of_array=np.shape(ifile.variables[self.variable_name])
            # if self.var_len==4:
                # name_of_array=[name_of_array[0]]+[e for e in name_of_array[2:]]

            # self.x,self.y=np.meshgrid(np.arange(name_of_array[self.timedim+2]),\
                    # np.arange(name_of_array[self.timedim+1]))
            # ifile.close()

        return
        
    def camera(self,plotpreview=False):
        """function to create plots.
        
        :workingfolder: @todo
        :returns: @todo
        """
        #this is poor form, violates pep8! but means we can pick a backend for travis-ci testing...
        import matplotlib.pyplot as plt
        from mpl_toolkits.basemap import Basemap

        _lg.info("Camera! Creating your plots...")

        self.framecnt=1

        #might have been leaking memory? 
        plt.close('all')

        # if self.arguments['--cmap'] is not None:
            # opts={'cmap':self.arguments['--cmap']}
        # else:
            # opts={}

        if self.arguments['--xorigin'] and not self.arguments['--yorigin']:
            _lg.info("You want your movie to have xcentre : " + self.arguments['--xorigin'])
            opts={'lon_0':float(self.arguments['--xorigin']),'lat_0':0}

        elif self.arguments['--yorigin'] and not self.arguments['--xorigin']:
            opts={'lon_0':130,'lat_0':float(self.arguments['--yorigin'])}

        elif self.arguments['--xorigin'] and self.arguments['--yorigin']: 
            opts={'lon_0':float(self.arguments['--xorigin']),'lat_0':float(self.arguments['--yorigin'])}
        else:
            opts={'lon_0':130,'lat_0':0}

        for f in self.filelist:
        # for f in self.filelist:
            ifile=Dataset(f, 'r')

            if self.arguments['--rotatex']:
                opts['lon_0']=np.mod(opts['lon_0']+float(self.arguments['--rotatex']),360)
                print opts['lon_0']

            if not plotpreview:
                name_of_array=self.getdata(ifile)
            else:
                name_of_array=self.getdata(ifile,preview=True)

            #h'm the following loop has a problem, because if tstep isn't in dim 0 we are screwed! (probably needs some fancy syntax to slice out of name_of_array (hard without google)
            if self.timedim!=0:
                _lg.error("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")
                sys.exit("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")
            fig=plt.figure()

            for tstep in np.arange(np.shape(name_of_array)[self.timedim]):
                _lg.debug("Working timestep: " + str(self.framecnt)+ " frames in: " +self.workingfolder)
                ax=fig.add_subplot(111)

                if self.arguments['--proj']:
                    proj=self.arguments['--proj']
                else:
                    proj='moll'

                name_of_array_slice=name_of_array[tstep,:].squeeze()

                #for some unknown reason all this slicing kills the mask, so will put it back
                #this is a dodgy hack!
                name_of_array_slice=np.ma.masked_where(\
                       ifile.variables['adt'][0,:].squeeze().mask\
                       ,name_of_array_slice) 


                # create Basemap instance.
                # coastlines not used, so resolution set to None to skip
                # continent processing (this speeds things up a bit)
                m = Basemap(projection=proj,resolution=None,**opts)
                # lons,lats=m(lons,lats)

                # draw line around map projection limb.
                # color background of map projection region.
                # missing values over land will show up this color.
                m.drawmapboundary(fill_color='0.3')

                #x and y give the positions of the grid data if the latlon argument is true
                im1 = m.pcolormesh(self.x,self.y,name_of_array_slice,shading='flat',cmap=plt.cm.jet,latlon=True)

                # im1 = m.pcolormesh(lons,lats,sst,shading='flat',cmap=plt.cm.jet,latlon=False)
                # im1 = m.contourf(lons,lats,sst,30,shading='flat',cmap=plt.cm.jet,latlon=False)

                # draw parallels and meridians, but don't bother labelling them.
                m.drawparallels(np.arange(-90.,99.,30.))
                m.drawmeridians(np.arange(-180.,180.,60.))
                # add colorbar
                cb = m.colorbar(im1,"bottom", size="5%", pad="2%")

                # add a title.
                ax.set_title('Variable is: '+self.variable_name+'. Frame num is: ' +str(self.framecnt)+'. Projection: ' + proj)

                # Create divider for existing axes instance
                # divider = make_axes_locatable(ax)
                # caxis = divider.append_axes("bottom", size="5%", pad=0.25)
                
                cb = m.colorbar(im1,"bottom", size="5%", pad="2%")

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

            ifile.close()

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
