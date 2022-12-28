neofetch
# powerline-daemon -q
# POWERLINE_BASH_CONTINUATION=1
# POWERLINE_BASH_SELECT=1
# . /usr/share/powerline/bindings/bash/powerline.sh
alias sudo='sudo '
alias ope='sudo $(history -p !!)'
#export $TERM=xterm-256color
export PATH=/home/bcoates/.local/bin:$PATH
export HISTCONTROL=ignoreboth:erasedups
function clear() {
    command clear && neofetch
}
export -f clear

function git() {
    if [[ $@ == "ass" ]]; then
        command git add .
    else
        command git "$@"
    fi
}
export -f git

if [[ -z $DISPLAY ]] && [[ $(tty) = /dev/tty1 ]]; then
    startx
fi

eval "$(starship init bash)"
