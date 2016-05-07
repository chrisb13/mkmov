import numpy as np
from netCDF4 import Dataset
import os
import sys

from ._threedcube import _LogStart
_lg=_LogStart().setup()

import scf

"""
MkMov: sub-command "3dcube" workhorse file.
"""


def dispay_passed_args_threedcube(arguments,workingfolder):
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

    # #for optional parameters...
    # if (arguments['--min'] is not None) and (arguments['--max'] is not None):
        # _lg.info("You have specified a min/max range of: "+arguments['--min']+', '+arguments['--max'] )

    # #error check to make sure both min and max were passed
    # if (arguments['--min'] is not None) and (arguments['--max'] is None):
        # _lg.error("You passed min but not max")
        # sys.exit("You passed min but not max")
    # elif(arguments['--min'] is None) and (arguments['--max'] is not None): 
        # _lg.error("You passed max but not min")
        # sys.exit("You passed max but not min")

    if arguments['--preview']:
        _lg.info("You have opted to preview your plot before making a movie.")

    # if arguments['--bias']:
        # _lg.info("You want to create a movie of the bias from the mean (requires NCO tools...)")

        # try:
            # FNULL = open(os.devnull, 'w')
            # subprocess.call(["ncra", "--version"],stdout=FNULL, stderr=subprocess.STDOUT)
        # except OSError as e:
            # _lg.error("You don't have NCO installed!")
            # sys.exit("You don't have NCO installed!")

    # if arguments['--bcmapcentre']:
        # _lg.info("You want your bias plot to be centred around zero. (requires --cmap)")
        # if not arguments['--bias']:
            # _lg.error("This option is only for a bias plot")
            # sys.exit("This option is only for a bias plot")

        # if not arguments['--cmap']:
            # _lg.error("This option can only be used when you have specified a cmap (diverging colormap recommended)")
            # sys.exit("This option can only be used when you have specified a cmap (diverging colormap recommended)")

    # if arguments['-o']:
        # _lg.info("You want your movie to live in: " + arguments['-o'])

    # if arguments['--lmask']:
        # _lg.info("You want to mask out the following values: " + arguments['--lmask'])

    # if arguments['--lmask2']:
        # _lg.info("You want to mask out a second set of land values, this is unusual! Your second value is: " + arguments['--lmask2'])
        # if not arguments['--lmask']:
            # _lg.error("This option can only be used when you have specified a lmask")
            # sys.exit("This option can only be used when you have specified a lmask")

    # if arguments['--lmaskfld']:
        # _lg.info("You want to fill in the land mask you specified in lmask.")

        # if not arguments['--lmask']:
            # _lg.error("This option can only be used when you have specified a lmask")
            # sys.exit("This option can only be used when you have specified a lmask")

    # if arguments['--fps']:
        # _lg.info("You have said your final movie will be: " + \
                # str(int(arguments['--fps']))+"  frames per second.")

    # if arguments['--cmap']:
        # _lg.info("You have said you would like to contourf with the following matplotlib colour map: " + \
                # arguments['--cmap'])

    # if arguments['--clev']:
        # _lg.info("You have said you would like to contourf with the following number of levels: " + \
                # str(int(arguments['--clev'])))

    # if arguments['--4dvar']:
        # _lg.info("You have passed a 4 dimensional variable (time,depth,spatialdim1,spatialdim2) and would like to plot DEPTHLVL: " + \
                # str(int(arguments['--4dvar'])))

    # if (arguments['--figwth'] is not None) and (arguments['--fighgt'] is not None):
        # _lg.info("You have specified figure dimensions of: "+arguments['--figwth']+', '+arguments['--fighgt'] + ' (width,height).')

    # if (arguments['--x'] is not None) and (arguments['--y'] is not None):
        # _lg.info("You have specified a x and yvariable: "+arguments['--x']+', '+arguments['--y'] )

    # #error check to make sure both x and y variables were passed
    # if (arguments['--x'] is not None) and (arguments['--y'] is None):
        # _lg.error("You passed xvariable but not a yvariable")
        # sys.exit("You passed xvariable but not a yvariable")
    # elif(arguments['--x'] is None) and (arguments['--y'] is not None): 
        # _lg.error("You passed yvariable but not a xvariable")
        # sys.exit("You passed yvariable but not a xvariable")

    # if arguments['--killsplash']:
        # _lg.info("You have asked for the MkMov splash screen to NOT be displayed at the end of your movie.")

    # #error check to make sure both figwith and fighgt were passed
    # if (arguments['--figwth'] is not None) and (arguments['--fighgt'] is None):
        # _lg.error("You passed figwth but not fighgt")
        # sys.exit("You passed figwth but not fighgt")
    # elif(arguments['--figwth'] is None) and (arguments['--fighgt'] is not None): 
        # _lg.error("You passed fighgt but not figwth")
        # sys.exit("You passed fighgt but not figwth")

    _lg.info("-----------------------------------------------------------------")
    return



