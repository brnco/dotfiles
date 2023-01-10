'''
synchronizes the current branch with the actual config files (& vice versa)
'''
import argparse
import inspect
import shutil
from pathlib import Path
from pprint import pp
import sync_locations
import util

def copy(kwvars):
    '''
    handles all file/ folder copying
    '''
    if kwvars.mode == "gather":
        print("gathering files from their dispersed locations -> dotfiles")
        input("press any key to initiate sync")
        for sync in kwvars.syncs:
            if sync[1].is_dir():
                shutil.copytree(sync[1], sync[0], dirs_exist_ok=True)
            else:
                shutil.copy2(sync[1],sync[0])
    if kwvars.mode == "disperse":
        print("sending files from dotfiles -> dispersed locations")
        input("press any key to initiate sync")
        for sync in kwvars.syncs:
            if sync[0].is_dir():
                shutil.copytree(sync[0], sync[1], dirs_exist_ok=True)
            else:
                shutil.copy2(sync[0],sync[1])

def get_syncs(kwvars):
    '''
    runs the functions from sync_locations, resulting in list of files to move
    '''
    kwvars.syncs = []
    for name,func in kwvars.sync_these:
        syncs = func(kwvars.dotfiles)
        for s in syncs:
            kwvars.syncs.append(s)
    return kwvars

def parse_software_to_sync(all_software,kwvars):
    '''
    matches list of software to sync to list of all sync-able software
    '''
    kwvars.sync_these = []
    for name, func in all_software:
        if name in kwvars.software_to_sync:
            kwvars.sync_these.append((name, func))
    return kwvars

def init_kwvars(software_list):
    '''
    initialize arguments into kwvars obj
    '''
    software_list.append("all")
    parser = argparse.ArgumentParser(description="gather and disperse dotfiles")
    parser.add_argument("--mode",choices=["gather","disperse"],default="gather",\
            help="the mode to run the script in, gather brings current config into dotfiles github repo" + \
            "disperse sends current dotfiles branch config to locations where configs are read")
    parser.add_argument("--software",dest="sw",nargs="*",choices=software_list,default="all",\
            help="the software to gather/ disperse config for")
    args = parser.parse_args()
    kwvars = util.d({})
    kwvars.dotfiles = Path("/home/bcoates/code/dotfiles")
    kwvars.mode = args.mode
    kwvars.software_to_sync = args.sw
    return kwvars

def init_software_list():
    '''
    gets a list of all software we can update via thsi script
    i.e. a lsit of all the functions we've defined
    '''
    all_functions = inspect.getmembers(sync_locations, inspect.isfunction)
    software_list = []
    for name, func in all_functions:
        software_list.append(name)
    return all_functions, software_list

def main():
    '''
    do the thing
    '''
    print("starting...")
    all_functions, software_list = init_software_list()
    kwvars = init_kwvars(software_list)
    kwvars = parse_software_to_sync(all_functions, kwvars)
    kwvars = get_syncs(kwvars)
    pp(kwvars)
    copy(kwvars)

if __name__ == "__main__":
    main()
