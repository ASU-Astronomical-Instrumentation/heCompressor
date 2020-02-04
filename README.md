## CryoCompressor ##


### Intended use ###
For use with a Sumitomo (SHI) Cryogenics of America, INC.
F-70L Helium Compressor. The user should fully awknowledge that this software is not suitable for maitenance, or diagnoses of this compressor. There is No warranty of any kind and No guarintee for fitness of use regardless of application.

### Python Enviornment ###
Uses Anaconda 3 to manage the python virtual enviornment.
The easiest method to ensure everything works is to setup a conda enviornment.

Clone / download the repository and extract it to your desired destination.
Open a terminal in the destination folder and run:
```bash
conda env create -f env/environment.yml
```

* You can verify that the enviornment was created properly using
```bash
conda env list
```

Afterwards, activate the enviornment and run the program.
```bash
conda activate cryocomp; python gui.py
```




### Legal ###
This software is custom and not endorced, licensed, or affiliated with (SHI) Cryogenics of America.
