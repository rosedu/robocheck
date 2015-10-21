build:
	mkdir exes
	cl /Zi /MT /EHsc /Oy- /Ob0 /Ferobocheck-test.exe main.c
	xcopy robocheck-test.exe exes\ /y
	xcopy input.txt exes\ /y
clean:
	rd /s /q exes
	del main.obj robocheck-test.exe
	del *.pdb *.ilk
