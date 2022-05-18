@echo off

echo ######################
echo          INFO
echo ######################
echo The only restrictions are as following:
echo    - use 'initialposition' for static model name
echo    - you have to set your model result name like this: whatever_you_like_{WATERLEVEL}_{DIRECTIONdeg}.sim
echo.
echo Below is an ewample of valid naming:
echo    EDF_duopicth_V5_PMO_LWL_145deg.sim
echo ######################
echo.

set /p simulation_results_folder="Enter your path folder with .sim files: "
set /p output_file_path_name="Enter the path name of your output excel: "
set /p water_levels="Enter your wtaer levels with space between: "
echo 

python  ./extract_results.py %simulation_results_folder% %output_file_path_name% %water_levels%

pause