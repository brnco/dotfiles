# system files for Omphalos build

## material ocean

[Material Ocean theme](https://github.com/material-ocean/Material-Ocean)

# Install Guide for Omphalos

[Arch Wiki Install Guide](https://wiki.archlinux.org/title/installation_guide)

## initial setup

Using CHM 3083 Windows Surface Pro 3 with VirtualBox running Arch guest kneme

### Acquire iso

used MIT mirror

### check sig

used Arch VM with pacman-key and shared folder C:\Users\user\Downloads -> /mnt/Downloads

### prep install media

used Patriot 15GB USB drive. Had previous Arch bootable on it but because I'm making some changes and that was over a year old, decided to redo entirely.

#### delete previous data/ partitions

1. plug in drive
2. launch cmd.exe as admin
3. `diskpart`
4. `list disk`
5. `select Disk 1`
6. `clear`

#### add new partition

used MS Disk Management, formatted as FAT32

#### prep media

used Rufus

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

    mkfs.fat -F 32 /dev/sda1

    mkswap /dev/sda2

    swapon /dev/sda2

    mkfs.ext4 /dev/sda3

## mount big partition

    mount /dev/sda3 /mnt
    
## mount the EFI partition

    mount /dev/sda1 /mnt/boot/

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

### set locale

    pacman -S neovim

    nvim /etc/locale.gen

    uncomment "en_US.UTF-8 UTF-8"

    locale-gen

### set hostname

    nvim /etc/hostname

    omphalos

### create hostfile

    nvim /etc/hosts

    127.0.0.1   localhost

    ::1         localhost

    127.0.1.1   omphalos.localdomain    omphalos

### create users

    passwd - create new root password

    useradd -m bec - create your user name

    passwd bec

    usermod -aG wheel,audio,video,optical,storage bec

#### add sudo

    pacman -S sudo

    EDITOR=nvim visudo

    %wheel All=(ALL:ALL) ALL

### install systemd-boot loader
    
    bootctl install --graceful (from [here](https://github.com/systemd/systemd/issues/13603#issuecomment-864860578))
    
### configure boot entry

    https://wiki.archlinux.org/title/Systemd-boot#Loader_configuration
    
    including microcode from here
    
    https://wiki.archlinux.org/title/Systemd-boot#Adding_loaders
    
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

## cleanup

nouveau didn't like the startup without nvidia drivers but isntalling them removed the error

## other utils

(Reference)[https://wiki.archlinux.org/title/General_recommendations]

`sudo pacman -S git firefox starship neofetch nitrogen picom apache alacritty dolphin vifm moc tmux obs-studio ffmpeg vlc mediainfo openssh gcc make`

## desktop environment

### Xorg

(guide)[https://wiki.archlinux.org/title/Xorg]

`sudo pacman -S xorg-server xorg-xinit`

### nvidia

(guide)[https://wiki.archlinux.org/title/NVIDIA]

your GTX 960 is too old for the open-sourced NVIDIA drivers so you're usign regular NVIDIA dirvers instead (per (this tool)[https://www.nvidia.com/Download/index.aspx])

`sudo pacman -S nvidia nvidia-utils`

then, configure the driver for Xorg

`nvidia-xconfig`

### dwm

`git clone git://git.suckless.org/dwm
cd dwm
make
make clean install`

### set startx

nvim ~/.xinitrc
exec dwm

#### set startx -> run on login

`nvim ~/.bashrc
if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
    exec startx
fi`

# Firefox Color link

(Material Ocean Colors)[https://color.firefox.com/?theme=XQAAAALqAQAAAAAAAABBqYhm849SCia-yK6EGccwS-xMDPrzes6HTzD03vuOyKjlfyrdYZKg16ucwzn46LoiebXC5487A3ofFrMe55F9rFx50m4sLuktAxanbAFEtNgCMnO8o3xFG-UrJ8YxD0MCdT9DEFi2EqUK_Uffh9w32qYMp-RHlBWR6BmkZn2Nl7_fByF9weOsL3X6B41rkrzqiKo791Ec7VJWdKmC1D76jmgTeyG_5dDOQglqBgXk3LdWX0sCKodHPrj0I0ihJKqq6MwTlfIWq4Tf-B41BhGwnWnKpcvhbMsQOsUPz_AYdUT3TzHfG1WHaLmjr2P2Gq7Gm90tmtVY5G-DB8_f_5AsLUA]
