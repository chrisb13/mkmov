![alt tag](https://raw.github.com/chrisb13/mkmov/master/img/mkmovlogo001.png)

# Travis-ci status
[![Build Status](https://travis-ci.org/chrisb13/mkmov.svg)](https://travis-ci.org/chrisb13/mkmov)

# mkmov
Welcome to MkMov. This utility is designed to make a movie from a NetCDF file or stitch together a series of *.png files. Interface is by command line and everything is done in one line!

# Official Documentation
[Official documentation here.](http://christopherbull.com.au/mkmov/)

# Usage
[![asciicast](https://asciinema.org/a/7etd14t6r4wqsccipcduhcrgo.png)](https://asciinema.org/a/7etd14t6r4wqsccipcduhcrgo)

```
MkMov v0.3
This is a python script for making movies. In can be used in two ways:
    1] from a netCDF file
    2] from a list of png files (use --stitch option)

Interface is by command line. Fully working examples can be found in: run_mkmov_examples.sh

Usage:
    mkmov.py -h
    mkmov.py [--min MINIMUM --max MAXIMUM --preview -o OUTPATH --lmask LANDVAR --fps FRATE --cmap PLTCMAP --clev LEVELS] VARIABLE_NAME FILE_NAME...
    mkmov.py --stitch [-o OUTPATH --fps FRATE] FILE_NAMES...

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
    --cmap PLTCMAP              : matplotlib color map to contourf with
    --clev LEVELS               : number of colour levels to have on the contour map (default is 30). See [1] for options.
    --stitch                    : stitch png files together with ffmpeg (files must be the same dimensions)

Example tests (should work 'out of the box'):
python mkmov.py zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 -o $(pwd)/zos_example.mov zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 --lmask 0 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 --lmask 0 --fps 10 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 --lmask 0 --fps 10 --cmap jet zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --min -1 --max 1 --lmask 0 --fps 10 --cmap autumn --clev 60 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py --stitch -o $(pwd)/stitchmov.mov $(pwd)/examples/StitchMePlots/*.png
python mkmov.py --stitch -o $(pwd)/stitchmov.mov --fps 10 $(pwd)/examples/StitchMePlots/*.png

References:
    [1]
```

## Contact      

Christopher Bull.   
Climate Change Research Centre and ARC Centre of Excellence for Climate System Science.
University of New South Wales                                           Sydney, NSW, Australia, 2052     
e: z3457920@student.unsw.edu.au                                     
w: christopherbull.com.au
gh: github.com/chrisb13
t: @ChrisBullOceanO

