import sys
import os
from netCDF4 import Dataset
import numpy as np

# sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from ._twod import _LogStart
_lg=_LogStart().setup()

import scf

"""
MkMov: sub-command "2d" workhorse file.
"""

def cmap_center_point_adjust(cmap, range, center):
    '''
    converts center to a ratio between 0 and 1 of the
    range given and calls cmap_center_adjust(). returns
    a new adjusted colormap accordingly

    NB: nicked from https://sites.google.com/site/theodoregoetz/notes/matplotlib_colormapadjust
    '''
    def cmap_center_adjust(cmap, center_ratio):
        '''
        returns a new colormap based on the one given
        but adjusted so that the old center point higher
        (>0.5) or lower (<0.5)
        '''
        if not (0. < center_ratio) & (center_ratio < 1.):
            return cmap
        a = math.log(center_ratio) / math.log(0.5)
        return cmap_powerlaw_adjust(cmap, a)

    def cmap_powerlaw_adjust(cmap, a):
        '''
        returns a new colormap based on the one given
        but adjusted via power-law:

        newcmap = oldcmap**a
        '''
        if a < 0.:
            return cmap
        cdict = copy.copy(cmap._segmentdata)
        fn = lambda x : (x[0]**a, x[1], x[2])
        for key in ('red','green','blue'):
            cdict[key] = map(fn, cdict[key])
            cdict[key].sort()
            assert (cdict[key][0]<0 or cdict[key][-1]>1), \
                "Resulting indices extend out of the [0, 1] segment."
        return colors.LinearSegmentedColormap('colormap',cdict,1024)

    if not ((range[0] < center) and (center < range[1])):
        return cmap
    return cmap_center_adjust(cmap,
        abs(center - range[0]) / abs(range[1] - range[0]))

def dispay_passed_args(arguments,workingfolder):
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

        _lg.info("Variable we are making a movie of: "+ arguments['VARIABLE_NAME'])

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

        if arguments['--preview']:
            _lg.info("You have opted to preview your plot before making a movie.")

        if arguments['--bias']:
            _lg.info("You want to create a movie of the bias from the mean (requires NCO tools...)")

            try:
                FNULL = open(os.devnull, 'w')
                subprocess.call(["ncra", "--version"],stdout=FNULL, stderr=subprocess.STDOUT)
            except OSError as e:
                _lg.error("You don't have NCO installed!")
                sys.exit("You don't have NCO installed!")

        if arguments['--bcmapcentre']:
            _lg.info("You want your bias plot to be centred around zero. (requires --cmap)")
            if not arguments['--bias']:
                _lg.error("This option is only for a bias plot")
                sys.exit("This option is only for a bias plot")

            if not arguments['--cmap']:
                _lg.error("This option can only be used when you have specified a cmap (diverging colormap recommended)")
                sys.exit("This option can only be used when you have specified a cmap (diverging colormap recommended)")

        if arguments['-o']:
            _lg.info("You want your movie to live in: " + arguments['-o'])

        if arguments['--lmask']:
            _lg.info("You want to mask out the following values: " + arguments['--lmask'])

        if arguments['--lmask2']:
            _lg.info("You want to mask out a second set of land values, this is unusual! Your second value is: " + arguments['--lmask2'])
            if not arguments['--lmask']:
                _lg.error("This option can only be used when you have specified a lmask")
                sys.exit("This option can only be used when you have specified a lmask")

        if arguments['--lmaskfld']:
            _lg.info("You want to fill in the land mask you specified in lmask.")

            if not arguments['--lmask']:
                _lg.error("This option can only be used when you have specified a lmask")
                sys.exit("This option can only be used when you have specified a lmask")

        if arguments['--fps']:
            _lg.info("You have said your final movie will be: " + \
                    str(int(arguments['--fps']))+"  frames per second.")

        if arguments['--cmap']:
            _lg.info("You have said you would like to contourf with the following matplotlib colour map: " + \
                    arguments['--cmap'])

        if arguments['--clev']:
            _lg.info("You have said you would like to contourf with the following number of levels: " + \
                    str(int(arguments['--clev'])))

        if arguments['--4dvar']:
            _lg.info("You have passed a 4 dimensional variable (time,depth,spatialdim1,spatialdim2) and would like to plot DEPTHLVL: " + \
                    str(int(arguments['--4dvar'])))

        if (arguments['--figwth'] is not None) and (arguments['--fighgt'] is not None):
            _lg.info("You have specified figure dimensions of: "+arguments['--figwth']+', '+arguments['--fighgt'] + ' (width,height).')

        if (arguments['--x'] is not None) and (arguments['--y'] is not None):
            _lg.info("You have specified a x and yvariable: "+arguments['--x']+', '+arguments['--y'] )

        #error check to make sure both x and y variables were passed
        if (arguments['--x'] is not None) and (arguments['--y'] is None):
            _lg.error("You passed xvariable but not a yvariable")
            sys.exit("You passed xvariable but not a yvariable")
        elif(arguments['--x'] is None) and (arguments['--y'] is not None): 
            _lg.error("You passed yvariable but not a xvariable")
            sys.exit("You passed yvariable but not a xvariable")

        if arguments['--killsplash']:
            _lg.info("You have asked for the MkMov splash screen to NOT be displayed at the end of your movie.")

        #error check to make sure both figwith and fighgt were passed
        if (arguments['--figwth'] is not None) and (arguments['--fighgt'] is None):
            _lg.error("You passed figwth but not fighgt")
            sys.exit("You passed figwth but not fighgt")
        elif(arguments['--figwth'] is None) and (arguments['--fighgt'] is not None): 
            _lg.error("You passed fighgt but not figwth")
            sys.exit("You passed fighgt but not figwth")

        _lg.info("-----------------------------------------------------------------")
    elif arguments['FILE_NAMES']!=[]:
        _lg.info("We are making a movie from your passed list of png files.")
        _lg.info("Our working directory is: "+ workingfolder)
        _lg.info("")
        _lg.info("Optional settings:")

        if arguments['-o']:
            _lg.info("You have specified you want your movie to live in: " + arguments['-o'])

        if arguments['--fps']:
            _lg.info("You have said your final movie will be: " + \
                    str(int(arguments['--fps']))+"  frames per second.")

        _lg.info("-----------------------------------------------------------------")
    return


