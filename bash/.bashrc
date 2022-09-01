neofetch
# powerline-daemon -q
# POWERLINE_BASH_CONTINUATION=1
# POWERLINE_BASH_SELECT=1
# . /usr/share/powerline/bindings/bash/powerline.sh
alias sudo='sudo '
alias ope='sudo $(history -p !!)'
export HISTCONTROL=ignoreboth:erasedups
alias tree='tree -C'
function git() {
    if [[ $@ == "ass" ]]; then
        command git add .
    else
        command git "$@"
    fi
}
export -f git

if [ -z "${DISPLAY}" ] && [ "${XDG_VTNR}" -eq 1 ]; then
    exec startx
fi

eval "$(starship init bash)"
