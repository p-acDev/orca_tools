@echo off

set /p simulation_results_file="Enter your .sim path name for which you want clashing report: "

python  ./z_delta.py %simulation_results_file%

pause