class MovMakerThreeDCube(object):
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
        from matplotlib import cm
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D

        def getdata():
            """function that grabs the data
            :returns: nparray
            """
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

            # if (self.arguments['--figwth'] is not None) and (self.arguments['--fighgt'] is not None):
                # #width then height
                # fig=plt.figure(figsize=(float(self.arguments['--figwth']),float(self.arguments['--fighgt'])))
            # else:
                # fig=plt.figure()
            fig=plt.figure()

            # minvar=np.min(name_of_array)
            # maxvar=np.max(name_of_array)
            levs=np.linspace(np.min(self.minvar),np.max(self.maxvar),30)

            #h'm the following loop has a problem, because if tstep isn't in dim 0 we are screwed! (probably needs some fancy syntax to slice out of name_of_array (hard without google)
            if self.timedim!=0:
                _lg.error("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")
                sys.exit("Your time dimension wasn't in the first dimension, MkMov doesn't know what to do with this kind of file.")

            for tstep in np.arange(np.shape(name_of_array)[self.timedim]):
                _lg.debug("Working timestep: " + str(framecnt)+ " frames in: " +self.workingfolder)

                # ax=fig.add_subplot(111)
                ax = fig.gca(projection='3d')

                ax.set_title(self.variable_name+' frame num is: ' +str(framecnt))

                #surface plot
                Z=name_of_array[tstep,0,:,:]

                X = np.linspace(-5, 5, np.shape(name_of_array)[self.timedim+2])
                Y = np.linspace(-5, 5, np.shape(name_of_array)[self.timedim+3])
                X, Y = np.meshgrid(Y, X)

                cset = [[],[],[]]

                cset[0] = ax.contourf(X, Y, Z, offset=5,zdir='z',
                                levels=levs,cmap=plt.cm.jet)

                #side far away
                # #t,z,y,x
                # #5,75,289,431
                # Z=name_of_array[tstep,::-1,:,5]
                # X = np.linspace(-5, 5, np.shape(name_of_array)[self.timedim+1])
                # Y = np.linspace(-5, 5, np.shape(name_of_array)[self.timedim+2])
                # X, Y = np.meshgrid(X, Y)

                # cset[0] = ax.contourf(Z.T, Y, X, offset=-5,zdir='x',
                                # levels=levs,cmap=plt.cm.jet)


                # #side close-by
                Z=name_of_array[tstep,::-1,:,-5]
                X = np.linspace(2, 5, np.shape(name_of_array)[self.timedim+1])
                Y = np.linspace(-5, 5, np.shape(name_of_array)[self.timedim+2])
                X, Y = np.meshgrid(X, Y)

                cset[1] = ax.contourf(Z.T, Y, X, offset=5,zdir='x',
                                levels=levs,cmap=plt.cm.jet)


                # front side
                Z=name_of_array[tstep,::-1,2,:]

                X = np.linspace(-5, 5, np.shape(name_of_array)[self.timedim+3])
                Y = np.linspace(2, 5, np.shape(name_of_array)[self.timedim+1])

                X,Y=np.meshgrid(X, Y)

                cset[2] = ax.contourf(X, Z, Y, offset=-5,zdir='y',
                                levels=levs,cmap=plt.cm.jet)

                ## setting 3D-axis-limits:    
                ax.set_xlim3d(-5,5)
                ax.set_ylim3d(-5,5)
                ax.set_zlim3d(2,5)
                #for one plot...
                #eg
                #cs1=ax.contourf(field,levels=np.linspace(-1,1,50))
                #plt.colorbar(cs1,orientation='vertical')
                plt.colorbar(cset[0],orientation='vertical')

                #########################
                #  options from 2d....  #
                #########################

                # if self.arguments['--lmask']:
                    # name_of_array= np.ma.masked_where(
                        # name_of_array==float(self.arguments['--lmask']),
                        # name_of_array) 

                    # #weird case where we have two landmasks... (i.e. MOM5_010)
                    # if self.arguments['--lmask2']:
                        # name_of_array= np.ma.masked_where(
                            # name_of_array==float(self.arguments['--lmask2']),
                            # name_of_array) 

                    # if not self.arguments['--lmaskfld']:
                        # #land mask...
                        # cs2=ax.contour(x,y,name_of_array[tstep,:,:].mask,levels=[-1,0],linewidths=1,colors='black')
                    # else:
                        # cs2=ax.contourf(x,y,name_of_array[tstep,:,:].mask,levels=[-1,0,1],colors=('#B2D1FF','#858588'),alpha=.9) #landmask


                # if self.arguments['--clev']:
                    # cnt_levelnum=int(self.arguments['--clev'])
                # else:
                    # cnt_levelnum=50

                # if not self.arguments['--cmap']:
                    # cs1=plt.contourf(x,y,name_of_array[tstep,:,:],\
                            # levels=np.linspace(self.minvar,self.maxvar,cnt_levelnum))
                # else:

                    # if self.arguments['--bcmapcentre']:
                        # #will plot colourmap centred around zero
                        # oldcmap=matplotlib.cm.get_cmap(self.arguments['--cmap'])
                        # shiftd=cmap_center_point_adjust(oldcmap,[self.minvar,self.maxvar],0)
                        # cs1=plt.contourf(x,y,name_of_array[tstep,:,:],\
                                # levels=np.linspace(self.minvar,self.maxvar,cnt_levelnum),\
                                # cmap=shiftd)
                    # else:
                        # cs1=plt.contourf(x,y,name_of_array[tstep,:,:],\
                                # levels=np.linspace(self.minvar,self.maxvar,cnt_levelnum),\
                                # cmap=self.arguments['--cmap'])


                # plt.colorbar(cs1)
                # #plt.show()

                scf.axisEqual3D(ax)

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

        scf.call_ffmpeg(self.workingfolder,outputdir=self.arguments['-o'])

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
