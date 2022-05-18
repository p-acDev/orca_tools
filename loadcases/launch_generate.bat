@echo off

echo ######################
echo          INFO
echo ######################
echo The only restrictions are as following:
echo    - use 'initialposition' for static model name
echo    - fill in the input load excel file with X and Y in Orcaflex axis
echo.


set /p static_model_path="Enter the path file name of the static: "
set /p input_file="Enter the path file name of your input excel: "
echo 

python  ./generate_loadcases.py %static_model_path% %input_file%

pause