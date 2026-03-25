# Building programs

## Obtaining codes

### MPAS-A code
```
git clone https://github.com/MPAS-Dev/MPAS-Model.git
```
### WPS (WRF Pre-precessing System) code for initialization
```
git clone https://github.com/wrf-model/WPS.git
```

### PIO (Parallel IO)
```
git clone https://github.com/NCAR/ParallelIO.git
```

## Building programs
GNU compiler is recommended for a quick test.

### Loading required modules
```
module load cray-hdf5
module load cray-netcdf
module load cray-parallel-netcdf
```
`NetCDF` and `Parallel NetCDF` are required modules. If those modules are not installed in the system, users need to install separately.

### Building PIO
Reference: https://ncar.github.io/ParallelIO/install.html
```
cd ParallelIO
mkdir build
cd build
CC=cc FC=ftn cmake -DCMAKE_INSTALL_PREFIX=../install -DPIO_ENABLE_TESTS=OFF -DPIO_ENABLE_TIMING=OFF ../
```
`CC` and `FC` must be set as compiler's executables.
```
make -j 4
make install
```
Set PIO as an environmetal variable
```
export PIO=/path/to/PIO/install
export PIO_PREFIX=/path/to/PIO/install
export PIO_INCLUDE_DIR=/path/to/PIO/install/include
```

### Building MPAS-A model & initialization program
```
cd MPAS-Model
mkdir build_mpas
cd build_mpas
cmake -DMPAS_CORES="init_atmosphere;atmosphere" -DMPAS_USE_PIO=ON -DPIO_PREFIX=$PIO_PREFIX -DPIO_INCLUDE_DIR=$PIO_INCLUDE_DIR -S ../ -B ./
cmake --build ./ -j 4
```
If successful, `bin/mpas_atmosphere` and `bin/mpas_init_atmosphere` are compiled. It is necessary to build tables for physics parameterization when compiling the model first time or changing the compiler. This will take a few minutes.
```
./bin/mpas_atmosphere_build_tables
cd MPAS/core_atmosphere
ln -fs /path/to/MPAS-Model/build_mpas/*.DBL ./
```

### Building WPS for ungrib
```
cd WPS

./configure --nowrf --build-grib2-libs
```
There are more than 20 choces. Enter a selection based on the system configuration. `serial` is recommended for quick tests.
```
./compile ungrib
```

<!-- 1195  cmake -DMPAS_CORES="init_atmosphere;atmosphere"  -S ../MPAS-Model -B ./
 1196  cmake --build ./ -j 4-->
