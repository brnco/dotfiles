#!/bin/bash
echo "starting"
dotfiles=$HOME"/code/dotfiles/"
alacritty=$HOME"/.config/alacritty/"
alacritty_git=$dotfiles"alacritty/"
bashrc=$HOME"/.bashrc"
bashrc_git=$dotfiles"bash/"
nvim=$HOME"/.config/nvim/"
nvim_git=$dotfiles"nvim/"
moc=$HOME"./moc/"
moc_git=$dotfiles"moc/"
xinitrc=$HOME"/.xinitrc"
xinitrc_git=$dotfiles
dwm="/usr/src/dwm/"
dwm_git=$dotfiles"dwm/"
vifm=$HOME"/.config/vifm/"
vifm_git=$dotfiles"vifm/"
powerline=$HOME"/.config/powerline/"
powerline_git=$dotfiles"powerline/"
function get_current_dotfiles {
	if [ -f "${alacritty}" ]; then
		cp -R "${alacritty}" "${alacritty_git}"
	fi

	if [ -f "${bashrc}" ]; then
		cp "${bashrc}" "${bashrc_git}"
	fi

	if [ -f "${nvim}" ]; then
		cp -R "${nvim}" "${nvim_git}"
	fi

    if [ -f "${moc}" ]; then
        cp -R "${moc}" "${moc_git}"
    fi

    if [ -f "${powerline}" ]; then
        cp -R "${powerline}" "${powerline_git}"
    fi

    if [ -f "${xinitrc}" ]; then
        cp "${xinitrc}" "${xinitrc_git}"
    fi

    if [ -f "${dwm}" ]; then
        cp -R "${dwm}" "${dwm_git}"
    fi

    if [ -f "${vifm}" ]; then
        cp -R "${vifm}" "${vifm_git}"
    fi
}

function send_repo_dotfiles {
	cp "/home/brnco/code/dotfiles/alacritty/alacritty.yml" "${alacritty}"
	cp "/home/brnco/code/dotfiles/bash/.bashrc" "${bashrc}"
	cp "/home/brnco/code/dotfiles/nvim/init.vim" "${nvim}"
    cp "/home/brnco/code/dotfiles/moc/config" "${moc_config}"
    cp -R "/home/brnco/code/dotfiles/moc/themes/" "${moc_themes}"
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
	send_repo_dotfiles
fi
