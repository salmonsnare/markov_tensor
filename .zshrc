source /home/tadachikaoki/antigen.zsh


# history
# refference: https://masutaka.net/chalow/2014-05-18-2.html
HISTFILE=$HOME/.zhistory
HISTSIZE=1000000
SAVEHIST=1000000
setopt extended_history
alias hall="history -E -i 1"
autoload history-search-end
zle -N history-beginning-search-backward-end history-search-end
zle -N history-beginning-search-forward-end history-search-end
bindkey "^p" history-beginning-search-backward-end
bindkey "^n" history-beginning-search-forward-end

# Load the oh-my-zsh's library.
antigen use oh-my-zsh

# Bundles from the default repo (robbyrussell's oh-my-zsh).
antigen bundle git
antigen bundle heroku
antigen bundle pip
antigen bundle lein
antigen bundle command-not-found

# Syntax highlighting bundle.
antigen bundle zsh-users/zsh-syntax-highlighting

# Load the theme.
antigen theme robbyrussell

# auto completion
antigen bundle zsh-users/zsh-completion

# Tell Antigen that you're done.
antigen apply
