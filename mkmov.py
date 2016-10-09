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
This is a python package for making movies. It has four things it can do:
    [T1] movie of a netCDF file plotting contourf output (see "python mkmov.py 2d -h");
    [T2] movie of a netCDF file plotting slices of a 3d variable as a 3d cube (see "python mkmov.py 3dcube -h");
    [T3] movie of a netCDF file plotting a 2d variable as a 3d surface (see "python mkmov.py 3dsurf -h");
    [T4] stitch a list of png files into a movie ("see python mkmov.py stitch -h").
    [T5] movie of two netCDF files plotting quiver of U/V fields from a C-grid
    [T6] movie of a netCDF file plotting pcolormesh output using basemap

Usage: 
    mkmov.py -h --help
    mkmov.py <command> [-h --help] [<args>...]

Commands:
   2d          [T1] use a netCDF file make a contourf of a 2d field
   3dcube      [T2] use a netCDF file make a movie of a 3d field as a 3d cube
   3dsurf      [T3] use a netCDF file make a movie of a 2d field as a 3d surface
   stitch      [T4] stitch files together using ffmpeg
   quiver      [T5] use two netCDF files to make a quiver of a 2d field
   2dbm        [T6] use a netCDF file make a contourf of a 2d field and use basemap
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
    mkmov.py 2d [--min MINIMUM --max MAXIMUM --preview --bias TIMENAME --bcmapcentre -o OUTPATH --lmask LANDVAR --lmask2 LANDVAR2 --lmaskfld --fps FRATE --cmap PLTCMAP --clev LEVELS --4dvar DEPTHLVL --figwth WIDTH --tstart TSTART --tdelta TDELTA --hamming HWINSIZE --crop CROPDIMS --zoominset ZOOMDIMS --fighgt HEIGHT --x XVARIABLE --y YVARIABLE --x2d XVARTWOD --y2d YVARTWOD --fixdateline --maggrad --vertgrad --hozgrad --extmin --extmax --extboth --killsplash] VARIABLE_NAME FILE_NAME...

Arguments:
    VARIABLE_NAME   variable name
    FILE_NAME       path to NetCDF file to make movie, can also be a list of files (dimensions must be the same)

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
    --tstart TSTART             : the start date, this will insert the time onto each frame (nb: if you select a tstart, you must also select a tdelta.) String will be handled by np.datetime64. See [2] for acceptable combinations.
    --tdelta TDELTA             : the time step between each frame, this will insert the time onto each frame (nb: if you select a tdelta, you must also select a tstart.) String will be handled by np.timedelta64 (unit must match tstart), format is: 'n_F' where n is the multiple and F is the frequency, e.g. '5_D' is every five days. See [2] for acceptable options.
    --hamming HWINSIZE          : plot low and high pass anomalies from a hamming window mean, specify window size. Must be an odd number.
    --crop CROPDIMS             : crop plot to xmin_xmax_ymin_ymax
    --zoominset ZOOMDIMS        : zoom inset plot to xmin_xmax_ymin_ymax_loc_height_width, loc_height_width are optional, so format is xmin_xmax_ymin_ymax OR xmin_xmax_ymin_ymax_loc_height_width. loc is between 0-10, height is in inches (e.g. 1.3) and width is in percentages (e.g. 80%). See [3] for more details.
    --x XVARIABLE               : variable to plot on the x-axis (nb: if you specify a xvariable, you must select a yvariable.)
    --y YVARIABLE               : variable to plot on the y-axis (nb: if you specify a yvariable, you must select a xvariable.)
    --x2d XVARTWOD              : variable to plot on the x-axis (nb: if you specify a xvartwod, you must select a yvartwod.) This is for unstructured grids, when coordinates depend on both (x,y).
    --y2d YVARTWOD              : variable to plot on the y-axis (nb: if you specify a yvartwod, you must select a xvartwod.) This is for unstructured grids, when coordinates depend on both (x,y).
    --fixdateline               : fix the dateline on --x2d (nb: if you select --fixdateline, you must specify --x2d and --y2d). Warning: only tested on NEMO output.
    --maggrad                   : plot the horizontal magnitude of the gradient of the field (i.e. sqrt(grad(field)[0]^2+grad(field)[1]^2))
    --vertgrad                  : plot the vertical gradient of the field F (i.e. dF/dy). NB: cannot be used with maggrad. Assumes y is in 'first' coord.
    --hozgrad                   : plot the horizontal gradient of the field F (i.e. dF/dx). NB: cannot be used with maggrad. Assumes x is in 'second' coord.
    --extmin                    : 'extend' the contourf colour range on the minimum end only
    --extmax                    : 'extend' the contourf colour range on the maximum end only
    --extboth                   : 'extend' the contourf colour range on both the minimum and maximum ends (cannot be specified with --extmin or --extmax)
    --killsplash                : do not display splash screen advertisement for MkMov at end of movie

