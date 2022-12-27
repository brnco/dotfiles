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
import shutil
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
    logger.debug("initializing info for daily backups")
    daily_subdirs = [x for x in kwvars.config.backup_daily.iterdir() if x.is_dir()]
    kwvars.backups.daily = util.d({"path":kwvars.config.backup_daily,\
                                "subdirs":daily_subdirs})
    logger.debug(daily_subdirs)
    most_recent_backup = datetime.strptime(str(sorted(daily_subdirs)[-1].name),'%Y-%m-%d')
    logger.debug(most_recent_backup)
    yesterday = datetime.now() - timedelta(days=1)
    logger.debug(yesterday)
    logger.debug(yesterday > most_recent_backup)
    if yesterday > most_recent_backup:
        kwvars.backups.daily.needs_new_backup = True
    else:
        kwvars.backups.daily.needs_new_backup = False
    logger.debug(kwvars)
    return kwvars

def init_monthly_backups(kwvars):
    '''
    initializes info for monthly backups
    '''
    logger.debug("initializing info for monthly backups")
    monthly_subdirs = [x for x in kwvars.config.backup_monthly.iterdir() if x.is_dir()]
    kwvars.backups.monthly = util.d({"path":kwvars.config.backup_monthly,\
                            "subdirs":monthly_subdirs})
    logger.debug(monthly_subdirs)
    kwvars.backups.monthly.remove_dirs = parse_backup_dates_for_removal(monthly_subdirs,365)
    most_recent_backup = datetime.strptime(str(sorted(monthly_subdirs)[-1].name),'%Y-%m-%d')
    last_month = datetime.now() - timedelta(days=28)
    if most_recent_backup < last_month:
        kwvars.backups.monthly.needs_new_backup = True
        kwvars.backups.monthly.origin = get_monthly_backup_origin(kwvars)
    else:
        kwvars.backups.monthly.needs_new_backup = False
    logger.debug(kwvars)
    return kwvars

def get_monthly_backup_origin(kwvars):
    '''
    determines the weekly backup to copy to monthly
    '''
    logger.debug("determining the weekly backup to copy to monthly")
    most_recent_backup_weekly = sorted(kwvars.backups.monthly.subdirs)[0]
    current_weekly_origins = kwvars.backups.weekly.subdirs
    closeness = timedelta(days=0)
    monthly_origin = False
    for potential_origin in current_weekly_origins:
        _closeness = datetime.strptime(potential_origin.name,"%Y-%m-%d") - \
                datetime.strptime(most_recent_backup_weekly.name,"%Y-%m-%d")
        if _closeness == timedelta(days=28):
            monthly_origin = potential_origin
            break
        elif _closeness > closeness and _closeness < timedelta(days=28):
            closeness = _closeness
            monthly_origin = potential_origin
    if not monthly_origin:
        logger.error("there was a problem determining the origin of the monthly backup")
        logger.error("but the script detected that a new monthly backup is necessary")
        logger.error("please investigate")
        return False
    return monthly_origin

def init_weekly_backups(kwvars):
    '''
    initializes info for weekly backups
    '''
    logger.debug("initializing weekly backups")
    weekly_subdirs = [x for x in kwvars.config.backup_weekly.iterdir() if x.is_dir()]
    kwvars.backups.weekly = util.d({"path":kwvars.config.backup_weekly,\
                            "subdirs":weekly_subdirs})
    logger.debug(weekly_subdirs)
    kwvars.backups.weekly.remove_dirs = parse_backup_dates_for_removal(weekly_subdirs,28)
    most_recent_backup = datetime.strptime(str(sorted(weekly_subdirs)[-1].name),'%Y-%m-%d')
    logger.debug(most_recent_backup)
    last_week = datetime.now() - timedelta(days=7)
    logger.debug(last_week)
    if most_recent_backup < last_week:
        kwvars.backups.weekly.needs_new_backup = True
        kwvars.backups.weekly.origin = get_weekly_backup_origin(kwvars)
    else:
        kwvars.backups.weekly.needs_new_backup = False
    logger.debug(kwvars)
    return kwvars

def get_weekly_backup_origin(kwvars):
    '''
    determines the daily backup to copy to weekly
    '''
    logger.debug("determining the daily backup to copy to weekly")
    most_recent_backup_weekly = sorted(kwvars.backups.weekly.subdirs)[0]
    current_daily_origins = kwvars.backups.daily.subdirs
    logger.debug(current_daily_origins)
    closeness = timedelta(days=0)
    weekly_origin = False
    for potential_origin in current_daily_origins:
        logger.debug("potential origin")
        logger.debug(potential_origin)
        _closeness = datetime.strptime(potential_origin.name,"%Y-%m-%d") - \
                datetime.strptime(most_recent_backup_weekly.name,"%Y-%m-%d")
        if _closeness == timedelta(days=7):
            weekly_origin = potential_origin
            break
        elif _closeness > closeness and _closeness < timedelta(days=7):
            closeness = _closeness
            weekly_origin = potential_origin
        logger.debug("current weekly origin")
        logger.debug(weekly_origin)
    if not weekly_origin:
        logger.error("there was a problem determining the origin of the weekly backup")
        logger.error("but the script detected that a new weekly backup is necessary")
        logger.error("please investigate")
        return False
    return weekly_origin

def make_monthly_backup(kwvars):
    '''
    copies a weekly backup to monthly
    '''
    logger.info("creating monthly backup from origin " + str(kwvars.backups.monthly.origin))
    cmd = "sudo rsync -aAXHSv " + str(kwvars.backups.monthly.origin) + " " + str(kwvars.backups.monthly.path)
    ran_ok = util.run_cmd(cmd)
    if not ran_ok:
        logging.error("the script encoutnered an error creating the monthly backup")
        return False
    return True

