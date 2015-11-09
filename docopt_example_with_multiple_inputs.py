#!/usr/bin/env python

"""
Example of how me might be able to have multipe inputs.

try these:
python docopt_example_with_multiple_inputs.py tempvar fileone.nc filetwo.nc filethree.nc
python docopt_example_with_multiple_inputs.py  -m 2 -f fileone_nc,tempvar,filetwo_nc,windvar

Usage:
    test.py -m <num> -f FILES
    test.py <var> <file_name>...

Arguments:
    var             name to plot
    file_name       path to NetCDF file to make movie

Options:
    -m  Flag that should be counted
    -f FILES comma sep
"""

import docopt
args=docopt.docopt(__doc__)
if args['-f']:
    args['-f'] = [str(x) for x in args['-f'].split(',')]
print(args)

#
