# Download MPAS-A mesh
This instruction uses a quasi-uniform 120-km mesh provided by NCAR.

## Download mesh using wget
Reference: https://mpas-dev.github.io/atmosphere/atmosphere_meshes.html

```
mkdir base_mesh
cd base_mesh
wget https://www2.mmm.ucar.edu/projects/mpas/atmosphere_meshes/x1.40962.tar.gz
tar xzf x1.40962.tar.gz
```
There are several files after untar. `x1.40962.grid.nc` is the base mesh file, `x1.40962.graph.info` is the graph partition file, and `x1.40962.graph.info.part.XX` files are partitioned graph files for XX cpu cores.
