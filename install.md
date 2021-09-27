# INSTALL GUIDE______________________________________________________

The requirements - install in order (Ubuntu 20.04)

-- needs C++ compiler
GCC is pre-installed on linux - to check:

$ g++ -v

tested on gcc 9.3.0

-- make should already be installed

-- needs cmake

https://cmake.org/download/

or:

$ sudo apt-get install cmake 

cmake version 3.16.3

-- Boost Libraries version 1.70 ot higher

sudo apt-get install libboost-all-dev

1.71 installed

-- mrc is optional -- could not get it working

	git clone https://github.com/mhekkel/mrc.git 
	cd mrc
	mkdir build
	cd build
	cmake ..
	cmake --install .



-- needs libcif++ 

https://github.com/PDB-REDO/libcifpp

	git clone https://github.com/PDB-REDO/libcifpp.git
	cd libcifpp
	mkdir build
	cd build
	cmake ..
	cmake --build . --config Release
	ctest -C Release
	cmake --install .


# DSSP Install
______________________________________________________________________________

1. https://swift.cmbi.umcn.nl/gv/dssp/DSSP_5.html
-- information guide

2. https://github.com/PDB-REDO/dssp

3. builld it

git clone https://github.com/PBD-REDO/dssp.git
cd dssp
mkdir build
cd build
cmake ..
cmake --build . --config Release
ctest -C Release
cmake --install .

## I had to manually download this 

-- added alias to ~/.bashrc
alias mkdssp='$HOME/.local/bin/mkdssp'
##

# A Quick Test

mkdssp --output-format=mmcif 6xmy.pdb
mkdssp --output-format=dssp 6xmy.pdb

