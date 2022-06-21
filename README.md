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
Just double clikc on the `launch_posttreat.bat`
