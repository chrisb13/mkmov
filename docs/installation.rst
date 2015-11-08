
############
Installation
############

We have tried to keep dependencies to a minimum. Most users working with climate data and python will already have the following installed.

MkMov requires:

* matplotlib
* netCDF4
* ffmpeg

*If you already have these installed, skip to the usage section.*

If you're not sure if you have the right packages or not, skip to usage and try and run mkmov and it will tell you if you do not have the correct python packages and ffmpeg.

------------
Matplotlib and netCDF4
------------

There are a number of ways to install the python packages matplotlib and netCDF4 we recommend Anaconda. 

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

