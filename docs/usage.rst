
############
Usage
############

Welcome to MkMov. This utility is designed to make a movie from a NetCDF file.

We have tried to make this program as easy to install and use as possible.

Basic usage is as follows: 
::
    #First activate python environment that has matplotlib and netCDF4 packages..
    git clone ...
    cd mkmov
    python main.py FILE_NAME VARIABLE_NAME
That's it! A .mov file will appear in your mkmov folder with your movie.


--------------------
More advanced usage
--------------------

Details to this section are ongoing as optional arguments are added.
::
    MkMov v0.1
    This is a python script for making movies from a netCDF file.

    Example: python main.py /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/1989/cordex24-ERAI01_1d_19890101_19890105_grid_T_2D.nc tos

    Usage:
        main.py -h
        main.py FILE_NAME VARIABLE_NAME 

    Arguments:
        FILE_NAME       path to NetCDF file to make movie
        VARIABLE_NAME   variable name

    Options:
        -h,--help          : show this help message
