'''
synchronizes the current branch with the actual config files (& vice versa)
'''
from pathlib import Path


def alacritty(dotfiles):
    '''
    for alacritty terminal
    '''
    config_file = "alacritty.yml"
    dispersed = Path("/home/bec/alacritty/")
    dotfile = dotfiles / "alacritty/"
    return [(dotfile / config_file, dispersed / config_file)]

def bash(dotfiles):
    '''
    for .bashrc
    '''
    config_file = ".bashrc"
    dispersed = Path("/home/bec/")
    dotfile = dotfiles / "bash/"
    return [(dotfile / config_file, dispersed / config_file)]

def neofetch(dotfiles):
    '''
    for neofetch for making the terminal pretty
    '''
    config_file = "config.conf"
    special_file1 = "smpte.ascii"
    dispersed = Path("/home/bec/.config/neofetch")
    dotfile = dotfiles / "neofetch"
    return [(dotfile / config_file, dispersed / config_file),(dotfile / special_file1, dispersed)]

