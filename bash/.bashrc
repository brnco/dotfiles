neofetch

alias sudo='sudo '
alias ope='sudo $(history -p !!)'

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

eval "$(starship init bash)"
