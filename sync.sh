#!/bin/bash
alacritty=$HOME"/.config/alacritty/alacritty.yml"
alacrittybak="$alacritty.bak"
bashrc=$HOME"/.bashrc"
bashrcbak="$bashrc.bak"
nvim=$HOME"/.config/nvim/init.vim"
nvimbak="$nvim.bak"

function get_current_dotfiles {
	if [ -f "${alacritty}" ]; then
		cp "${alacritty}" "/home/brnco/devs/dotfiles/alacritty/alacritty.yml"
	fi

	if [ -f "${bashrc}" ]; then
		cp "${bashrc}" "/home/brnco/devs/dotfiles/bash/.bashrc"
	fi

	if [ -f "${nvim}" ]; then
		cp "${nvim}" "/home/brnco/devs/dotfiles/nvim/init.vim"
	fi
}

function send_repo_dotfiles {
	cp "/home/brnco/devs/dotfiles/alacritty/alacritty.yml" "${alacritty}"
	cp "/home/brnco/devs/dotfiles/bash/.bashrc" "${bashrc}"
	cp "/home/brnco/devs/dotfiles/nvim/init.vim" "${nvim}"
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

while getopts "gs:" opt; do
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