References:
    [1] http://matplotlib.org/examples/color/colormaps_reference.html
    [2] http://docs.scipy.org/doc/numpy/reference/arrays.datetime.html
    [3] http://matplotlib.org/mpl_toolkits/axes_grid/users/overview.html (see insetLocator section) and http://stackoverflow.com/questions/10824156/matplotlib-legend-location-numbers
"""

cube3d = \
"""
MkMov: sub-command "3dcube" help.
    [T2] movie of a netCDF file plotting slices of a 3d variable as a 3d cube.

Usage: 
    mkmov.py 3dcube [-o OUTPATH --preview --killsplash] VARIABLE_NAME FILE_NAME...

Arguments:
    VARIABLE_NAME   variable name
    FILE_NAME       path to NetCDF file to make movie, can also be a list of files (dimensions must be the same)

Options:
    -h,--help                   : show this help message
    -o OUTPATH                  : path/to/folder/to/put/movie/in/moviename.mov  (needs to be absolute path, no relative paths)
    --preview                   : show a preview of the plot (will exit afterwards).
    --killsplash                : do not display splash screen advertisement for MkMov at end of movie

Note: feature is still in development.
"""

surf3d = \
"""
MkMov: sub-command "3dsurf" help.
    [T3] movie of a netCDF file plotting a 2d variable as a 3d surface.

Usage: 
    mkmov.py 3dsurf [--min MINIMUM --max MAXIMUM -o OUTPATH --preview --killsplash] VARIABLE_NAME FILE_NAME...

Arguments:
    VARIABLE_NAME   variable name
    FILE_NAME       path to NetCDF file to make movie, can also be a list of files (dimensions must be the same)

Options:
    -h,--help                   : show this help message
    --min MINIMUM               : the minimum value for the contour map (nb: if you select a min, you must select a max.)
    --max MAXIMUM               : the maximum value for the contour map (nb: if you select a max, you must select a min.)
    -o OUTPATH                  : path/to/folder/to/put/movie/in/moviename.mov  (needs to be absolute path, no relative paths)
    --preview                   : show a preview of the plot (will exit afterwards).

Note: feature is still in development.
"""

STITCH = \
"""
MkMov: sub-command "stitch" help.
    [T4] stitch a list of png files into a movie.

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

QUIVERTWOD=\
"""
MkMov: sub-command "quiver" help.
    [T5] movie of two netCDF files plotting quiver of U/V fields from a C-grid

Usage: 
    mkmov.py quiver [--min MINIMUM --max MAXIMUM -o OUTPATH --preview --vorticity --magonly --tfile TFILE --tfilevar TFILEVAR --cmap PLTCMAP --lmask LANDVAR --4dvar DEPTHLVL --x2d XVARTWOD --y2d YVARTWOD --fixdateline] VAR_X VAR_Y FILE_NAME...

Arguments:
    VAR_X           variable name in the x direction
    VAR_Y           variable name in the y direction
    FILE_NAME       path to NetCDF files to make movie, can also be a list of files (dimensions must be the same). Must contain at least two files

Options:
    -h,--help                   : show this help message
    -o OUTPATH                  : path/to/folder/to/put/movie/in/moviename.mov  (needs to be absolute path, no relative paths)
    --preview                   : show a preview of the plot (will exit afterwards).
    --vorticity                 : plot vorticity
    --magonly                   : plot magnitude of vector only
    --tfile TFILE               : plot land mask from T-file            (must specify tfilevar), assumes a 3d file from NEMO T-grid.
    --tfilevar TFILEVAR         : variable from T-file to plot landmask (must specify tfile)
    --cmap PLTCMAP              : matplotlib color map to contourf with. See [1] for options.
    --lmask LANDVAR             : land value to mask out (will draw a solid black contour around the land points)
    --4dvar DEPTHLVL            : passing 4d variable of the form (time,depth,spatialdim1,spatialdim2), DEPTHLVL is the depth/height level you would like to plot (default is level 0).
    --min MINIMUM               : the minimum value for the contour map (nb: if you select a min, you must select a max.)
    --max MAXIMUM               : the maximum value for the contour map (nb: if you select a max, you must select a min.)
    --x2d XVARTWOD              : variable to plot on the x-axis (nb: if you specify a xvartwod, you must select a yvartwod.) This is for unstructured grids, when coordinates depend on both (x,y).
    --y2d YVARTWOD              : variable to plot on the y-axis (nb: if you specify a yvartwod, you must select a xvartwod.) This is for unstructured grids, when coordinates depend on both (x,y).
    --fixdateline               : fix the dateline on --x2d (nb: if you select --fixdateline, you must specify --x2d and --y2d). Warning (experimental): only tested on NEMO output.

References:
    [1] http://matplotlib.org/examples/color/colormaps_reference.html
"""


