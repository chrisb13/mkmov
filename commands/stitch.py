import os
from ._stitch import _LogStart
_lg=_LogStart().setup()

from .scf import call_ffmpeg

"""
MkMov: sub-command "stitch" workhorse file.
"""

def stitch_action(workingfolder,args):
    """function to stitch files together using ffmpeg

    :workingfolder: directory where we will create some symlinks
    :args: arguments from the arg passer
    :returns: @todo
    """
    framecnt=1
    for infile in args['FILE_NAMES']:
        os.symlink(infile,workingfolder+'moviepar'+str(framecnt).zfill(5)+'.png')

        framecnt+=1

    if not args['--killsplash']:
        #adding logo at end.
        logo=os.path.dirname(os.path.realpath(__file__))+'/img/'+'mkmov_logo001_splash.png'
        nologo=False
        for more in range(20):
            try:
                os.symlink(logo,workingfolder+'moviepar'+str(framecnt).zfill(5)+'.png')
            except OSError:
                nologo=True
                break
            framecnt+=1

        if nologo:
            #on some file systems, like some network shares,  we can't make symlinks ..
            _lg.warning("Couldn't insert the logo at the end, sorry!")


    call_ffmpeg(workingfolder,fps_pass=args['--fps'],outputdir=args['-o'])

    #remove working folder
    if args['-o']:
        if os.path.exists(workingfolder):

            if not os.listdir(workingfolder):
                os.rmdir(workingfolder)
                _lg.info("Working folder: " + workingfolder +" removed.")
            else:
                _lg.warning("Working directory: " + workingfolder+" not empty, please remove manually")

