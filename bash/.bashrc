# # # set environment variables
export TERM="xterm-256color"			#get the nice colors you like
export HISTCONTROL=ignoredups:erasedups		#no duplicate entries
export EDITOR="vim"

# # # aliases
alias sudo='sudo '
alias ope='sudo $(history -p !!)'

# # # functions

function git() {
if [[ $@ == "ass" ]]; then
        command git add .
    else
        command git "$@"
    fi
}
export -f git

# # # launch
neofetch
eval "$(starship init bash)"
