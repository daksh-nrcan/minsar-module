# MINSAR Module

Nutshell: This repo self contains all up-to-date code and commands for InSAR processing. Clone it with this command:


```bash 
cd ~/
git clone --recurse-submodules <repo-url> # so it pulls and initializs minsar, which's a submodule in this repo
```


### Conda Env Setup

Refer to the `README.md` in the `conda/` folder.


### Using MiNSAR

`minsar/minsar/bin/minsarApp.bash` is the entrypoint to use minsar
```bash
minsarApp.bash $TE/AlbertaSenAT49.template --dostep download --download-method slc
# no preprocessing step for Sentinel-1 SLCs according to minsarApp.bash, line 556-560
minsarApp.bash $TE/AlbertaSenAT49.template --dostep dem
minsarApp.bash $TE/AlbertaSenAT49.template --dostep jobfiles
```

##### Potential Issue

If it keeps saying `minsarApp.bash: command not found`, you probably didn't use `--recurse-submodules` when git cloning. Not to wrory, use this:

```bash
cd ~/minsar-module
git submodule update --init
```


##### Monitoring Download Step

This automatically updates with the space taken up by the zip files minsar is downloading in your folder:

```bash
# /* at end shows contents, remove and just shows space taken by overall folder
watch -n 5 du -sh /proc2/<USER>/scratch/<PROJECT_NAME>/SLC/* 
```

### Checking NASA Earthdata Status

If the download step is timing out, for both `asf.py` and `minsarApp.bash download`, use this [link](https://status.earthdata.nasa.gov/), and look at `Common Metadata Repository -> Search Integrity`. If it's yellow, that's probably the issue

Currently, `asf.py` works perfectly fine for download. Follow these steps:
1. Change 
```bash

```


### Sharing Files Between Laptop & HPC

`rsync` allows you to send and retrieve files between your two computers. Assuming you've configured the SSH as I explained in .ssh/README.md:

```bash
# second argument "source", third argument "recipient"

# leo2g to laptop
rsync -avzP leo2g:~/<folder>/file.ext ./ 
```

Note: If there's a newer version of minsar we need to 'update to'