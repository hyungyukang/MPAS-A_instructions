# MPAS-A_instructions

This repository briefly introduces how to run MPAS-Atmosphere (MPAS-A) and create initial conditions using reanalysis data.

- MPAS-Atmosphere (MPAS-A) instructions
  - Building WRF Pre-processing System (WPS)
  - Buliding MPAS-A initialization program
  - Building MPAS-A model


(For more details, please refer to the MPAS Tutorial practice guide: https://www2.mmm.ucar.edu/projects/mpas/tutorial/StAndrews2025/)

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
`NetCDF` and `Parallel NetCDF` are required modules. If those modules are not installed in the system, users need to install separately.

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
There are more than 20 choces. Enter a selection based on the system configuration. `serial` is recommended for quick tests.
```
./compile ungrib
```

## 2. Creating model initial conditions using reanalysis data
The ERA5 reanalysis data is provided in this instruction as an example.

https://1drv.ms/u/c/b751c0f0fb0cd990/IQD2Ydn7jOs-QZSjG4AVeVHzAZewZyg60SMTnSu79ympxmQ?e=vncMiQ

### 2.1. Generating intermediate files from reanalysis GRIB data
#### 2.1.1. Linking the reanalysis data
```
cd WPS
./link_grib.csh /path/to/era5_all_2021082700.grb
```
#### 2.1.2. Changing the data in `namelist.wps` accordingly
Open `namelist.wps` and change `start_date` and `end_date` accordingly.
For the current example data, set as follows:
```
 start_date = '2021-08-27_00:00:00',
 end_date   = '2021-08-27_00:00:00',
```
#### 2.1.3. Linking `Vtable` for the reanalysis data
The current ERA5 reanalysis data uses `ungrib/Variable_Tables/Vtable.ERA-interim.pl`.
```
ln -fs ./ungrib/Variable_Tables/Vtable.ERA-interim.pl ./Vtable
```
#### 2.1.4. Running `ungrib.exe`
```
./ungrib.exe
```
Successful running will create the intermediate file `FILE:2021-08-27_00`.

For more details on WPS, please refer to WPS user guide (https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/wps.html).

### 2.2. Creating MPAS-A initial conditions
#### 2.2.1. Generating the static file from the base mesh

To obtain base meshes, please visit the NCAR MPAS-A mesh download section (https://mpas-dev.github.io/atmosphere/atmosphere_meshes.html)

#### 2.2.2. Creating the initial condition


## 3. Running MPAS-A

## 4. Vizualization
