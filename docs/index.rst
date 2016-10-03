.. MkMov documentation master file, created by
   sphinx-quickstart on Fri Nov  6 10:54:15 2015.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

MkMov documentation!
=================================

.. image:: https://raw.githubusercontent.com/chrisb13/mkmov/master/img/mkmovlogo001.png

---------------------------------
What does it do?
---------------------------------

This utility is designed to make a movie from a NetCDF file or stitch together a series of *.png files. Interface is by command line and everything is done in one line! All code is on `GitHub`_, `pull requests`_ welcome!

.. _Github: https://github.com/chrisb13/mkmov

.. _pull requests: https://help.github.com/articles/creating-a-pull-request/

MkMov's utility is best shown by an example, here is AVISO global allsat madt, output is daily and variable is adt.

.. raw:: html
    
    <iframe width="480" height="385" src="https://youtube.com/embed/JEMj05o-KA4" frameborder="0" allowfullscreen></iframe>

This movie was created with a single line command, namely
::
    python mkmov.py 2d adt --lmask -214748 --cmap Set3 -o /srv/ccrc/data42/z3457920/mkmovmovies4/AVISOdt_global_allsat_madt_Set3.mov /srv/ccrc/data42/z3457920/RawData/AVISO/RawData/dt_global_allsat_madt/ftp.aviso.altimetry.fr/global/delayed-time/grids/madt/all-sat-merged/h/*/*.nc &>  /srv/ccrc/data42/z3457920/mkmovmovies4/15.log &

MkMov does more than just filled contour plots, have a look at `usage`_ to see other options. More examples with their respective run command `here`_.

.. _here: http://christopherbull.com.au/mkmov/examples.html

---------------------------------
Getting started quickly...
---------------------------------

Already have matplotlib, numpy, netCDF4 and ffmpeg? Jump straight to `usage`_ or check out this video. Note: video can be paused and you can copy and paste code!

.. _usage: http://christopherbull.com.au/mkmov/usage.html

.. raw:: html

    <script type="text/javascript" src="https://asciinema.org/a/7etd14t6r4wqsccipcduhcrgo.js" id="asciicast-7etd14t6r4wqsccipcduhcrgo" async></script>

Need to install some python packages or ffmpeg? Have a look at the `installation section`_.

.. _installation section: http://christopherbull.com.au/mkmov/installation.html

Contents:

.. toctree::
   :maxdepth: 2
   
   installation
   usage
   examples
   contributing
   all-about-me


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

