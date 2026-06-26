# Conda Environment Setup

I'm using:
- **miniforge** (mini conda installer)
- **mamba** (fast conda solver) 

Why not just a .venv? I've learned not to trust plain pip, even in venvs lol.

I partly used [this repo](https://github.com/yunjunz/conda-envs/tree/main) as inspiration

## 1. Install Miniforge

Miniforge bundles conda + conda-forge as the default channel. Download and run the installer:

```bash
# Linux
wget https://github.com/conda-forge/miniforge/releases/latest/download/Miniforge3-Linux-x86_64.sh
bash Miniforge3-Linux-x86_64.sh -b -p ~/miniforge # edit where you want to place miniforge, AND REMEMBER IT FOR NEXT STEP!

rm Miniforge3-Linux-x86_64.sh # delete after install, not useful
```

Then initialize conda for your shell and restart:

```bash
# make sure actual filepath you downloaded miniforge above!
~/miniforge3/bin/conda init bash
# close and reopen terminal
```
Turns out Ana/Miniconda has license restrictions for institutional use, miniforge open source, which's why I think the repo I mentioned uses it.

## 2. Install mamba

Mamba = conda command subsitute.
```bash
# makes 'base' env with mamba, installed by conda-forge channel
# mamba's default channel is conda-forge anyways, which iirc has much more stuff available
source ~/miniforge/etc/profile.d/conda.sh # change to correct path
conda install -n base -c conda-forge mamba
```

After this, use `mamba` anywhere you'd type `conda install` or `conda create`.

**Note**: You can NOT use `mamba activate <env-name>`!! Must use `conda activate`, I'm not too sure why though

---

## 3. Create the project environment

```bash
# first time setup only!
mamba env create -f conda/environment.yml
conda activate minsar # not mamba activate!
```

### Sharing Minsar Env from Laptop to HPC

I was having trouble building the minsar env on the HPC, during the solver step, so I just zipped it and sent it over rsync as follows:

```bash
# On laptop
conda activate base # if you have starship like me, wont say (base), but use conda env list to confirm
mamba install -n base conda-pack  # -n base just means you don't really need to enter env to install
conda pack -n minsar -o /tmp/minsar.tar.gz

# rsync to HPC (dry run first)
rsync -avn /tmp/minsar.tar.gz leo2g:/home/draval/
rsync -av  /tmp/minsar.tar.gz leo2g:/home/draval

rm -f /tmp/minsar.tar.gz # if successful


# On HPC
# pulls conda 'basepath' sourced from .bashrc
mkdir -p $(conda info --base)/envs/minsar # I had trouble since I had a non-interactive shell from VSCode SSH, if you have trouble just put absolute path ~/apps/miniforge, or source ~/.bashrc
tar -xzf /home/draval/minsar.tar.gz -C $(conda info --base)/envs/minsar
conda activate minsar
conda-unpack  # fixes hardcoded paths

rm -f ~/minsar.tar.gz # if successful
```

## 4. Changes to Env

Let's say it turns out a new package is necessary. If one of us just installs it in the mamba environment, great, it works, but how will the rest of us replicate it?
```bash
# add package
conda activate minsar && mamba install numpy

# update environment.yml
mamba env export --from-history > conda/environment.yml # then push it to the repo!!

# if you want to 'pull it forward'/rebase the env
mamba env update -f conda/environment.yml --prune
```


## Notes

- The environment name is `minsar` (set in `environment.yml`).
- Always activate the environment before running scripts: `conda activate minsar`.
- To deactivate: `conda deactivate`.
