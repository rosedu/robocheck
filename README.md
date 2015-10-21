Robocheck
==========
Work in progress.

Installation
=================
##### 1. Linux
First of all download Robocheck
```
$ git clone git@github.com:rosedu/robocheck.git
```
###### 1.1 Using the installation script
Run the following command from the downloaded folder.
```
$ ./install-robocheck-linux.sh
```
From now on you can run Robocheck just by using the command `$ robocheck`.

###### 1.2 Step by step installation:
After you've downloaded the files check to see if **Python** is installed.
You can install it by running
```
$ apt-get install python
```
The next step would be to install **python-pip**
```
$ apt-get install python-pip
```
Create an alias for Robocheck in `~/.bashrc` like this:
```
alias robocheck="python /path/to/robocheck-core.py"
```
Installing Robocheck's dependencies:

1. **Valgrind**
    ```
    $ valgrind --version
    ```
    If the command is not found run:
    ```
    $ apt-get install valgrind
    ```
2. **Dr. Memory**
    ```
    $ drmemory -version
    ```
    If the command is not found download Dr. Memory from [here](https://drmemory.googlecode.com/files/DrMemory-Linux-1.5.1-6.tar.gz). After downloading extract the files from the archive using
    ```
    $ tar -xzf DrMemory-Linux-1.5.1-6.tar.gz
    ```
    Create a symbolic link to drmemory's binary in `/bin` so that it can be run using drmemory command.
    ```
    $ ln -s /path/to/DrMemory-Linux-1.5.1-6/bin/drmemory.pl /bin/drmemory
    ```
    Check to see if it's working by running
    ```
    $ drmemory -version
    ```

You have succesfully installed Robocheck! :)

##### 2. Windows
Download robocheck by clicking [here](https://github.com/rosedu/robocheck/archive/master.zip) or on the **Download ZIP** button on the right of this page and then extract the archive.

Before moving further make sure you installed:
* **Python2.7** along with **python-pip**. You can download the installer from [here](https://www.python.org/ftp/python/2.7.10/python-2.7.10.amd64.msi).
* **Microsoft Visual Studio**. The installer is found [here](https://www.visualstudio.com/en-us/downloads/download-visual-studio-vs.aspx). (**Before running Robocheck** `cl` and `nmmake` commands should be available from the command prompt. [Go to this link]() for a guide on how to do this.)



###### 1.1 Using the installation script
Open a command prompt window and go to the extracted directory.
```
C:\path\to\robocheck> install-robocheck-windows.bat
```
If the installation was successful the next step should be setting the environment variables.

Go to **Control Panel > System > Advanced system settings** and then, under the **Advanced** tab, click on *Environment Variables...*.

Edit the **PATH** system variable by appending the following, each suffixed by a semicolon:
* robocheck folder path
* drmemory bin folder path


```
C:\last\path;C:\path\to\robocheck;C:\path\to\drmemory\bin;
```

Test if robocheck is available from command prompt
```
C:\> robocheck
```
###### 1.2 Step by step installation
Open a command prompt.
```
C:\> pip install -U mock
```
Download Dr. Memory from [this link](https://bintray.com/artifact/download/bruening/DrMemory/DrMemory-Windows-1.8.1-RC1.zip). Extract the archive and then add the path of the Dr. Memory `bin/` directory to the `PATH` variable as shown above.

You have succesfully installed Robocheck! :)

Configuration
==============

###### 1. If you have an alias in `.bashrc` run:
```
robocheck --config
```
###### 2. Otherwise run:
```
python /path/to/robocheck-core.py --config
```

Using Robocheck
================
**IMPORTANT!!! Never run Robocheck through a symbolic link!** Use either an alias or the full command.

Robocheck receives a zip archive that must have a predefined structure!
###### 1. Zip Archive's structure
The archive must have in the root two folders `src/` and `bins/`. In
the `src/` folder there should be all the source files for the executables and
in `bins/` all the binaries/executables and if necessary their data files.

###### 2. Running robocheck
After the archive was created using the specifications from 3.1 you can run Robocheck:

* (Linux) If you have an alias in `.bashrc` using `robocheck /path/to/Archive.zip`
* (Windows) If the environment paths are set accordingly using `python robocheck.py /path/to/Archive.zip`
* Otherwise using `python /path/to/robocheck-core.py /path/to/Archive.zip`
