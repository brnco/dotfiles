# system files for pi-backyardwatcher build

# Install Guide for pi-backyardwatcher

[Arch ARM Install Guide](https://archlinuxarm.org/platforms/armv8/broadcom/raspberry-pi-3)

## step 9 above

use root login (so you can use pacman, sudo isn't installed)

## post-install

### update mirrors and stuff

    pacman -Syu

### create users

    passwd - create new root password

    useradd -m bec - create your user name

    passwd bec

    usermod -aG wheel,audio,video,optical,storage bec

### install your favorite text editor

    pacman -S neovim
    
### set hostname

    nvim /etc/hostname

    pi-backyardwatcher

### create hostfile

    nvim /etc/hosts

    127.0.0.1   localhost

    ::1         localhost

    127.0.1.1   pi-backyardwatcher.localdomain    pi-backyardwatcher

### add sudo

    pacman -S sudo

    EDITOR=nvim visudo

    %wheel All=(ALL:ALL) ALL 

### install and enable Networkmanager

    pacman -S networkmanager

    systemctl enable NetworkManager
    
    systemctl start NetworkManager.service

## other utils

[Reference](https://wiki.archlinux.org/title/General_recommendations)

`sudo pacman -S git starship neofetch apache alacritty tmux ffmpeg mediainfo openssh base-devel unzip tree`

### get ssh going

    systemctl enable sshd
    
    systemctl start sshd.service

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
