@echo off
echo Here you can redefine the mesh of your bathy
echo Just fill in the below input
echo your input bathy file must be in following format
echo.
echo X;Y;Z
echo 123;45;335
echo 124;45;332
echo 125;45;331
echo 126;45;338
echo.

set /p filename="path of original bath file in .csv: "
set /p dx="Step in x axis for new mesh: "
set /p dy="Step in y axis for new mesh: "

python mesh_bathy.py %filename% %dx% %dy%

pause