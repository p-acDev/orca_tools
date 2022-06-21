@echo off

set /p simulation_results_file="Enter your .sim path name for which you want plot: "

python  ./plot_line_elevation.py %simulation_results_file%

pause
