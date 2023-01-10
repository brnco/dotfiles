'''
synchronizes the current branch with the actual config files (& vice versa)
'''
from pathlib import Path

def palette():
    '''
    initializes palette for theme colors
    '''
    palette = {"primary":"#0F111A",
               "secondary":"#00010A",
               "accent":"#FF4151",
               "eightcolors":
               ["#3B4252",
                "#BF616A",
                "#A3BE8C",
                "#EBCB8B",
                "#81A1C1",
                "#B48EAD",
                "#88C0D0",
                "#E5E9F0"]}
    return palette

def alacritty(dotfiles):
    '''
    for alacritty terminal
    '''
    config_file = "alacritty.yml"
    dispersed = Path("/home/bcoates/.config/alacritty/")
    colors = "gruvbox.yml"
    dotfile = dotfiles / "alacritty/"
    return [(dotfile / config_file, dispersed / config_file),(dotfile / colors, dispersed/ colors)]

def bash(dotfiles):
    '''
    for .bashrc
    '''
    config_file = ".bashrc"
    dispersed = Path("/home/bcoates/")
    dotfile = dotfiles / "bash/"
    return [(dotfile / config_file, dispersed / config_file)]

def neofetch(dotfiles):
    '''
    for neofetch for making the terminal pretty
    '''
    config_file = "config.conf"
    special_file1 = "smpte.ascii"
    dispersed = Path("/home/bcoates/.config/neofetch")
    dotfile = dotfiles / "neofetch"
    return [(dotfile / config_file, dispersed / config_file),(dotfile / special_file1, dispersed)]

def nvim(dotfiles):
    '''
    for neovim
    '''
    config_file = "init.vim"
    plugins = "plugged"
    dispersed = Path("/home/bcoates/.config/nvim")
    dotfile = dotfiles / "nvim"
    return [(dotfile / config_file, dispersed / config_file), (dotfile / plugins, dispersed)]

def tmux(dotfiles):
    '''
    for terminal multiplexing
    '''
    config_file = ".tmux.conf"
    dispersed = "/home/bcoates"
    dotfile = dotfiles / "tmux"
    return [(dotfile / config_file, dispersed / config_file)]

def vifm(dotfiles):
    '''
    for vifm for pretty file mgmt
    '''
    config_file = "vifmrc"
    dispersed = Path("/home/bcoates/.vifm")
    colors = dispersed / "colors/"
    dotfile = dotfiles / "vifm"
    dots = [(dotfile / config_file, dispersed / config_file)]
    for color_file in colors.iterdir():
        dots.append((dotfile / color_file.relative_to(dispersed), dispersed / colors))
    return dots


