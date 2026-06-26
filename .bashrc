# ~/.bashrc: executed by bash(1) for non-login shells.
# see /usr/share/doc/bash/examples/startup-files (in the package bash-doc)
# for examples

# If not running interactively, don't do anything
case $- in
    *i*) ;;
      *) return;;
esac

# don't put duplicate lines or lines starting with space in the history.
# See bash(1) for more options
HISTCONTROL=ignoreboth

# append to the history file, don't overwrite it
shopt -s histappend

# for setting history length see HISTSIZE and HISTFILESIZE in bash(1)
HISTSIZE=1000
HISTFILESIZE=2000

# check the window size after each command and, if necessary,
# update the values of LINES and COLUMNS.
shopt -s checkwinsize

# If set, the pattern "**" used in a pathname expansion context will
# match all files and zero or more directories and subdirectories.
#shopt -s globstar

# make less more friendly for non-text input files, see lesspipe(1)
[ -x /usr/bin/lesspipe ] && eval "$(SHELL=/bin/sh lesspipe)"

# set variable identifying the chroot you work in (used in the prompt below)
if [ -z "${debian_chroot:-}" ] && [ -r /etc/debian_chroot ]; then
    debian_chroot=$(cat /etc/debian_chroot)
fi

# set a fancy prompt (non-color, unless we know we "want" color)
case "$TERM" in
    xterm-color|*-256color) color_prompt=yes;;
esac

# uncomment for a colored prompt, if the terminal has the capability; turned
# off by default to not distract the user: the focus in a terminal window
# should be on the output of commands, not on the prompt
#force_color_prompt=yes
# If this is an xterm set the title to user@host:dir

# enable color support of ls and also add handy aliases
# colored GCC warnings and errors
#export GCC_COLORS='error=01;31:warning=01;35:note=01;36:caret=01;32:locus=01:quote=01'

# some more ls aliases
alias ll='ls -alF'
alias la='ls -A'
alias l='ls -CF'

# Add an "alert" alias for long running commands.  Use like so:
#   sleep 10; alert
alias alert='notify-send --urgency=low -i "$([ $? = 0 ] && echo terminal || echo error)" "$(history|tail -n1|sed -e '\''s/^\s*[0-9]\+\s*//;s/[;&|]\s*alert$//'\'')"'

# Alias definitions.
# You may want to put all your additions into a separate file like
# ~/.bash_aliases, instead of adding them here directly.
# See /usr/share/doc/bash-doc/examples in the bash-doc package.

if [ -f ~/.bash_aliases ]; then
    . ~/.bash_aliases
fi

# enable programmable completion features (you don't need to enable
# this, if it's already enabled in /etc/bash.bashrc and /etc/profile
# sources /etc/bash.bashrc).
############################################################
##### MinSAR Dec, 14th 2024

# User specific aliases and functions
shopt -s expand_aliases

modules_shell="bash"
[ -n module ] && module purge
umask 007

export USER_PREFERRED=draval
module purge

export CPL_ZIP_ENCODING=UTF-8
export WORK2=/home/yjiang/

alias source_environment='cd $RSMASINSAR_HOME; export PATH=/bin; unset PYTHONPATH; source ~/minsar-module/accounts/platforms_defaults.bash; source ~/minsar-moduleaccounts/environment.bash; export PATH=$ISCE_STACK/topsStack:$PATH; cd -;'

# Modified for ALOS March 6 2025
#alias source_environment='cd $RSMASINSAR_HOME; export PATH=/bin; unset PYTHONPATH; source ~/accounts/platforms_defaults.bash; source ~/accounts/environment.bash; export PATH=${PATH}:${ISCE_STACK}/stripmapStack; source ~/accounts/alias.bash; source ~/accounts/login_alias.bash; cd -;'

alias s.bw2='export RSMASINSAR_HOME=${WORK2%/*}/stampede3/code/rsmas_insar; source_environment'
alias s.bw2o='export RSMASINSAR_HOME=${WORK2%/*}/stampede3/code2/rsmas_insar; source_environment'

export PATH="$HOME/bin:$PATH"
export PATH="$HOME/bin:$PATH"
alias wget="$HOME/bin/wget"

conda activate minsar
