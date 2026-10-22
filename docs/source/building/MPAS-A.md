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

### METIS (graph partition) & GKlib
```
git clone https://github.com/KarypisLab/METIS.git
cd METIS
git clone https://github.com/KarypisLab/GKlib.git
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

### Building METIS
Reference: https://karypislab.github.io/METIS/
- METIS is serial graph partitioning software for distributed MPAS-A runs.
- GKlib installation is required.

#### Building GKlib
```
cd METIS/GKlib
make config cc=gcc shared=1 prefix=/path/to/METIS/install
make
make install
```
`cc` must be set as the C compiler executable.

#### Building METIS
```
cd METIS/
make config cc=gcc prefix=/path/to/METIS/install
```

If successful, `METIS/install/bin/gpmetis` is compiled.



<!-------------------------------------------------------------!>

## Building in offline machines



If your offline machine already has **MPICH, NetCDF, NetCDF-Fortran, and Parallel-NetCDF** installed, the main challenge is not the libraries themselves. Instead, recent versions of MPAS-Atmosphere attempt to download additional physics source code and lookup tables during compilation.

For **MPAS-Atmosphere v8.4.1**, the build process uses `manage_externals` to obtain **MMM-physics** and **UGWP**, while `checkout_data_files.sh` retrieves WRF physics lookup tables.

See the [MPAS v8.4.1 Externals configuration](https://github.com/MPAS-Dev/MPAS-Model/blob/v8.4.1/src/core_atmosphere/Externals.cfg).

The recommended approach is:

1. Prepare a **complete MPAS source tree** on a machine with internet access.
2. Transfer the complete source tree to the offline machine.
3. Compile MPAS using the libraries already installed on the offline machine.

### 1. Prepare MPAS on a machine with internet access

#### 1.1. Download MPAS-Atmosphere

Clone the MPAS v8.4.1 repository:

```bash
git clone --branch v8.4.1 https://github.com/MPAS-Dev/MPAS-Model.git MPAS-Model-8.4.1

cd MPAS-Model-8.4.1
```

#### 1.2. Download external physics packages

MPAS v8.4.1 requires two external atmosphere physics packages:

- **MMM-physics**
- **GSL_UGWP**

These are defined in the [Externals.cfg](https://github.com/MPAS-Dev/MPAS-Model/blob/v8.4.1/src/core_atmosphere/Externals.cfg) file.

Download these packages before transferring the source tree:

```bash
cd src/core_atmosphere/physics

../tools/manage_externals/checkout_externals \
    --externals ../Externals.cfg
```

After successful checkout, the following directories should exist:

```text
physics_mmm/
physics_noaa/UGWP/
```

Verify that the required Makefiles are available:

```bash
ls physics_mmm/Makefile.mpas
ls physics_noaa/UGWP/Makefile
```

**Note:** The MPAS physics Makefile normally executes the `checkout_externals` command automatically during compilation. Therefore, transferring only the basic MPAS GitHub source archive is insufficient for an offline build.

See the [MPAS physics Makefile](https://github.com/MPAS-Dev/MPAS-Model/blob/v8.4.1/src/core_atmosphere/physics/Makefile).

#### 1.3. Download WRF physics lookup tables

Download the required WRF physics lookup tables:

```bash
./checkout_data_files.sh
```

Verify the downloaded files:

```bash
ls physics_wrf/files/
```

The directory should contain files such as:

```text
COMPATIBILITY
*.TBL
*DATA*
```

These files must be located under:

```text
src/core_atmosphere/physics/physics_wrf/files/
```

The MPAS `checkout_data_files.sh` script explicitly documents this directory for manually installing lookup tables.

See [checkout_data_files.sh](https://github.com/MPAS-Dev/MPAS-Model/blob/v8.4.1/src/core_atmosphere/physics/checkout_data_files.sh).

#### 1.4. Create an offline source bundle

Return to the parent directory of the MPAS source tree:

```bash
cd ../../../..
```

Create a compressed archive containing the complete MPAS source tree, including the external physics packages and lookup tables:

```bash
tar czf MPAS-Model-8.4.1-offline.tar.gz MPAS-Model-8.4.1
```

Transfer the archive to the offline machine using an appropriate method, such as:

- USB storage
- SCP through an internal network
- Another approved file-transfer mechanism

### 2. Prepare MPAS on the offline machine

#### 2.1. Extract the source bundle

Extract the transferred archive:

```bash
tar xzf MPAS-Model-8.4.1-offline.tar.gz

cd MPAS-Model-8.4.1
```

#### 2.2. Disable automatic external repository checkout

Because the external physics packages have already been downloaded, the network-dependent `manage_externals` invocation can be disabled.

Open the following file:

```text
src/core_atmosphere/physics/Makefile
```

Find the line:

```makefile
./../tools/manage_externals/checkout_externals --externals ./../Externals.cfg
```

Comment out this command:

```makefile
# ./../tools/manage_externals/checkout_externals --externals ./../Externals.cfg
```

This modification prevents the build system from attempting to synchronize external repositories during compilation.

See the [MPAS physics Makefile](https://github.com/MPAS-Dev/MPAS-Model/blob/v8.4.1/src/core_atmosphere/physics/Makefile).

**Note:** You normally do not need to disable the following command:

```bash
./checkout_data_files.sh
```

The script first checks whether compatible lookup tables already exist. If compatible files are present, it exits without downloading anything.

See [checkout_data_files.sh](https://github.com/MPAS-Dev/MPAS-Model/blob/v8.4.1/src/core_atmosphere/physics/checkout_data_files.sh).

### 3. Configure installed libraries

MPAS requires compatible installations of MPI, NetCDF-C, NetCDF-Fortran, and Parallel-NetCDF.

For example, suppose the following libraries are already installed:

```text
/opt/mpich
/opt/netcdf
/opt/pnetcdf
```

#### 3.1. Set environment variables

Configure the library paths:

```bash
export PATH=/opt/mpich/bin:$PATH

