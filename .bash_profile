
if [ -f ~/.bashrc ]; then
    . ~/.bashrc
fi
setenv JOBSCHEDULER SLURM >>$HOME/.bashrc