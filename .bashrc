# paths maintenance
export PATH=$PATH:$HOME/brew/bin:/usr/local/opt/python:/Users/bcoates/devs

# update PATH for Google Cloud SDK
if [ -f '/Users/bcoates/brew/Cellar/google-cloud-sdk/path.bash.inc' ]; then . '/Users/bcoates/brew/Cellar/google-cloud-sdk/path.bash.inc'; fi

# enable shell command completion for Google Cloud SDK
if [ -f '/Users/bcoates/brew/Cellar/google-cloud-sdk/completion.bash.inc' ]; then . '/Users/bcoates/brew/Cellar/google-cloud-sdk/completion.bash.inc'; fi

# shell start
neofetch

# powerline
powerline daemon -q
POWERLINE_BASH_CONTINUATION=1
POWERLINE_BASH_SELECT=1
source /Users/bcoates/brew/lib/python3.9/site-packages/powerline/bindings/bash/powerline.sh

# aliases
alias sudo='sudo '
alias ope='sudo $(history -p !!)'
alias python="/Users/bcoates/brew/bin/python3"
function git(){
    if [[ $@ == "ass"  ]]; then
        command git add .
    else
        command git "$@"
    fi
}
export -f git
