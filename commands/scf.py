import os
import subprocess
import glob
import numpy as np
import shutil
import sys

from ._scf import _LogStart
_lg=_LogStart().setup()


"""
subcommand common functions (scf) used by ./subcommands
"""

def pl_inset_title_box(ax,title,bwidth="20%",location=1):
    """
    Function that puts title of subplot in a box
    
    :ax:    Name of matplotlib axis to add inset title text box too
    :title: 'string to put inside text box'
    :returns: @todo
    """
    import matplotlib.pyplot as plt
    #for inset axes
    #hacked from:
    #http://matplotlib.org/examples/axes_grid/inset_locator_demo.html
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes, zoomed_inset_axes
    from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar

    axins = inset_axes(ax,
                       width=bwidth, # width = 30% of parent_bbox
                       height=.30, # height : 1 inch
                       loc=location)

    plt.setp(axins.get_xticklabels(), visible=False)
    plt.setp(axins.get_yticklabels(), visible=False)
    axins.set_xticks([])
    axins.set_yticks([])

    axins.text(0.5,0.3,title,
            horizontalalignment='center',
            transform=axins.transAxes,size=10)


def mkdir_sub(p):
    """make directory of path that is passed"""
    try:
       os.makedirs(p)
       _lg.info("output folder: "+p+ " does not exist, we will make one.")
    except OSError as exc: # Python >2.5
       import errno
       if exc.errno == errno.EEXIST and os.path.isdir(p):
          pass
       else: raise


def call_ffmpeg(pngfolder,fps_pass=None,outputdir=None):
    """function that actually calls ffmpeg to stitch all the png together
    
    :pngfolder: folder where all the pngs are that we are stitching together
    :fps_pass (optional): 
    :returns: None (except for a movie!)
    """
    def fixcomment(ffmpegcomm):
        """function that fixes the ffmpeg commaand so that it can be properly passed to subprocess
        
        Note:
        Based on:
        http://stackoverflow.com/questions/29801975/why-is-the-subprocess-popen-argument-length-limit-smaller-than-what-the-os-repor
        Poor form to use shell=True basically.
        
        :returns: list
        """
        newcomm=[]
        lw=''
        insidecomm=False
        for w in ffmpegcomm.split():
            if 'comment' in w:
                lw+=w
                insidecomm=True
            elif insidecomm:
                if '-vb' not in w:
                    lw+=w
                else:
                    newcomm.append(lw)
                    newcomm.append(w)
                    insidecomm=False
            else:
                newcomm.append(w)
        return newcomm
    
    #ollie's command didn't work on storm
    # os.chdir(pngfolder)
    # subprocess.call('ffmpeg -framerate 10 -y -i moviepar%05d.png -s:v 1920x1080 -c:v libx264 -profile:v high -crf 20 -pix_fmt yuv420p movie.mp4')

    # ffmpeg ideas:
    # ffmpeg -r 15 -i moviepar%05d.png -b 5000k -vcodec libx264 -y -an movie.mov

    _lg.info("Stitching frames together (might take a bit if you have lots of frames)...")

    FNULL = open(os.devnull, 'w')

    if fps_pass is not None:
        fps=str(fps_pass)
    else:
        fps=str(15)

    quality='20'
    if outputdir:
        os.chdir(pngfolder)
        # subprocess.call('ffmpeg -r '+fps+' -i moviepar%05d.png '+' -vb '+quality+'M -y -an '+outputdir,shell=True,stdout=FNULL, stderr=subprocess.STDOUT)
        comm='ffmpeg -r '+fps+' -i moviepar%05d.png '+' -metadata comment="'+' '.join(sys.argv)+'"'+' -vb '+quality+'M -y -an '+outputdir
        newcomm=fixcomment(comm)
        try:
            subprocess.call(newcomm,shell=False,stdout=FNULL, stderr=subprocess.STDOUT)
        except OSError, e:
            if len(newcomm[6])>10000:
                _lg.warning("Metadata likely too long, will not record")
                subprocess.call(newcomm[:5]+newcomm[7:],shell=False,stdout=FNULL, stderr=subprocess.STDOUT)
            else:
                _lg.error("Error: " + e)
                sys.exit()
    else:                                                       
        os.chdir(pngfolder)                                     

        newcomm=fixcomment('ffmpeg -r '+fps+' -i moviepar%05d.png '+' -metadata comment="'+' '.join(sys.argv)+'"'+' -vb '+quality+'M -y -an movie.mov')
        try:
            subprocess.call(newcomm,shell=True,stdout=FNULL, stderr=subprocess.STDOUT)
        except OSError, e:
            if len(newcomm[6])>10000:
                _lg.warning("Metadata likely too long, will not record")
                subprocess.call(newcomm[:5]+newcomm[7:],shell=False,stdout=FNULL, stderr=subprocess.STDOUT)
            else:
                _lg.error("Error: " + e)
                sys.exit()

    #remove png
    if os.path.isfile(pngfolder+'movie.mov') or os.path.isfile(outputdir):
        ifiles=sorted(glob.glob(pngfolder+ 'moviepar*.png' ))
        assert(ifiles!=[]),"glob didn't find any symlinks to remove anything!"
        for f in ifiles:
            os.remove(f)

        if os.path.isfile(pngfolder+'movie.mov'):
            _lg.info("MkMov SUCCESS, check it out: "+pngfolder+'movie.mov')

            sys.exit(0)

        if outputdir:
            if os.path.isfile(outputdir):
                _lg.info("Removing working folder: "+pngfolder)
                shutil.rmtree(pngfolder)
                _lg.info("MkMov SUCCESS, check it out: "+outputdir)

                sys.exit(0)
    else:
        _lg.info("MkMov FAIL")
        _lg.error("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")
        sys.exit(1)

def axisEqual3D(ax):
    """
    nice little hack to make the 3d plot look less cube like!
    from: http://stackoverflow.com/questions/8130823/set-matplotlib-3d-plot-aspect-ratio
    """
    extents = np.array([getattr(ax, 'get_{}lim'.format(dim))() for dim in 'xyz'])
    sz = extents[:,1] - extents[:,0]
    centers = np.mean(extents, axis=1)
    maxsize = max(abs(sz))
    r = maxsize/2
    for ctr, dim in zip(centers, 'xyz'):
        getattr(ax, 'set_{}lim'.format(dim))(ctr - r, ctr + r)