export NETCDF=/opt/netcdf
export PNETCDF=/opt/pnetcdf
```

If NetCDF-C and NetCDF-Fortran are installed in separate directories, configure both:

```bash
export NETCDF=/opt/netcdf-c
export NETCDFF=/opt/netcdf-fortran
```

If necessary, add the libraries to `LD_LIBRARY_PATH`:

```bash
export LD_LIBRARY_PATH=$NETCDF/lib:$PNETCDF/lib:$LD_LIBRARY_PATH
```

For separate NetCDF-C and NetCDF-Fortran installations:

```bash
export LD_LIBRARY_PATH=$NETCDF/lib:$NETCDFF/lib:$PNETCDF/lib:$LD_LIBRARY_PATH
```

The MPAS build system uses the `NETCDF` and `PNETCDF` environment variables to locate required headers and libraries.

See the [MPAS Makefile](https://github.com/MPAS-Dev/MPAS-Model/blob/v8.4.1/Makefile).

#### 3.2. Verify compiler and MPI configuration

Check the available compilers:

```bash
which gcc
which gfortran
which mpicc
which mpif90
which mpicxx
```

Verify the MPI compiler configuration:

```bash
mpicc -show
mpif90 -show
```

Check the NetCDF installations:

```bash
nc-config --version
nf-config --version
```

If supported by your Parallel-NetCDF installation:

```bash
pnetcdf-config --version
```

**Important:** MPICH, NetCDF-C, NetCDF-Fortran, and Parallel-NetCDF must be compatible with the same compiler and MPI environment.

Mixing libraries compiled with incompatible compiler or MPI implementations may cause linking errors or runtime failures.

### 4. Configure MPAS I/O using SMIOL

MPAS supports two I/O configurations:

- **PIO:** Parallel I/O library
- **SMIOL:** Simple MPAS I/O Layer

If Parallel-NetCDF is already installed, the external PIO library is not required.

To use the bundled **SMIOL** library, make sure the `PIO` environment variable is unset:

```bash
unset PIO
```

MPAS uses its bundled SMIOL implementation when `PIO` is not defined.

See the [MPAS Makefile](https://github.com/MPAS-Dev/MPAS-Model/blob/v8.4.1/Makefile).

The recommended configuration is:

```text
             MPICH
               |
       +-------+-------+
       |               |
    NetCDF       Parallel-NetCDF
                       |
                     SMIOL
                       |
                MPAS-Atmosphere
```

This configuration avoids requiring an additional external PIO installation.

### 5. Compile init_atmosphere

The `init_atmosphere` core is used to generate initial conditions and prepare input data for MPAS-Atmosphere.

#### 5.1. Build the initialization core

Using GNU compilers:

```bash
make -j 4 gfortran CORE=init_atmosphere
```

Alternatively, use additional parallel compilation processes:

```bash
make -j 8 gfortran CORE=init_atmosphere
```

A successful build produces the executable:

```text
init_atmosphere_model
```

The executable name is defined in the [init_atmosphere build configuration](https://github.com/MPAS-Dev/MPAS-Model/blob/v8.4.1/src/core_init_atmosphere/build_options.mk).

#### 5.2. Verify the executable

Check that the executable exists:

```bash
ls -lh init_atmosphere_model
```

Verify its shared library dependencies:

```bash
ldd init_atmosphere_model
```

Make sure there are no missing shared libraries.

### 6. Compile MPAS-Atmosphere

After successfully compiling `init_atmosphere`, compile the MPAS-Atmosphere core.

#### 6.1. Build the atmosphere core

Using GNU compilers:

```bash
make -j 4 gfortran CORE=atmosphere
```

Or increase the number of parallel build processes:

```bash
make -j 8 gfortran CORE=atmosphere
```

A successful build produces:

```text
atmosphere_model
```

The executable name is defined in the [atmosphere build configuration](https://github.com/MPAS-Dev/MPAS-Model/blob/v8.4.1/src/core_atmosphere/build_options.mk).

#### 6.2. Verify the executable

Check that the executable exists:

```bash
ls -lh atmosphere_model
```

Verify its shared library dependencies:

```bash
ldd atmosphere_model
```

Make sure that all required shared libraries can be located.

### 7. Verify the final MPAS installation

After successfully completing both builds, the MPAS source directory should have a structure similar to:

```text
MPAS-Model-8.4.1/
├── atmosphere_model
├── init_atmosphere_model
├── namelist.atmosphere
├── streams.atmosphere
├── namelist.init_atmosphere
├── streams.init_atmosphere
├── src/
│   └── core_atmosphere/
│       └── physics/
│           ├── physics_mmm/
│           ├── physics_noaa/
│           │   └── UGWP/
│           └── physics_wrf/
│               └── files/
│                   ├── COMPATIBILITY
│                   ├── *.TBL
│                   └── *DATA*
└── ...
```

The two primary executables are:

| Executable | Description |
|------------|-------------|
| `init_atmosphere_model` | Initializes MPAS-Atmosphere input data and initial conditions |
| `atmosphere_model` | Runs MPAS-Atmosphere simulations |

If both executables are generated successfully and their shared library dependencies are satisfied, the MPAS-Atmosphere build is complete.

**Note:** Successful compilation does not guarantee that all runtime input files are available. Additional mesh files, initial conditions, forcing data, and physics datasets may be required depending on the simulation configuration.


<!-------------------------------------------------------------!>
