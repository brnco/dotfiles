# system files for customization

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

rotatestack

swapfocus

winicon

### keybindings

look into [these](https://wiki.archlinux.org/title/Keyboard_shortcuts)

# cheat sheet

focused on dwm/ vim/ tmux keybindings

## nav

super+enter | push focused window to main

super+space | toggle to previous windowing mode

0 | start of line

$ | end of line

gg | first line

G | last line

5gg or 5G | goto line 5

A | insert at end of line

o | open newline below current line

## split window into panes

:sp | :vs | :only

horizontal split | vertical split | 1 pane only

## move between panes

tab

## hjkl

super+h | widen main

super+l | narrow main

super+j | focus 1 window down the stack

super+k | focus 1 window up the stack

# Arch Linux VirtualBox Install notes

[Arch Wiki Install Guide](https://wiki.archlinux.org/title/installation_guide)

## initial setup

Hard Disk - create vritual hard disk now

VDI

Dynamically allocated

### System

Processors

Enable EFI

### Display

Video Memory - max it out (currently 128MB)

Enable 3d Accel

### Storage

controller: IDE -> +

-- add arch linux iso (downloaded)

## Launch

### set keyboard layout

should be done automatically, but

    ls /usr/share/kbd/keymaps/**/*.map.gz | less

    loadkeys [keymap]

## get working internet

    ping google.com

## set system clock

    timedatectl set-ntp true

    timedatctl status

## partition disk

### set partition for boot

    fdisk -l

    fdisk /dev/sda

    g - create gpt partition table

    n - create new partition

    1 - set partition number

    enter - default start block

    +550M - EFI partition, needs to be 550MB

### set partition for swap

    n - new partition

    2 - partition number

    enter - default start block

    +2G - 2GB swap size

### set partition for linux install

    n - new partition

    3 - 3rd partition

    enter - default start block

    enter - default size/ end block

### set correct partition types for each of the above

#### boot

    t - change partition type

    1 - partition type

    1 - EFI system

#### swap

    t

    2

    19 - linmux swap

### write table to disk

    w

## make file systems

    mkfs.fat -F32 /dev/sda1

    mkswap /dev/sda2

    swapon /dev/sda2

    mkfs.ext4 /dev/sda3

## mount big partition

    mount /dev/sda3 /mnt

## run pacstrap

    pacstrap /mnt base linux linux-firmware

## generate fstab

    genfstab -U /mnt >> /mnt/etc/fstab

## setup in root dir of new install

    arch-chroot /mnt

### set timezone

    ln -sf /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

    ls /usr/share/zoneinfo/America - lists cities for zoneinfo

### set hardware clock

    hwclock --systohc

### set locale

    pacman -S neovim

    nvim /etc/locale.gen

    uncomment "en_US.UTF-8 UTF-8"

    locale-gen

### set hostname

    nvim /etc/hostname

    axil

### create hostfile

    nvim /etc/hosts

    127.0.0.1   localhost

    ::1         localhost

    127.0.1.1   axil.localdomain    axil

### create users

    passwd - create new root password

    useradd -m brnco - create your user name

    passwd brnco

    usermod -aG wheel,audio,video,optical,storage brnco

#### add sudo

    pacman -S sudo

    EDITOR=nvim visudo

    %wheel All=(ALL:ALL) ALL

### install some important stuff

    pacman -S grub efibootmgr dosfstools os-prober mtools
    
    mkdir /boot/EFI

    mount /dev/sda1 /boot/EFI

### GRUB install and config

    grub-install --target=x86_64-efi --bootloader-id=GRUB --efi-directory=/boot/EFI

    grub-mkconfig -o /boot/grub/grub.cfg

### install and enable Networkmanager

    pacman -S networkmanager

    systemctl enable NetworkManager

### exit chroot

    exit

### unmount

    umount -l /mnt

## shutdown

    shutdown now

## in VM settings -> Storage

click on .iso -> click disc with minus sign on it

## start VM

should see hostname for login

run ping to see if you have networking

# Firefox Color link

https://color.firefox.com/?theme=XQAAAALqAQAAAAAAAABBqYhm849SCia-yK6EGccwS-xMDPrzes6HTzD03vuOyKjlfyrdYZKg16ucwzn46LoiebXC5487A3ofFrMe55F9rFx50m4sLuktAxanbAFEtNgCMnO8o3xFG-UrJ8YxD0MCdT9DEFi2EqUK_Uffh9w32qYMp-RHlBWR6BmkZn2Nl7_fByF9weOsL3X6B41rkrzqiKo791Ec7VJWdKmC1D76jmgTeyG_5dDOQglqBgXk3LdWX0sCKodHPrj0I0ihJKqq6MwTlfIWq4Tf-B41BhGwnWnKpcvhbMsQOsUPz_AYdUT3TzHfG1WHaLmjr2P2Gq7Gm90tmtVY5G-DB8_f_5AsLUA
