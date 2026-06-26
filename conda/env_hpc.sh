#!/usr/bin/env bash
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

export MINSAR_HOME="$REPO_ROOT/minsar"
export SCRATCHDIR="/proc2/$USER/scratch"
export SAMPLESDIR="$REPO_ROOT/templates"
export TEMPLATES="$SAMPLESDIR"
export TE="$SAMPLESDIR"
export WORKDIR="$SCRATCHDIR"
export NETRC="$REPO_ROOT/.netrc"
export PLATFORM_NAME=mac
export QUEUENAME=skx
export JOBSCHEDULER=SLURM

export ISCE_STACK="$CONDA_PREFIX/share/isce2"
export ISCE_HOME="$CONDA_PREFIX/lib/python3.10/site-packages/isce"
export SENTINEL_ORBITS="$SCRATCHDIR/orbits"
export SENTINEL_AUX="$SCRATCHDIR/aux"

export PATH="$MINSAR_HOME/minsar:$PATH"
export PATH="$MINSAR_HOME/minsar/bin:$PATH"
export PATH="$MINSAR_HOME/minsar/scripts:$PATH"
export PATH="$MINSAR_HOME/minsar/src/minsar/cli:$PATH"
export PATH="$MINSAR_HOME/minsar/utils:$PATH"
export PATH="$ISCE_STACK/topsStack:$PATH"
# export PATH="$REPO_ROOT/scripts:$PATH"
export PYTHONPATH="$ISCE_HOME/components:$ISCE_STACK:$MINSAR_HOME:${PYTHONPATH:-}"

echo "HPC env active:"
echo "  MINSAR_HOME  = $MINSAR_HOME"
echo "  SCRATCHDIR   = $SCRATCHDIR"
echo "  SAMPLESDIR   = $SAMPLESDIR"
echo "  WORKDIR      = $WORKDIR"
echo "  NETRC        = $NETRC"