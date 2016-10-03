############
Usage
############

Functionality as follows:
::
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

--------------------
Basic usage
--------------------

We have tried to make this program as easy to install and use as possible. Interface is by command line and everything is done in one line!

A 2d movie (usage [T1]) is a good place to start, some of the options are the same across functions.

Basic usage, to make a 2d movie from a netCDF file is as follows: 
::
    #First activate python environment that has matplotlib, numpy and netCDF4 packages..
    git clone https://github.com/chrisb13/mkmov
    cd mkmov
    python mkmov.py 2d VARIABLE_NAME FILE_NAME
That's it! A .mov file will appear in a temporary directory as directed by the output (alternatively suggest an absolute path with -o option).

Usage, to make a movie from a list of png files (usage [T4]) is as follows: 
::
    #First activate python environment that has matplotlib, numpy and netCDF4 packages..
    git clone https://github.com/chrisb13/mkmov
    cd mkmov
    python mkmov.py stitch *.png FILE_NAMES

Here's a full example:

.. raw:: html

    <script type="text/javascript" src="https://asciinema.org/a/7etd14t6r4wqsccipcduhcrgo.js" id="asciicast-7etd14t6r4wqsccipcduhcrgo" async></script>

Note: you can pause the script and copy the code! **This movie refers to an older version of MkMov, insert '2d' after 'python mkmov.py'.**

MkMov comes with a few working examples which can be found by *python mkmov.py examples*. A netCDF file and some example png files are included in the examples folder, so these examples should work 'out of the box'. Indeed, these same examples form our `testing`_ suite!

.. _testing: https://raw.githubusercontent.com/chrisb13/mkmov/master/.travis.yml

Head over to the `examples`_ section to see some output and example commands:

.. _examples: http://christopherbull.com.au/mkmov/examples.html

--------------------
Usage comments
--------------------

* Mkmov will start faster and require much less memory resources if the --min MINIMUM and --max MAXIMUM arguments are used, see advanced usage below. Particularly important when passing multiple files.
* Mkmov expects full paths not relative paths.
* Usage [T2],[T3] are still in beta.

--------------------
More advanced usage
--------------------

See 'python mkmov.py help <command>' for more information on a specific command.

Look at the `examples`_ section to see some working examples. Also type 'python mkmov.py examples'.

.. _examples: http://christopherbull.com.au/mkmov/examples.html
