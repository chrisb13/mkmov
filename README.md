![alt tag](https://raw.github.com/chrisb13/mkmov/master/img/mkmovlogo001.png)

# mkmov
python movie maker for NetCDF files

# Usage
```
MkMov v0.3
This is a python script for making movies. In can be used in two ways:
    1] from a netCDF file
    2] from a list of png files (use --stitch option)
    
Interface is by command line.

Usage:
    main.py -h
    main.py [--min MINIMUM --max MAXIMUM --preview -o OUTPATH] VARIABLE_NAME FILE_NAME...
    main.py --stitch [-o OUTPATH] FILE_NAMES...
    
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
    --preview                   : show a preview of the plot (will exit afterwards)
    -o OUTPATH                  : path/to/folder/to/put/movie/in/moviename.mov  (needs to be absolute path, no relative paths)
    --stitch                    : stitch png files together with ffmpeg (files must be the same dimensions)
    
Examples: 
python main.py --help
python main.py tos /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/1989/cordex24-ERAI01_1d_19890101_19890105_grid_T_2D.nc 
python main.py tos /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc 
python main.py --min -1 --max 1 --preview zos /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/nemo_cordex24_ERAI01/*/cordex24-ERAI01_1d_*_grid_T_2D.nc 
python main.py --stitch -o ~/temp/movie.mov /srv/ccrc/data42/z3457920/20151012_eac_sep_dynamics/analysis/nemo_cordex24_FLATFCNG_ERAI01_sepfinder/19940101_sepfinderplots/moviepar0000*
```

# tutorial I followed to create sphinx docs
http://dont-be-afraid-to-commit.readthedocs.org/en/latest/documentation.html

Also see:
http://stackoverflow.com/questions/1553800/how-to-upload-html-documentation-generated-from-sphinx-to-github
https://daler.github.io/sphinxdoc-test/includeme.html

Okay, I think this is the guide to use:
http://raxcloud.blogspot.com.au/2013/02/documenting-python-code-using-sphinx.html

Ollie want to implement? Just use the last link I think...
