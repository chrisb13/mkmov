#python logging
import logging as lg
import time
import subprocess
import sys
import os
import socket

class LogStart(object):
   "class that sets up a logger"
   def __init__(self, fname,fout=False,level='debug'):
       if level=='debug':
           lvl=lg.DEBUG
       elif level=='info':
           lvl=lg.INFO
       elif level=='warning':
           lvl=lg.WARNING
       elif level=='error':
           lvl=lg.ERROR
       else: 
           raise Exception('You passed a bad logging level')

       if fout:
          lg.basicConfig(filename=fname,filemode='w',\
                  format='%(name)s - %(levelname)s - %(message)s'\
                  , level=lvl) #where filemode clobbers file
       else:
          lg.basicConfig(format='%(name)s - %(levelname)s - %(message)s',\
                  level=lvl)

       lg.info('')
       lg.info('SCRIPT started')
       lg.info('Logging level is: ' + level)
       localtime = time.asctime( time.localtime(time.time()) )
       #found from (see limitations):
       #http://stackoverflow.com/questions/7871319/how-to-know-who-is-importing-me-in-python
       lg.info("Path for script is : "+os.path.dirname(os.path.realpath(__name__)) )
       lg.info("Script name is : "+ str(sys.argv[0]))

       lg.info("Local current time : "+ str(localtime))

       lg.info("Machine run on : "+ socket.gethostname())
       if hasattr(sys, 'real_prefix'):
           lg.info("We are running inside a venv.")
       else:
           lg.info("We are not running inside a venv.")
           lg.info("")
           return

       lg.info("")
       command=subprocess.Popen(['pip','freeze'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
       pipout, piperr = command.communicate()
       lg.info("---Pip freeze (including system-wide) START...--- ")
       for pkg in pipout.splitlines():
           lg.info(pkg)
       lg.info("---Pip freeze (including system-wide) END.---")
       lg.info("")
       

