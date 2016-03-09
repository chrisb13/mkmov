
############
Usage
############

--------------------
Basic usage
--------------------

This utility is designed to:

#. make a movie from a NetCDF file or 
#. stitch together a series of *.png files. 

Interface is by command line and everything is done in one line!

We have tried to make this program as easy to install and use as possible.

Basic usage, to make a movie from a netCDF file is as follows: 
::
    #First activate python environment that has matplotlib, numpy and netCDF4 packages..
    git clone https://github.com/chrisb13/mkmov
    cd mkmov
    python mkmov.py VARIABLE_NAME FILE_NAME
That's it! A .mov file will appear in a temporary directory as directed by the output (alternatively suggest an absoolute path with -o option, details below).

Usage, to make a movie from a list of png files is as follows: 
::
    #First activate python environment that has matplotlib, numpy and netCDF4 packages..
    git clone https://github.com/chrisb13/mkmov
    cd mkmov
    python mkmov.py --stitch *.png FILE_NAMES

Here's a full example:

.. raw:: html

    <script type="text/javascript" src="https://asciinema.org/a/7etd14t6r4wqsccipcduhcrgo.js" id="asciicast-7etd14t6r4wqsccipcduhcrgo" async></script>

Note: you can pause the script and copy the code!

There are more working examples in run_mkmov_examples.sh (in the root of the repository). A netCDF file and some example png files are included in the examples folder, so these examples should work 'out of the box'. Indeed, these same examples form our `testing`_ suite!

.. _testing: https://raw.githubusercontent.com/chrisb13/mkmov/master/.travis.yml

Head over to the `examples`_ section to see some output and example commands:

.. _examples: http://christopherbull.com.au/mkmov/examples.html

--------------------
Usage comments
--------------------

* Mkmov will start faster and require much less memory resources if the --min MINIMUM and --max MAXIMUM arguments are used, see advanced usage below. Particularly important when passing multiple files.
* Mkmov expects full paths not relative paths

--------------------
More advanced usage
--------------------

Details to this section are ongoing as optional arguments are added.
::
    MkMov v0.3
    This is a python package for making movies. In can be used in two ways:
        1] from a netCDF file
        2] from a list of png files (use --stitch option)

    Interface is by command line. Fully working examples can be found in: run_mkmov_examples.sh

    Usage:
        mkmov.py -h
        mkmov.py [--min MINIMUM --max MAXIMUM --preview -o OUTPATH --lmask LANDVAR --fps FRATE --cmap PLTCMAP --clev LEVELS --4dvar DEPTHLVL --figwth WIDTH --fighgt HEIGHT --killsplash] VARIABLE_NAME FILE_NAME...
        mkmov.py --stitch [-o OUTPATH --fps FRATE --killsplash] FILE_NAMES...

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
        --killsplash                : do not display splash screen advertisement for MkMov at end of movie
        --stitch                    : stitch png files together with ffmpeg (files must be the same dimensions). Use absolute not relative path.

    Example tests (should work 'out of the box'):
    python mkmov.py zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
    python mkmov.py --min -1 --max 1 -o $(pwd)/zos_example.mov zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
    python mkmov.py --min -1 --max 1 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
    python mkmov.py --min -1 --max 1 --lmask 0 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
    python mkmov.py --min -1 --max 1 --lmask 0 --fps 10 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
    python mkmov.py --min -1 --max 1 --lmask 0 --fps 10 --cmap jet zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
    python mkmov.py --min -1 --max 1 --lmask 0 --fps 10 --cmap autumn --clev 60 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
    python mkmov.py --min -1 --max 1 --lmask 0 --figwth 10 --fighgt 12 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
    python mkmov.py --min -1 --max 1 --lmask 0 --figwth 10 --fighgt 12 --killsplash zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
    python mkmov.py --stitch -o $(pwd)/stitchmov.mov $(pwd)/examples/StitchMePlots/*.png
    python mkmov.py --stitch -o $(pwd)/stitchmov.mov --fps 10 $(pwd)/examples/StitchMePlots/*.png
    python mkmov.py --stitch -o $(pwd)/stitchmov.mov --fps 10 --killsplash $(pwd)/examples/StitchMePlots/*.png

    References:
        [1] http://matplotlib.org/examples/color/colormaps_reference.html
