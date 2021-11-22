# system files for customization + notes for arch system maintenance

## individual colors/themes are on different branches

### material ocean

my take on the [Material Ocean theme](https://github.com/material-ocean/Material-Ocean)

### gruvbox

coming soon [Gruvbox](https://github.com/morhetz/gruvbox)

## to do

### general

integrate Gruvbox

### DWM

#### add patches

attachbottom

barheight

barpadding

centretitle

colorbar

cursorwarp

leftstack

swapfocus

winicon

### keybindings

look into [these](https://wiki.archlinux.org/title/Keyboard_shortcuts)

# upgrading zfs

## upgrading kernel independently

use this workflow if you've upgraded other software and, say, NVIDIA and Xorg updates no longer work on your outdated kernel. this will break your zfs install but let you use the rest of the computer. upgrade zfs-linux in a few days

ensure all relevant IgnorePkg lines are uncommented in /etc/pacman.conf

sudo pacman -Syu

error is two parts

part 1. zfs-linux can't be upgraded, would you like to skip? y

part2. linux upgrade breaks zfs-linux dependency linux=5.12.15

sudo pacman -Syu --assume-installed linux=5.12.15

^repeat this line for any zfs-related dependencies (incl. zfs-utils)

kernel can then (potentially) be downgraded to latest version that works with latest zfs version: sudo pacman -U https://archive.archlinux.org/repos/2021/11/21/core/os/x86_64/[version]

add linux to IgnorePkg in /etc/pacman.conf