def make_weekly_backup(kwvars):
    '''
    copies a daily backup to weekly
    '''
    logger.info("creating weekly backup from origin " + str(kwvars.backups.weekly.origin))
    cmd = "sudo rsync -aAXHSv " + str(kwvars.backups.weekly.origin) + " " + str(kwvars.backups.weekly.path)
    ran_ok = util.run_cmd(cmd)
    if not ran_ok:
        logger.error("there was an error copying the daily backup to weekly")
        return False
    return True

def make_current_backup():
    '''
    runs the most recent backup (every few hours)
    '''
    logger.info("starting current backup...")
    cmd = "sudo rsync -aAXHSv /* /mnt/omphalos_bak/ " + \
            "--exclude={/dev/*,/proc/*,/sys/*,/tmp/*,/run/*,/mnt/*,/media/*,/lost+found" + \
            "/home/*/.gvfs,/home/*/.cache/*,/home/*/.mozilla/*," + "/etc/fstab,/etc/hosts,/etc/hostname}"
    ran_ok = util.run_cmd(cmd)
    if not ran_ok:
        logger.error("the script encountered an error creating the current backup")
        return False
    return True

def make_todays_backup(kwvars):
    '''
    moves current backup to daily backups subfolder with today's date
    '''
    logger.info("creating today's backup...")
    today = datetime.strftime(datetime.now(),'%Y-%m-%d')
    logging.info('copying current backup to todays backup ' + today)
    cmd = "sudo rsync -aAXHSv /mnt/omphalos_bak/ " + str(kwvars.backups.daily.path / today)
    ran_ok = util.run_cmd(cmd)
    if not ran_ok:
        logger.error("the script encountered an error creating today's backup")
        return False
    kwvars.backups.daily.scrub = False
    if len(list(kwvars.config.backup_daily.glob('*'))) > 7:
        kwvars.backups.daily.scrub = True
    return True

def make_backup(kwvars):
    '''
    manages the backups process
    '''
    logger.info("starting backup process...")
    '''
    start with daily backup
    '''
    kwvars = init_daily_backups(kwvars)
    if kwvars.backups.daily.needs_new_backup == True:
        backup_worked = make_todays_backup(kwvars)
        if not backup_worked:
            logger.error("there was a problem writing today's backup, quitting...")
            exit()
        '''
        if we copy current to daily, make a new current
        '''
        backup_worked = make_current_backup()
        if not backup_worked:
            logger.error("there was a problem creating the current backup, quitting...")
            exit()
    '''
    make curent backup if requested
    '''
    if kwvars.backup_now == True and kwvars.backups.daily.needs_new_backup == False:
        backup_worked = make_current_backup(kwvars)
        if not backup_worked:
            logger.error("there was a problem writing a new current backup, quitting...")
            exit()
    '''
    make the weekly backup if necessary
    '''
    kwvars = init_weekly_backups(kwvars)
    if kwvars.backups.weekly.needs_new_backup == True:
        backup_worked = make_weekly_backup(kwvars)
        if not backup_worked:
            logger.error("there was a problem writing the new weekly backup, quitting...")
            exit()
    '''
    make the monthly backup if necessary
    '''
    kwvars = init_monthly_backups(kwvars)
    if kwvars.backups.monthly.needs_new_backup == True:
        backup_worked = make_monthly_backup(kwvars)
        if not backup_worked:
            logger.error("there was a problem writing the new monthly backup, quitting...")
            exit()
    '''
    delete superflous directories
    '''
    scrub_backup_dirs(kwvars)

def scrub_backup_dirs(kwvars):
    '''
    manages the process of removing overflow dirs from daily, weekly, monthly folder
    '''
    logger.info("deleting old folders in daily, weekly, monthly dirs")
    if kwvars.backups.daily.scrub:
        kwvars.backups.daily.remove_dirs = parse_backup_dates_for_removal(\
                kwvars.backups.daily.path,7)
    if kwvars.backups.weekly.scrub:
        kwvars.backups.weekly.remove_dirs = parse_backup_dates_for_removal(\
                kwvars.backups.weekly.path,28)
    if kwvars.backups.monthly.scrub:
        kwvars.backups.monthly.remove_dirs = parse_backup_dates_for_removal(\
                kwvars.backups.monthly.path,365)
    remove_dirs = []
    if kwvars.backups.daily.remove_dirs:
        remove_dirs += kwvars.backups.daily.remove_dirs
    if kwvars.backups.weekly.remove_dirs:
        remove_dirs += kwvars.backups.weekly.remove_dirs
    if kwvars.backups.monthly.remove_dirs:
        remove_dirs += kwvars.backups.monthly.remove_dirs
    for d in remove_dirs:
        logger.info("removing overflow dir: " + str(d))
        shutil.rmtree(d)

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
    parser.add_argument('--now',action='store_true',default=False,\
            help="make a new current backup")
    args = parser.parse_args()
    kwvars.test = args.test
    if args.verbose:
        kwvars.print_loglevel = logging.DEBUG
    elif args.quiet:
        kwvars.print_loglevel = logging.WARNING
    else:
        kwvars.print_loglevel = logging.INFO
    kwvars.backups = util.d({})
    kwvars.backup_now = args.now
    return kwvars

def main():
    '''
    do the thing
    '''
    print("starting backup...")
    kwvars = init_args()
    kwvars.config = init_config()
    init_log(kwvars)
    kwvars = make_backup(kwvars)

if __name__ == "__main__":
    main()
