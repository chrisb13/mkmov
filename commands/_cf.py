##   Author: Christopher Bull. 
##   Affiliation: Climate Change Research Centre and ARC Centre of Excellence for Climate System Science.
##                Level 4, Mathews Building
##                University of New South Wales
##                Sydney, NSW, Australia, 2052
##   Contact: z3457920@student.unsw.edu.au
##   www:     christopherbull.com.au
##   Date created: Thu Jun  5 10:11:55 EST 2014
##   Machine created on: squall.ccrc.unsw.edu.au
##
##   The virtualenv packages available on creation date (includes systemwide):
##   Cartopy==0.11.x
##   Cython==0.19.1
##   Fiona==1.1.2
##   GDAL==1.10.1
##   Jinja==1.2
##   Jinja2==2.7.2
##   MDP==3.3
##   MarkupSafe==0.18
##   PyNGL==1.4.0
##   Pygments==1.6
##   ScientificPython==2.8
##   Shapely==1.3.0
##   Sphinx==1.2.1
##   backports.ssl-match-hostname==3.4.0.2
##   basemap==1.0.7
##   brewer2mpl==1.4
##   descartes==1.0.1
##   distribute==0.7.3
##   docutils==0.11
##   geopandas==0.1.0.dev-1edddad
##   h5py==2.2.0
##   ipython==1.2.0
##   joblib==0.7.1
##   matplotlib==1.3.1
##   netCDF4==1.0.4
##   nose==1.3.3
##   numexpr==2.2.2
##   numpy==1.8.1
##   pandas==0.13.1
##   patsy==0.2.1
##   pexpect==2.4
##   prettyplotlib==0.1.7
##   progressbar==2.3
##   py==1.4.20
##   pycairo==1.8.6
##   pygrib==1.9.7
##   pyhdf==0.8.3
##   pyparsing==2.0.2
##   pyproj==1.9.3
##   pyshp==1.2.1
##   pytest==2.5.2
##   python-dateutil==2.2
##   pytz==2014.1
##   pyzmq==14.0.1
##   scikit-learn==0.13.1
##   scipy==0.12.0
##   seaborn==0.3.1
##   six==1.6.1
##   statsmodels==0.5.0
##   tables==3.0.0
##   tornado==3.2.1
##   virtualenv==1.10.1
##   wsgiref==0.1.2
##   xmltodict==0.8.6
##
##   The modules availabe on creation date:
##   # Currently Loaded Modulefiles:
#   1) hdf5/1.8.11-intel    5) matlab/2011b         9) perl/5.18.2
#   2) ncview/2.1.2         6) python/2.7.5        10) gdal/1.10.1
#   3) netcdf/3.6.3-intel   7) proj/4.8.0
#   4) intel/13.1.3.192     8) geos/3.3.3
##   # Currently Loaded Modulefiles:
#   1) hdf5/1.8.11-intel    5) matlab/2011b         9) perl/5.18.2
#   2) ncview/2.1.2         6) python/2.7.5        10) gdal/1.10.1
#   3) netcdf/3.6.3-intel   7) proj/4.8.0
#   4) intel/13.1.3.192     8) geos/3.3.3

#
#python logging
import logging as _logging 
from functools import wraps as _wraps

class _LogStart(object):
   "class that sets up a logger"
   def setup(self,fname=''):
       if fname=='':
           _logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
               level=_logging.DEBUG,disable_existing_loggers=True)
       else:
          _logging.basicConfig(filename=fname,filemode='w',format='%(name)s - %(levelname)s - %(message)s',
                  level=lg.DEBUG,disable_existing_loggers=False) #where filemode clobbers file

       lg = _logging.getLogger(__name__)
       return lg

if __name__ == "__main__":                                     #are we being run directly?
   lg=_LogStart().setup()
   #lg=meh.go()
   print __name__

   #LogStart(args.inputdir+'asciplot_lc_katana'+args.fno + '.log',fout=True)
   lg.info('moo')

   #PUT wothwhile code here!

