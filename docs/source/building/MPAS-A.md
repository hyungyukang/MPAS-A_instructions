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
module load cray-netcdf-hdf5parallel
module load cray-parallel-netcdf
```
`NetCDF` and `Parallel NetCDF` are required modules. If those modules are not installed in the system, users need to install separately.

### Building PIO
```
cd ParallelIO
mkdir build
cd build
```

### Building MPAS-A model
```
mkdir build_mpas
cd build_mpas
cmake -DMPAS_CORES=atmosphere -S /path/to/MPAS-Model -B ./
cmake --build ./ -j 4
```
If successful, `bin/mpas_atmosphere` is compiled.

### Building MPAS-A initialization program
```
cmake -DMPAS_CORES=init_atmosphere -S /path/to/MPAS-Model -B ./
cmake --build ./ -j 4
```
If successful, `bin/mpas_init_atmosphere` is compiled.

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
