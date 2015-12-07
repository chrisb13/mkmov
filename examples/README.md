# Example 1 basic

```Bash
git clone https://github.com/chrisb13/mkmov.git
cd mkmov
mkmov.py zos examples/cordex24-ERAI01_1d_20040101_20040112_grid_T_2D.nc
```

# Example 2 with arguments
```Bash
git clone https://github.com/chrisb13/mkmov.git
cd mkmov
mkmov.py --min -1 --max 1 --preview -o ./zos_example.mov zos examples/cordex24-ERAI01_1d_20040101_20040112_grid_T_2D.nc
```
