#!/usr/bin/env python
'''
manages backups
'''
#full python libraries
import os
import re
import configparser
import argparse
import logging
import time
import sys
#partial python libraries
from pprint import pprint
from pathlib import Path
from datetime import datetime, timedelta
#my libraries
import util

def parse_backup_dates(backups):
    '''
    parses backup dates and determines what goes where
    '''


def get_backup_dates(logs_path):
    '''
    gets the date of the last backup
    '''
    backups = util.d({})
    paths = sorted(logs_path.iterdir(), key=os.path.getmtime)
    print(paths[0])
    current_bu_date, current_bu_time = str(paths[0].name).split("_")
    with open(paths[0],"r") as f:
        last_log = f.read()
    sstr = "daily backup is \d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}"
    match = ''
    match = re.search(sstr,last_log)
    if match:
        match = match.group()
        daily_bu_date, daily_bu_time = match.replace("daily backup is ","").split("_")
    sstr = "weekly backup is \d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}"
    match = ''
    match = re.search(sstr,last_log)
    if match:
        match = match.group()
        weekly_bu_date, weekly_bu_time = match.replace("weekly backup is ","").split("_")
    sstr = "monthly backup is \d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}"
    match = ''
    match = re.search(sstr,last_log)
    if match:
        match = match.group()
        monthly_bu_date, monthly_bu_time = match.replace("monthly backup is ","").split("_")
    backups.current = util.d({"date":current_bu_date,"time":current_bu_time})
    backups.daily = util.d({"date":daily_bu_date,"time":daily_bu_time})
    backups.weekly = util.d({"date":weekly_bu_date,"time":weekly_bu_time})
    backups.monthly = util.d({"date":monthly_bu_date,"time":monthly_bu_time})
    pprint(backups)
    return backups

def run_backup():
    '''
    actually runs the backup
    '''
    cmd = "rsync -aAXHSv /* /mnt/omphalos_bak/ " + \
            "--exclude={/dev/*,/proc/*,/sys/*,/tmp/*,/run/*,/mnt/*,/media/*,\
            /lost+found,/home/*/.gvfs,/home/*/.cache/*,/etc/fstab,/etc/hosts,/etc/hostname}"

def make_backup(kwvars):
    '''
    creates the list of operations to perform when backing up
    '''
    last_backup_date = get_last_backup_date(kwvars.config.backup_logs)

def init_log(kwvars):
    '''
    initalizes log actions
    '''
    log_filename = Path(time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime()) + ".txt")
    log_filepath = kwvars.config.backup_logs / log_filename
    message_format = logging.Formatter('%(asctime)s %(levelname)s %(message)s',\
            datefmt='%Y-%m-%d %H:%M:%S')
    global logger
    logger = logging.getLogger()
    '''
    make a handler for the log file, add to logger
    '''
    log_handler = logging.FileHandler(log_filepath)
    log_handler.setFormatter(message_format)
    log_handler.setLevel(logging.DEBUG)
    logger.addHandler(log_handler)
    '''
    make a handler for printing to screen, add to logger
    '''
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(message_format)
    stream_handler.setLevel(kwvars.print_loglevel)
    logger.addHandler(stream_handler)
    logger.setLevel(logging.DEBUG)
    logger.info("initializing script and log")
    logger.debug(str(kwvars))

def init_config():
    '''
    gets info from config file
    '''
    config = util.d({})
    config = configparser.ConfigParser()
    config.read("config")
    config.backup_current = Path(config.get("backup","current"))
    config.backup_daily = Path(config.get("backup","daily"))
    config.backup_weekly = Path(config.get("backup","weekly"))
    config.backup_monthly = Path(config.get("backup","monthly"))
    config.backup_logs = Path(config.get("backup","logs"))
    return config

def init_args():
    '''
    initializes arguments from command line
    '''
    kwvars = util.d({})
    parser = argparse.ArgumentParser(description='manages backups')
    parser.add_argument('--test',action='store_true',default=False,\
            help="run in test mode, prints result to terminal")
    parser.add_argument('-v','--verbose',action='store_true',default=False,\
            help="verbose mode, print debug messages to terminal window")
    parser.add_argument('-q','--quiet',action='store_true',default=False,\
            help="quiet mode, only report errors to terminal window")
    args = parser.parse_args()
    kwvars.test = args.test
    if args.verbose:
        kwvars.print_loglevel = logging.DEBUG
    elif args.quiet:
        kwvars.print_loglevel = logging.WARNING
    else:
        kwvars.print_loglevel = logging.INFO
    return kwvars

def main():
    '''
    do the thing
    '''
    print("starting backup...")
    kwvars = init_args()
    kwvars.config = init_config()
    init_log(kwvars)
    daily_backup = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d_%H-%M-%S')
    weekly_backup = (datetime.now() - timedelta(7)).strftime('%Y-%m-%d_%H-%M-%S')
    monthly_backup = (datetime.now() - timedelta(30)).strftime('%Y-%m-%d_%H-%M-%S')
    logger.info("daily backup is " + daily_backup)
    logger.info("weekly backup is " + weekly_backup)
    logger.info("monthly backup is " + monthly_backup)
    kwvars.backups = get_backup_dates(kwvars.config.backup_logs)
    #kwvars = make_backup(kwvars)

if __name__ == "__main__":
    main()
