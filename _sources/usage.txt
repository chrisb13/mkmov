
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

--------------------
More advanced usage
--------------------

Details to this section are ongoing as optional arguments are added.
::
    MkMov v0.3
    This is a python script for making movies. In can be used in two ways:
        1] from a netCDF file
        2] from a list of png files (use --stitch option)

    Interface is by command line.

    Usage:
        mkmov.py -h
        mkmov.py [--min MINIMUM --max MAXIMUM --preview -o OUTPATH] VARIABLE_NAME FILE_NAME...
        mkmov.py --stitch [-o OUTPATH] FILE_NAMES...

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
        --stitch                    : stitch png files together with ffmpeg (files must be the same dimensions)
