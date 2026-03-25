# Download reanalysis data
In this instruction, global reanalysis data is used to initialize the model.

## Download FNL data
Reference: https://gdex.ucar.edu/datasets/d083003/

### Linking the reanalysis data
```
cd WPS
./link_grib.csh /path/to/era5_all_2021082700.grb
```
### Changing the data in `namelist.wps` accordingly
Open `namelist.wps` and change `start_date` and `end_date` accordingly.
For the current example data, set as follows:
```
 start_date = '2021-08-27_00:00:00',
 end_date   = '2021-08-27_00:00:00',
```
### Linking `Vtable` for the reanalysis data
The current ERA5 reanalysis data uses `ungrib/Variable_Tables/Vtable.ERA-interim.pl`.
```
ln -fs ./ungrib/Variable_Tables/Vtable.ERA-interim.pl ./Vtable
```
### Running `ungrib.exe`
```
./ungrib.exe
```
Successful running will create the intermediate file `FILE:2021-08-27_00`.

For more details on WPS, please refer to WPS user guide (https://www2.mmm.ucar.edu/wrf/users/wrf_users_guide/build/html/wps.html).

## Creating MPAS-A initial conditions
### Generating the static file from the base mesh

To obtain base meshes, please visit the NCAR MPAS-A mesh download section (https://mpas-dev.github.io/atmosphere/atmosphere_meshes.html)

### Creating the initial condition
