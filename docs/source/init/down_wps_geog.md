# Download WPS GEOG data
The WPS geographical static data is required to generate MPAS-A static field.

## Download data using wget
Reference: https://www2.mmm.ucar.edu/wrf/users/download/get_sources_wps_geog.html
Note: ~29G Uncompressed (2.6G Compressed)

```
cd /path/to/MPAS-Model
wget https://www2.mmm.ucar.edu/wrf/src/wps_files/geog_high_res_mandatory.tar.gz
```

## Untar the GEOG file
```
tar xzf geog_high_res_mandatory.tar.gz
```
Untar of the GEOG file will take some time.
