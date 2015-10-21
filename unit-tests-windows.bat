:: Run all unit tests
@echo off

setlocal EnableDelayedExpansion
dir /b unit-tests > tempFile1
findstr /e /c:".py" tempFile1 > tempFile2
findstr /B /R /C:"[^__]" tempFile2 > tempFile3
del tempFile1
del tempFile2

set /A testIndex=1
for /F "tokens=*" %%A in (tempFile3) do (
	echo|set /p=Test !testIndex!:
	echo  %%~nA
	echo ----------------------------------------------------------------------
	call python -m unit-tests.%%~nA -v
	set /A "testIndex+=1"
	echo.
)

del tempFile3
