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

def parse_backup_dates_for_removal(dirs,_days):
    '''
    parses backup dates and determines what goes where
    '''
    remove_dirs = []
    for subdir in dirs:
        s = datetime.strptime(subdir.name,'%Y-%m-%d')
        timeframe = datetime.now() - timedelta(days=_days)
        if timeframe > s:
            remove_dirs.append(subdir)
    return remove_dirs

def init_daily_backups(kwvars):
    '''
    initializes info for daily backups
    '''
    daily_subdirs = [x for x in kwvars.config.backup_daily.iterdir() if x.is_dir()]
    kwvars.backups.daily = util.d({"path":kwvars.config.backup_daily})
    kwvars.backups.daily.remove_dirs = parse_backup_dates_for_removal(daily_subdirs,7)
    most_recent_backup = datetime.strptime(str(sorted(daily_subdirs)[-1].name),'%Y-%m-%d')
    yesterday = datetime.now() - timedelta(days=1)
    if yesterday > most_recent_backup:
        kwvars.backups.daily.needs_new_backup = True
    else:
        kwvars.backups.daily.needs_new_backup = False
    pprint(kwvars)
    return kwvars

def init_weekly_backups(kwvars):
    '''
    initializes info for weekly backups
    '''
    weekly_subdirs = [x for x in kwvars.config.backup_weekly.iterdir() if x.is_dir()]
    kwvars.backups.weekly = util.d({"path":kwvars.config.backup_weekly})
    kwvars.backups.weekly.remove_dirs = parse_backup_dates_for_removal(weekly_subdirs,28)
    most_recent_backup = datetime.strptime(str(sorted(weekly_subdirs)[-1].name),'%Y-%m-%d')
    last_week = datetime.now() - timedelta(days=7)
    if most_recent_backup > last_week:
        kwvars.backups.weekly.needs_new_backup = True
    else:
        kwvars.backups.weekly.needs_new_backup = False
    pprint(kwvars)
    return backups

def make_current_backup():
    '''
    actually runs the backup
    '''
    cmd = "rsync -aAXHSv /* /mnt/omphalos_bak/ " + \
            "--exclude={/dev/*,/proc/*,/sys/*,/tmp/*,/run/*,/mnt/*,/media/*,\
            /lost+found,/home/*/.gvfs,/home/*/.cache/*,/etc/fstab,/etc/hosts,/etc/hostname}"

def make_todays_backup(kwvars):
    '''
    moves current backup to daily backups subfolder with today's date
    '''
    today = datetime.strftime(datetime.now(),'%Y-%m-%d')
    cmd = "sudo rsync -aAXHSv /mnt/omphalos_bak/ " + str(kwvars.backups.daily.path / today)
    ran_ok = util.run_cmd(cmd)
    if not ran_ok:
        logger.error("the script encountered an error running  that command")
        return False
    return True

def make_backup(kwvars):
    '''
    creates the list of operations to perform when backing up
    '''
    kwvars = init_daily_backups(kwvars)
    if kwvars.backups.daily.needs_new_backup == True:
        backup_worked = make_todays_backup(kwvars)
    if not backup_worked:
        logger.error("there was a problem writing today's backup, quitting...")
        exit()
    kwvars = init_weekly_backups(kwvars)

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
    kwvars.backups = util.d({})
    return kwvars

def main():
    '''
    do the thing
    '''
    print("starting backup...")
    kwvars = init_args()
    kwvars.config = init_config()
    init_log(kwvars)
    #daily_backup = (datetime.now() - timedelta(1)).strftime('%Y-%m-%d_%H-%M-%S')
    #weekly_backup = (datetime.now() - timedelta(7)).strftime('%Y-%m-%d_%H-%M-%S')
    #monthly_backup = (datetime.now() - timedelta(30)).strftime('%Y-%m-%d_%H-%M-%S')
    #logger.info("daily backup is " + daily_backup)
    #logger.info("weekly backup is " + weekly_backup)
    #logger.info("monthly backup is " + monthly_backup)
    #kwvars.backups = get_backup_dates(kwvars.config.backup_logs)
    kwvars = make_backup(kwvars)

if __name__ == "__main__":
    main()
