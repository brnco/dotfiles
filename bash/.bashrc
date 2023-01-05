neofetch

alias sudo='sudo '
alias ope='sudo $(history -p !!)'
export PATH=/home/bec/.local/:$PATH

function clear() {
    command clear && neofetch
}
export -f clear

function ls() {
    command ls -1 "$@"
}
export -f ls

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
