# system files for pi-backyardwatcher build

# Install Guide for pi-backyardwatcher

[Arch Wiki Install Guide](https://wiki.archlinux.org/title/installation_guide)

## initial setup

Using Omphalos

### Acquire iso

used MIT mirror

### check sig

pacman-key -v ~/Downloads/archlinux-2023.03.01-x86_64.iso.sig

### prep install media

used SanDisk MicroSD card in Vanja adapter for USB. drive

#### delete previous data/ partitions

1. plug in drive
2. sudo cat ~/Downloads/archlinux-2023.03.01-x86_64.iso > /dev/sdf

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

already contained EFI partiton but was MBR so we're re-doing everything

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

    mkfs.fat -F 32 /dev/sdf1

    mkswap /dev/sdf2

    swapon /dev/sdf2

    mkfs.ext4 /dev/sdf3

## mount big partition

    mount /dev/sdf3 /mnt
    
## mount the EFI partition

    mkdir /mnt/boot

    mount /dev/sdf1 /mnt/boot/

## run pacstrap

    pacstrap /mnt base linux linux-firmware

## generate fstab

    genfstab -U /mnt >> /mnt/etc/fstab

## setup in root dir of new install

    arch-chroot /mnt

### set timezone

    ln -sf /usr/share/zoneinfo/America/LosAngeles /etc/localtime

    ls /usr/share/zoneinfo/America - lists cities for zoneinfo

### set hardware clock

    hwclock --systohc

### install your favorite text editor

    pacman -S neovim
    
### set locale

    nvim /etc/locale.gen

    uncomment "en_US.UTF-8 UTF-8"

    locale-gen

### set hostname

    nvim /etc/hostname

    pi-backyardwatcher

### create hostfile

    nvim /etc/hosts

    127.0.0.1   localhost

    ::1         localhost

    127.0.1.1   pi-backyardwatcher.localdomain    pi-backyardwatcher

### create users

    passwd - create new root password

    useradd -m bec - create your user name

    passwd bec

    usermod -aG wheel,audio,video,optical,storage bec

### add sudo

    pacman -S sudo

    EDITOR=nvim visudo

    %wheel All=(ALL:ALL) ALL

### install systemd-boot loader
    
from [here](https://github.com/systemd/systemd/issues/13603#issuecomment-864860578)
    
    bootctl install --graceful
    
### get root partition UUID

this is the partition used by linux, not boot partition

    blkid -s PARTUUID -o value /dev/sdf3 >> /boot/loader/entries/arch.conf

### configure boot entry

    *esp*/loader/entries/arch.conf
    title   Arch Linux
    linux   /vmlinuz-linux
    initrd  /intel-ucode.img
    initrd  /initramfs-linux.img
    options root=PARTUUID=*UUID from previous step* rw
    
    cp arch.conf arch-fallback.conf
    
    *esp*/loader/entries/arch-fallback.conf
    title   Arch Linux (fallback initramfs)
    linux   /vmlinuz-linux
    initrd  /intel-ucode.img
    initrd  /initramfs-linux-fallback.img
    options root=PARTUUID=*UUID from previous step* rw
    
### install microcode

    sudo pacman -S intel-ucode

### install and enable Networkmanager

    pacman -S networkmanager

    systemctl enable NetworkManager

### exit chroot

    exit

### unmount

    umount -l /mnt

## shutdown

    shutdown now
    
# Post Install

## other utils

[Reference](https://wiki.archlinux.org/title/General_recommendations)

`sudo pacman -S git starship neofetch apache alacritty tmux ffmpeg mediainfo openssh base-devel unzip tree`

## get your dang dotfiles

### add new system to GH ssh

[guide](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

### clone and set up

    cd ~/code
    git clone git@github.com:brnco/dotfiles.git
    cd ~/code/dotfiles
    git branch pi-backyardwatcher
    git branch --set-upstream-to=origin/pi-backyardwatcher pi-backyardwatcher
    
## beyond

### yay

get your [aur helper](https://aur.archlinux.org/packages/yay)

### nerd-fonts-complete

get [one single font](https://archlinux.org/packages/community/any/ttf-meslo-nerd/)

TO DO - configure the fonts

### your neofetch build

clone [this](https://github.com/brnco/neofetch) then make install it

### your tmux config

clone [this](https://github.com/thewtex/tmux-mem-cpu-load) then cmake make install it

## sound

   sudo pacman -S alsa-utils
   
   alsamixer

turn main volume up/ unmute with m key

# Firefox Color link

[Material Ocean Colors](https://color.firefox.com/?theme=XQAAAALqAQAAAAAAAABBqYhm849SCia-yK6EGccwS-xMDPrzes6HTzD03vuOyKjlfyrdYZKg16ucwzn46LoiebXC5487A3ofFrMe55F9rFx50m4sLuktAxanbAFEtNgCMnO8o3xFG-UrJ8YxD0MCdT9DEFi2EqUK_Uffh9w32qYMp-RHlBWR6BmkZn2Nl7_fByF9weOsL3X6B41rkrzqiKo791Ec7VJWdKmC1D76jmgTeyG_5dDOQglqBgXk3LdWX0sCKodHPrj0I0ihJKqq6MwTlfIWq4Tf-B41BhGwnWnKpcvhbMsQOsUPz_AYdUT3TzHfG1WHaLmjr2P2Gq7Gm90tmtVY5G-DB8_f_5AsLUA)
