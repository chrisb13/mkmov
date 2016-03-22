"""
MkMov v0.4
This is a python package for making movies. It has three things it can do:
    [T1] movie of a netCDF file plotting contourf output (see "python mkmov.py 2d -h");
    [T2] movie of a netCDF file plotting slices of a 3d variable as a 3d cube (see "python mkmov.py 3dcube -h");
    [T3] movie of a netCDF file plotting a 2d variable as a 3d surface (see "python mkmov.py 3dsurf -h");
    [T4] stitch a list of png files into a movie ("see python mkmov.py stitch -h").

Usage: 
    mkmov.py -h --help
    mkmov.py <command> [-h --help] [<args>...]

Commands:
   2d          [T1] use a netCDF file make a contourf of a 2d field
   3dcube      [T2] use a netCDF file make a movie of a 3d field as a 3d cube
   3dsurf      [T3] use a netCDF file make a movie of a 2d field as a 3d surface
   stitch      [T4] stitch files together using ffmpeg
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
    mkmov.py [--min MINIMUM --max MAXIMUM --preview --bias TIMENAME --bcmapcentre -o OUTPATH --lmask LANDVAR --lmask2 LANDVAR2 --lmaskfld --fps FRATE --cmap PLTCMAP --clev LEVELS --4dvar DEPTHLVL --figwth WIDTH --fighgt HEIGHT --x XVARIABLE --y YVARIABLE --killsplash] VARIABLE_NAME FILE_NAME...

Arguments:
    VARIABLE_NAME   variable name
    FILE_NAME       path to NetCDF file to make movie, can also be a list of files (dimensions must be the same)
    FILE_NAMES      list of files to stich with ffmpeg 

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
    --x XVARIABLE               : variable to plot on the x-axis (nb: if you specify a xvariable, you must select a yvariable.)
    --y YVARIABLE               : variable to plot on the y-axis (nb: if you specify a yvariable, you must select a xvariable.)
    --killsplash                : do not display splash screen advertisement for MkMov at end of movie
    --stitch                    : stitch png files together with ffmpeg (files must be the same dimensions). Use absolute not relative path.

References:
    [1] http://matplotlib.org/examples/color/colormaps_reference.html
"""

cube3d = \
"""
MkMov: sub-command "3dcube" help.
    [T2] movie of a netCDF file plotting slices of a 3d variable as a 3d cube.

Usage: basic.py 3dcube [options] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].
"""

surf3d = \
"""
MkMov: sub-command "3dsurf" help.
    [T3] movie of a netCDF file plotting a 2d variable as a 3d surface.

Usage: basic.py 3dsurf [options] [<name>]

  -h --help         Show this screen.
  --caps            Uppercase the output.
  --greeting=<str>  Greeting to use [default: Hello].
"""

STITCH = \
"""
MkMov: sub-command "stitch" help.
    [T4] stitch a list of png files into a movie ("see python mkmov.py stitch -h").

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

EXAMPLES=\
"""
python mkmov.py 2d zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 -o $(pwd)/zos_example.mov zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --fps 10 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --fps 10 --cmap jet zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --fps 10 --cmap autumn --clev 60 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --figwth 10 --fighgt 12 zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py 2d --min -1 --max 1 --lmask 0 --figwth 10 --fighgt 12 --killsplash zos examples/cordex24-ERAI01_1d_20040101_20040111_grid_T_2D.nc
python mkmov.py stitch -o $(pwd)/stitchmov.mov $(pwd)/examples/StitchMePlots/*.png
python mkmov.py stitch -o $(pwd)/stitchmov.mov --fps 10 $(pwd)/examples/StitchMePlots/*.png
python mkmov.py stitch -o $(pwd)/stitchmov.mov --fps 10 --killsplash $(pwd)/examples/StitchMePlots/*.png
"""

from docopt import docopt
import subprocess
def greet(args):
    print(args)

if __name__ == '__main__':
    arguments = docopt(__doc__, options_first=True)

    if arguments['<command>'] == '2d':
        greet(docopt(TWOD))
    elif arguments['<command>'] == '3dcube':
        greet(docopt(cube3d))
    elif arguments['<command>'] == '3dsurf':
        greet(docopt(surf3d))
    elif arguments['<command>'] == 'stitch':
        greet(docopt(STITCH))
    elif arguments['<command>'] == 'examples':
        print(EXAMPLES)
    #display help messages
    #this needs to be above, what comes next...
    elif arguments['<command>'] == 'help' and len(arguments['<args>'])==0:
        subprocess.call(['python','greet.py', '--help'])
    elif arguments['<command>'] == 'help' and (arguments['<args>'][0] in '2d 3dcube 3dsurf stitch examples'.split()):
        subprocess.call(['python','greet.py', arguments['<args>'][0],'--help'])
    elif arguments['<command>'] == 'help' and not (arguments['<args>'][0] in '2d 3dcube 3dsurf stitch examples'.split()):
        print "I don't recognise that sub-command"
    else:
        print "error"