TWODBM=\
"""
MkMov: sub-command "2dbm" help.
    [T6] movie of a netCDF file plotting pcolormesh output using basemap

Usage: 
    mkmov.py 2dbm [--preview --proj PROJECTION  --boundinglat LATBOUND --rotatex XSPEED --xorigin XSTART --yorigin YSTART --zoom ZOOM --min MINIMUM --max MAXIMUM --cmap PLTCMAP --4dvar DEPTHLVL  -o OUTPATH] X_NAME Y_NAME VARIABLE_NAME FILE_NAME...

Arguments:
    X_NAME          variable for longitudes
    Y_NAME          variable for latitudes
    VARIABLE_NAME   variable name
    FILE_NAME       path to NetCDF file to make movie, can also be a list of files (dimensions must be the same)

Options:
    -h,--help                   : show this help message
    --preview                   : show a preview of the plot (will exit afterwards).
    --proj PROJECTION           : projection, options are [2], default is 'moll'
    --boundinglat LATBOUND      : bounding latitude, needed for some projections, e.g. [5]
    --rotatex XSPEED            : spin/rotate the x coordinate (each frame will increment the specified number of degrees)
    --xorigin XSTART            : xcenter of map will be located at xorigin (default is 130 E)
    --yorigin YSTART            : ycenter of map will be located at yorigin (default is 0    )
    --zoom ZOOM                 : zoom plot to llcrnrlon_llcrnrlat_urcrnrlon_urcrnrlat, e.g. Australian region is: 90.25_-50_220.25_-10.75. See [3] for more details. NB: this will only be effective on some projections (e.g. not moll but merc normally works)
    --min MINIMUM               : the minimum value for the contour map (nb: if you select a min, you must select a max.)
    --max MAXIMUM               : the maximum value for the contour map (nb: if you select a max, you must select a min.)
    --cmap PLTCMAP              : matplotlib color map to pcolormesh with. See [4] for options.
    --4dvar DEPTHLVL            : passing 4d variable of the form (time,depth,spatialdim1,spatialdim2), DEPTHLVL is the depth/height level you would like to plot (default is level 0).
    -o OUTPATH                  : path/to/folder/to/put/movie/in/moviename.mov  (needs to be absolute path, no relative paths)

References:
    [1] http://matplotlib.org/basemap/
    [2] http://matplotlib.org/basemap/users/mapsetup.html
    [3] http://basemaptutorial.readthedocs.io/en/latest/utilities.html
    [4] http://matplotlib.org/examples/color/colormaps_reference.html
    [5] http://matplotlib.org/basemap/users/pstere.html
"""



EXAMPLES=\
"""
MkMov: sub-command "examples". Here are some examples that work 'out of the box' (example data included).

    [T1] movie of a netCDF file plotting contourf output (see "python mkmov.py 2d -h");
python mkmov.py 2d zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 -o $(pwd)/zos_example.mov zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --fps 10 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --fps 10 --cmap jet zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --fps 10 --cmap autumn --clev 60 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --figwth 10 --fighgt 12 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --figwth 10 --fighgt 12 --killsplash zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc

    [T4] stitch a list of png files into a movie ("see python mkmov.py stitch -h").
python mkmov.py stitch -o $(pwd)/stitchmov.mov $(pwd)/examples/StitchMePlots/*.png
python mkmov.py stitch -o $(pwd)/stitchmov.mov --fps 10 $(pwd)/examples/StitchMePlots/*.png
python mkmov.py stitch -o $(pwd)/stitchmov.mov --fps 10 --killsplash $(pwd)/examples/StitchMePlots/*.png
"""


from docopt import docopt
import commands as sc
import subprocess

