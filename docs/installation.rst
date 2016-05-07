
############
Installation
############

We have tried to keep dependencies to a minimum. Most users working with climate data and python will already have the following installed.

MkMov requires:

* matplotlib
* numpy
* netCDF4
* ffmpeg
* NCO tools (optional, needed for 2d --bias options)
* pandas (optional, needed for 2d --hamming)

*If you already have these installed, skip to the usage section.*

If you're not sure if you have the right packages or not, skip to usage and try and run mkmov and it will tell you if you do not have the correct python packages and ffmpeg.

-----------------------------
Matplotlib, numpy and netCDF4
-----------------------------

There are a number of ways to install the python packages matplotlib, numpy and netCDF4, Anaconda is recommend. 

Steps:

#. Go to `Anaconda`_ and get the lastest version of Anaconda
#. Install Anaconda with bash FILE_NAME, where FILE_NAME is the file you just downloaded
#. Add netCDF4 library with ``conda install netcdf4`` 

.. _Anaconda: https://www.continuum.io/downloads

------------
FFMPEG
------------

To install ffmpeg, assuming you are on a *nix system, then: 
::
    sudo apt-get install ffmpeg

Maybe that didn't work? If you're using Linux `Mint`_ this works:
::
    sudo add-apt-repository ppa:mc3man/trusty-media
    sudo apt-get update
    sudo apt-get install ffmpeg

.. _Mint: https://mintguide.org/video/339-installing-ffmpeg-library-on-linux-mint-via-ppa.html

------------------------------------------
Travis-CI environments using Conda
------------------------------------------
This package is tested with Travis-CI to see how these environments are set up have a look at this `file`_.

.. _file: https://raw.githubusercontent.com/chrisb13/mkmov/master/.travis.yml
