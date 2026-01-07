# MPAS-A_instructions

This repository briefly introduces  

- MPAS-Atmosphere (MPAS-A) instructions
  - Building WRF Pre-processing System (WPS)
  - Buliding MPAS-A initialization program
  - Building MPAS-A model

(References: https://www2.mmm.ucar.edu/projects/mpas/tutorial/StAndrews2025/)

## 1. Building programs

### 1.1. Obtaining codes

#### 1.1.1. MPAS-A code
```
git clone https://github.com/MPAS-Dev/MPAS-Model.git
```
#### 1.1.2. WPS (WRF Pre-precessing System) code for initialization
```
git clone https://github.com/wrf-model/WPS.git
```

### 1.2. Building programs
#### 1.2.1. Loading required modules
```
module load cray-netcdf-hdf5parallel
module load cray-parallel-netcdf
```
`NetCDF` and `Parallel NetCDF` are required modules. If those modules are not loadable in your system, you need to install separately.

#### 1.2.2. Building MPAS-A model
```
mkdir build_mpas
cd build_mpas
cmake -S /path/to/MPAS-Model -B ./
cmake --build ./
```
If successful, `bin/mpas_atmosphere` is compiled.

#### 1.2.3. Building MPAS-A initialization program
```
cmake -DMPAS_CORES=init_atmosphere -S /path/to/MPAS-Model -B ./
cmake --build ./
```
If successful, `bin/mpas_init_atmosphere` is compiled.
#### 1.2.4. Building WPS for ungrib
```
cd WPS

./configure --nowrf --build-grib2-libs
```
There are more than 20 choces. Enter a selection based on your system configuration. `serial` is recommended for quick tests.
```
./compile ungrib
```


