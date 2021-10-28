#!/bin/bash
echo "starting"
alacritty=$HOME"/.config/alacritty/alacritty.yml"
alacrittybak="$alacritty.bak"
bashrc=$HOME"/.bashrc"
bashrcbak="$bashrc.bak"
nvim=$HOME"/.config/nvim/init.vim"
nvimbak="$nvim.bak"
moc_config=$HOME"./moc/config"
moc_themes=$HOME"/.moc/themes/"
xinitrc=$HOME"/.xinitrc"
dwm="/usr/src/dwm"
vifm=$HOME"/.config/vifm"

function get_current_dotfiles {
	if [ -f "${alacritty}" ]; then
		cp "${alacritty}" "/home/brnco/code/dotfiles/alacritty/alacritty.yml"
	fi

	if [ -f "${bashrc}" ]; then
		cp "${bashrc}" "/home/brnco/code/dotfiles/bash/.bashrc"
	fi

	if [ -f "${nvim}" ]; then
		cp "${nvim}" "/home/brnco/code/dotfiles/nvim/init.vim"
	fi

    if [ -f "${moc_config}" ]; then
        cp "${moc_config}" "/home/brnco/code/dotfiles/moc"
    fi

    if [ -f "${moc_themes}" ]; then
        cp -R "${moc_themes}" "/home/brnco/code/dotfiles/moc/"
    fi

    if [ -f "${xinitrc}" ]; then
        cp "${xinitrc}" "/home/brnco/code/dotfiles"
    fi

    if [ -f "${dwm}" ]; then
        cp -R "${dwm}" "/home/brnco/code/dotfiles/dwm/"
    fi

    if [ -f "${vifm}" ]; then
        cp "${vifm}" "/home/brnco/code/dotfiles/vifm"
    fi
}

function send_repo_dotfiles {
	cp "/home/brnco/code/dotfiles/alacritty/alacritty.yml" "${alacritty}"
	cp "/home/brnco/code/dotfiles/bash/.bashrc" "${bashrc}"
	cp "/home/brnco/code/dotfiles/nvim/init.vim" "${nvim}"
    cp "/home/brnco/code/dotfiles/moc/config" "${moc_config}"
    cp -R "/home/brnco/code/dotfiles/moc/themes/" "${moc_themes}"
}
function backup_current_dotfiles {
	if [ ! -f "${alacrittybak}" ]; then
		cp "${alacritty}" "${alacrittybak}"
	fi

	if [ ! -f "${bashrcbak}" ]; then
		cp "${bashrc}" "${bashrcbak}"
	fi

	if [ ! -f "${nvimbak}" ]; then
		cp "${nvim}" "${nvimbak}"
	fi
}

get=false
send=false
echo "here"
while getopts "gs:" opt; do
    echo "there"
	case $opt in
		g) get=true ;;
		s) send=true ;;
		?) echo "error: option -$OPTARG does not exist"; exit ;;
	esac
done

if [ "$get" = true ];
then
	echo "get"
	get_current_dotfiles
fi

if [ "$send" = true ];
then
	echo "send"
	backup_current_dotfiles
	send_repo_dotfiles
fi
