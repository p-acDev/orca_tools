# orca_tools
![GitHub release (latest by date)](https://img.shields.io/github/v/release/pacourbet/orca_tools?display_name=tag&style=plastic)
![Lines of code](https://img.shields.io/tokei/lines/github/pacourbet/orca_tools?style=plastic)
![GitHub code size in bytes](https://img.shields.io/github/languages/code-size/pacourbet/orca_tools?style=plastic)

A repo to store several orcaflex manip scripts

## models

### bathy
Just double click on the `bathy_mesh.bat`

### loadcases
- Just fill in the input load excel file in Orcaflex axis convention

| direction | X    | Y    | Z |
| --------- | ---- | ---- | - |
| 0         | 50   | \-81 | 0 |
| 20        | 85   | 49   | 0 |
| 30        | 60   | 39   | 0 |
| 50        | 78   | \-36 | 0 |
| 90        | \-83 | 74   | 0 |
| 140       | \-9  | \-34 | 0 |
| 180       | \-11 | 44   | 0 |
| 270       | \-72 | 12   | 0 |

- Just double click on the `launch_generate.bat`

> :warning: **The name of the sheet needs to be the same as the name in the orcaflex mdoel for the island**

## postreatment

### specific format
This script aims to extract the mooring line loads in the specific format:
Just double click on the `launch_posttreat.bat`

### 3 plot and line elevation
This script aims to do a 3D plot of mooring lines to check visually the line position and a heatmap which is 2D
Just double click on the `launch_plot.bat`

### clashing report
This scripts aims to provide a clashing line report with relative z position of each line Vs each line
It only checks the relevant lines, i.e, it checks only line side FRONT Vs line side RIGHT for instance.
In addition it only check the relative line elevation when XY of each line are close to each other
Just double click on the `launch_clashing_report.bat`
