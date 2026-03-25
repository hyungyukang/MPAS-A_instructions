# Download reanalysis data
In this instruction, global reanalysis data (e.g., FNL and ERA5) is used to initialize the model.

This instruction provides a Python script to download the Final (FNL) 0.25 degree global analysis data.

## Downloading FNL data
Reference: https://gdex.ucar.edu/datasets/d083003/

### Cloning this instruction
```
git clone https://github.com/hyungyukang/MPAS-A_instructions.git
cd MPAS-A_instructions/down_fnl_data

```

### Changing the date in `NCAR_FNL025.py`
Open `NCAR_FNL025.py` and change `startdate`, `starthour`, `enddate`, `endhour`.

In this instruction, we will simulation hurricane Helene (2024) initialized at `2024-09-25_00:00:00`.
To download one time frame, set the start time = end time. (note: FNL is provided 6 hourly.)
```
startdate = datetime.date(2024,9,25)
starthour = datetime.time(0, 0, 0)

enddate = datetime.date(2024,9,25)
endhour = datetime.time(0, 0, 0)
```

### Downloading FNL data (~450 MB)
```
python NCAR_FNL025.py
```
`gdas1.fnl0p25.2024092500.f00.grib2` will be downloaded.

<!--
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
-->
