import os
import subprocess
import glob
import numpy as np

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
        subprocess.call('ffmpeg -r '+fps+' -i moviepar%05d.png -vb '+quality+'M -y -an '+outputdir,shell=True,stdout=FNULL, stderr=subprocess.STDOUT)
    else:
        os.chdir(pngfolder)
        subprocess.call('ffmpeg -r '+fps+' -i moviepar%05d.png -vb '+quality+'M -y -an movie.mov',shell=True,stdout=FNULL, stderr=subprocess.STDOUT)

    #remove png
    if os.path.isfile(pngfolder+'movie.mov') or os.path.isfile(outputdir):
        ifiles=sorted(glob.glob(pngfolder+ 'moviepar*.png' ))
        assert(ifiles!=[]),"glob didn't find any symlinks to remove anything!"
        for f in ifiles:
            os.remove(f)

        if os.path.isfile(pngfolder+'movie.mov'):
            _lg.info("MkMov SUCCESS, check it out: "+pngfolder+'movie.mov')

        if outputdir:
            if os.path.isfile(outputdir):
                _lg.info("MkMov SUCCESS, check it out: "+outputdir)
    else:
        _lg.info("MkMov FAIL")
        _lg.error("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")
        sys.exit("Something went wrong with ffmpeg, it hasn't made a movie :( We won't delete the plots.")

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
