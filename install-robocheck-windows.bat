@echo off
echo Installing Robocheck
echo ==================================

:: Default values
set environmentWarning=0
set drmemoryPathWarning=0

:: Check prerequisites
:: Check if python is installed
echo|set /p=PYTHON 2.7.x ..........
python --version 2> tempFile
if %errorlevel% neq 0 goto errorNoPython
findstr /C:"2.7" tempFile > nul 2>&1
if %errorlevel% neq 0 goto errorNoPython
del tempFile
echo  OK

:: Check if python pip is installed
echo|set /p=PYTHON-PIP ..........
pip --version > nul 2>&1
if %errorlevel% neq 0 goto errorNoPythonPip
echo  OK

:: Check if CL is available from cmd
echo CL (compiler) .......... Manual
cl > nul 2>&1
if %errorlevel% neq 0 (
	set environmentWarning=1
)

:: Check if nmake is available from cmd
echo NMAKE ......... Manual
nmake /help > nul 2>&1
if %errorlevel% neq 0 (
	set environmentWarning=1
)

:: Finished checking prerequisites

:: Get additional packets
:: Install python mock library
echo.
echo **Installing python mock library...
pip install -U mock > nul 2>&1
echo Done

:: Install Dr. Memory tool
echo.
echo **Installing Dr. Memory ...
:: check if tool is installed
drmemory -version > nul 2>&1
if %errorlevel% equ 0 (
	echo Already installed
	goto drmemoryInstalled
)
:: install locally
:: check if tool directory exists
if not exist ./tools/ (
	mkdir tools
)

if exist %cd%\tools\DrMemory-Windows-1.8.1-RC1\bin\drmemory.exe (
	set drmemoryPathWarning=1
	goto drmemoryInstalled
)
if not exist %cd%\tools\drmemory.zip (
	python ./utils/download.py ./tools drmemory.zip https://bintray.com/artifact/download/bruening/DrMemory/DrMemory-Windows-1.8.1-RC1.zip
	if %errorlevel% neq 0 goto errorNoDownloadSuccess
)
python ./utils/unzip.py ./tools/drmemory.zip ./tools
if %errorlevel% neq 0 goto errorNoUnzipSuccess
echo Done
set drmemoryPathWarning=1
echo You can find drmemory at %cd%\tools\DrMemory-Windows-1.8.1-RC1\bin\drmemory.exe
:drmemoryInstalled

:: Finished install
echo.
if %drmemoryPathWarning% equ 1 (
	echo ## WARNING ## drmemory is not available from cmd.
)
if %environmentWarning% equ 1 (
	echo ## WARNING ## CL or NMAKE are not available from cmd.
	echo.
)
echo|set /p=Robocheck has been installed!
exit /b 0

:: Exception handling
:errorNoPython
echo  ERROR
echo.
echo You must install Python 2.7.x before installing Robocheck!
exit /b 1

:errorNoPythonPip
echo  ERROR
echo.
echo You must install python pip before installing Robocheck!
exit /b 1

:errorNoDownloadSuccess
echo  ERROR
echo.
echo The download process was unsuccessful!
exit /b 1

:errorNoUnzipSuccess
echo  ERROR
echo.
echo The unzip process was unsuccessful!
exit /b 1