class MovMaker(object):
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

    def lights(self):
        """function to do some sanity checks on the files and find out where the time dim is.
        
        """
        _lg.info("Lights! Looking at your netCDF files...")
        var_timedims=[]

        #create bias files
        if self.arguments['--bias']:
            #following example in http://linux.die.net/man/1/ncdiff
            ncout='ncra '+' '.join(self.filelist)+' '+workingfol+'mean.nc'
            _lg.info("Creating mean file: " + ncout)
            subprocess.call(ncout,shell=True)

            ncout='ncwa -O -a '+self.arguments['--bias']+' '+workingfol+'mean.nc '+workingfol+'mean_notime.nc'
            _lg.info("Removing time dimension from mean file: " + ncout)
            subprocess.call(ncout,shell=True)

            difffol=workingfol+'difffiles/'
            mkdir(workingfol+'difffiles/')
            newfilelist=[]
            cnt=0
            for f in self.filelist:
                ncout='ncdiff '+' '+f+' '+workingfol+'mean_notime.nc '+difffol+os.path.basename(f)[:-3]+'_diff_'+str(cnt).zfill(5)+'.nc'
                _lg.info("Creating anomaly file: " + ncout)
                subprocess.call(ncout,shell=True)
                newfilelist.append(difffol+os.path.basename(f)[:-3]+'_diff_'+str(cnt).zfill(5)+'.nc')
                cnt+=1

            self.filelist=newfilelist
                
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
        
    def camera(self,minvar=None,maxvar=None,plotpreview=False):
        """function to create plots.
        
        :workingfolder: @todo
        :returns: @todo
        """
        #this is poor form, violates pep8! but means we can pick a backend for travis-ci testing...
        import matplotlib.pyplot as plt

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
        for f in self.filelist:
            ifile=Dataset(f, 'r')
            name_of_array=getdata()

            plt.close('all')

            if (self.arguments['--figwth'] is not None) and (self.arguments['--fighgt'] is not None):
                #width then height
                fig=plt.figure(figsize=(float(self.arguments['--figwth']),float(self.arguments['--fighgt'])))
            else:
                fig=plt.figure()

            #not ideal really, this thing being in the loop
            if (self.arguments['--x'] is not None) and (self.arguments['--y'] is not None):
                ifile=Dataset(f, 'r')
                xvar=ifile.variables[self.arguments['--x']][:]
                yvar=ifile.variables[self.arguments['--y']][:]
                x,y=np.meshgrid(xvar,yvar)
            else:
                x,y=np.meshgrid(np.arange(np.shape(name_of_array)[self.timedim+2]),\
                        np.arange(np.shape(name_of_array)[self.timedim+1]))

            minvar=np.min(name_of_array)
            maxvar=np.max(name_of_array)

            #h'm the following loop has a problem, because if tstep isn't in dim 0 we are screwed! (probably needs some fancy syntax to slice out of name_of_array (hard without google)
            if self.timedim!=0:
                _lg.error("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")
                sys.exit("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")

            for tstep in np.arange(np.shape(name_of_array)[self.timedim]):
                _lg.debug("Working timestep: " + str(framecnt)+ " frames in: " +self.workingfolder)

                ax=fig.add_subplot(111)

                ax.set_title(self.variable_name+' frame num is: ' +str(framecnt))
                #ax.set_xlabel('msg')
                #ax.set_ylabel('msg')

                if self.arguments['--lmask']:
                    name_of_array= np.ma.masked_where(
                        name_of_array==float(self.arguments['--lmask']),
                        name_of_array) 

                    #weird case where we have two landmasks... (i.e. MOM5_010)
                    if self.arguments['--lmask2']:
                        name_of_array= np.ma.masked_where(
                            name_of_array==float(self.arguments['--lmask2']),
                            name_of_array) 

                    if not self.arguments['--lmaskfld']:
                        #land mask...
                        cs2=ax.contour(x,y,name_of_array[tstep,:,:].mask,levels=[-1,0],linewidths=1,colors='black')
                    else:
                        cs2=ax.contourf(x,y,name_of_array[tstep,:,:].mask,levels=[-1,0,1],colors=('#B2D1FF','#858588'),alpha=.9) #landmask


                if self.arguments['--clev']:
                    cnt_levelnum=int(self.arguments['--clev'])
                else:
                    cnt_levelnum=50

                if not self.arguments['--cmap']:
                    cs1=plt.contourf(x,y,name_of_array[tstep,:,:],\
                            levels=np.linspace(self.minvar,self.maxvar,cnt_levelnum))
                else:

                    if self.arguments['--bcmapcentre']:
                        #will plot colourmap centred around zero
                        oldcmap=matplotlib.cm.get_cmap(self.arguments['--cmap'])
                        shiftd=cmap_center_point_adjust(oldcmap,[self.minvar,self.maxvar],0)
                        cs1=plt.contourf(x,y,name_of_array[tstep,:,:],\
                                levels=np.linspace(self.minvar,self.maxvar,cnt_levelnum),\
                                cmap=shiftd)
                    else:
                        cs1=plt.contourf(x,y,name_of_array[tstep,:,:],\
                                levels=np.linspace(self.minvar,self.maxvar,cnt_levelnum),\
                                cmap=self.arguments['--cmap'])


                plt.colorbar(cs1)
                #plt.show()

                if plotpreview:
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

        scf.call_ffmpeg(self.workingfolder,fps_pass=self.arguments['--fps'],outputdir=self.arguments['-o'])


    def cleanup(self):
        """function to clean up the mess we have made
        
        :returns: @todo
        """
        _lg.info("Post-processing. Cleaning up the mess we've made...")

        #remove working folder
        if arguments['-o']:
            if os.path.exists(workingfol):
                #remove temp files from bias movie making
                if arguments['--bias']:
                    tempfiles=\
                    sorted(glob.glob(workingfol+'*.nc'))+\
                    sorted(glob.glob(workingfol+'difffiles/*.nc'))
                    for f in tempfiles:
                        os.remove(f)
                    os.rmdir(workingfol+'difffiles/')

                if not os.listdir(workingfol):
                    os.rmdir(workingfol)
                    _lg.info("Working folder: " + workingfol +" removed.")
                else:
                    _lg.warning("Working directory: " + workingfol+" not empty, please remove manually")