'''
utility functions
'''
import os
import subprocess
import traceback
import logging
logger = logging.getLogger(__name__)

class d(dict):
    '''
    dot.notation access to dictionary attributes
    '''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

#Context manager for changing the current working directory
class cd:
    def __init__(self, newPath):
        self.newPath = os.path.expanduser(newPath)
    def __enter__(self):
        self.savedPath = os.getcwd()
        os.chdir(self.newPath)
    def __exit__(self, etype, value, traceback):
        os.chdir(self.savedPath)

def run_cmd(cmd):
    '''
    runs cmd
    '''
    try:
        logger.info("running below command:")
        logger.info(str(cmd))
        output = subprocess.run(cmd, shell=True)
        if not output.returncode == 0:
            logger.error("there was an error running that command")
            return False
        else:
            logger.info("command ran successfully")
            return True
    except Exception as e:
        logger.error("there was an error in the python execution of that command")
        logger.error(traceback.format_exc())