if __name__ == "__main__": 
    # not really sure why global logger is no longer working :(
    # lg=cb2logger.LogStart('',fout=False)

    arguments_top = docopt(__doc__, options_first=True)

    sc.check_dependencies()

    if arguments_top['<command>'] == '2d':
        arguments=docopt(TWOD)

        workingfol=sc.workingfol_func(arguments)

        sc.dispay_passed_args(arguments,workingfol)

        #We are in 2d movie making mode...
        #main.py [OPTIONS] VARIABLE_NAME FILE_NAME...
        if not arguments['--preview']:
            #for travis-ci
            import matplotlib
            matplotlib.use('Agg')

        movmk=sc.MovMaker(arguments['FILE_NAME'],arguments['VARIABLE_NAME'],workingfol,arguments)

        #aah I've always wanted to say this!
        movmk.lights(minvar=arguments['--min'],maxvar=arguments['--max'])
        if not arguments['--hamming']:
            movmk.camera(plotpreview=arguments['--preview'])
        else:
            movmk.camera_hamming(plotpreview=arguments['--preview'])
        movmk.action()
        # movmk.cleanup()

    elif arguments_top['<command>'] == '3dcube':

        arguments=docopt(cube3d)

        workingfol=sc.workingfol_func(arguments)

        sc.dispay_passed_args_threedcube(arguments,workingfol)

        if not arguments['--preview']:
            #for travis-ci
            import matplotlib
            matplotlib.use('Agg')

        movmk=sc.MovMakerThreeDCube(arguments['FILE_NAME'],arguments['VARIABLE_NAME'],workingfol,arguments)

        #aah I've always wanted to say this!
        movmk.lights()
        movmk.camera()
        movmk.action()
        # movmk.cleanup()

    elif arguments_top['<command>'] == '3dsurf':

        arguments=docopt(surf3d)

        workingfol=sc.workingfol_func(arguments)

        sc.dispay_passed_args_threedsurf(arguments,workingfol)

        if not arguments['--preview']:
            #for travis-ci
            import matplotlib
            matplotlib.use('Agg')

        movmk=sc.MovMakerThreeDSurf(arguments['FILE_NAME'],arguments['VARIABLE_NAME'],workingfol,arguments)

        #aah I've always wanted to say this!
        movmk.lights()
        movmk.camera(minvar=arguments['--min'],maxvar=arguments['--max'])
        movmk.action()

    elif arguments_top['<command>'] == 'stitch':

        arguments=docopt(STITCH)
        workingfol=sc.workingfol_func(arguments)
        sc.stitch_action(workingfol,arguments)

    elif arguments_top['<command>'] == 'quiver':
        arguments=docopt(QUIVERTWOD)
        workingfol=sc.workingfol_func(arguments)

        sc.dispay_passed_args_quiver(arguments,workingfol)

        if not arguments['--preview']:
            #for travis-ci
            import matplotlib
            matplotlib.use('Agg')

        movmk=sc.MovMakerQuiver(arguments['FILE_NAME'],arguments['VAR_X'],arguments['VAR_Y'],workingfol,arguments)

        # #aah I've always wanted to say this!
        movmk.lights()
        movmk.camera(plotpreview=arguments['--preview'])
        movmk.action()
        # movmk.cleanup()

    elif arguments_top['<command>'] == '2dbm':
        arguments=docopt(TWODBM)
        workingfol=sc.workingfol_func(arguments)

        sc.dispay_passed_args_twodbm(arguments,workingfol)

        if not arguments['--preview']:
            #for travis-ci
            import matplotlib
            matplotlib.use('Agg')

        movmk=sc.MovMakerTwodBM(arguments['FILE_NAME'],arguments['VARIABLE_NAME'],workingfol,arguments)

        # #aah I've always wanted to say this!
        movmk.lights()
        movmk.camera(plotpreview=arguments['--preview'])
        movmk.action()
        # movmk.cleanup()

    elif arguments_top['<command>'] == 'examples':
        print(EXAMPLES)

    #display help messages
    elif arguments_top['<command>'] == 'help' and len(arguments_top['<args>'])==0:
        subprocess.call(['python','mkmov.py', '--help'])

    elif arguments_top['<command>'] == 'help' and (arguments_top['<args>'][0] in '2d 3dcube 3dsurf stitch examples'.split()):
        subprocess.call(['python','mkmov.py', arguments_top['<args>'][0],'--help'])

    elif arguments_top['<command>'] == 'help' and not (arguments_top['<args>'][0] in '2d 3dcube 3dsurf stitch examples'.split()):
        print("MkMov: I don't recognise that sub-command. Type 'python mkmov.py -h' to see available sub-commands.")
    else:
        print("MkMov: I don't recognise that command. Type 'python mkmov.py -h' for help.")
