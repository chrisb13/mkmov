import sys
import os

sys.path.insert(0,os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from ._twod_lg import _LogStart
_lg=_LogStart().setup()



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

