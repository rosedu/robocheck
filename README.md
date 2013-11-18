robocheck
=========

Work in progress.

How to
=========

1 Install Robocheck

 1.1 Linux instalation
 
  First of all run:
  
    git clone git@github.com:rosedu/robocheck.git

  1.1.1 Using the instaltion script
   
  After you've donwloaded Robocheck's files just run:
  
    install-robocheck-linux.sh
    
  directly from the folder. From now on you can run Robocheck just by using the command robocheck.

   1.1.2 Step by step installation:
   
    * After you've downloaded the files check to see if Python is installed.
    In order to do that run:
        python --version

        if the command is not found run:
            apt-get install python
        if the version is older than Python 2.7 run:
            apt-get update python

    * Create an alias for Robocheck in ~/.bashrc like this:
        alias robocheck="python /path/to/robocheck-core.py"

    IMPORTANT!!! Never run Robocheck through a symbolic link!
    Use either an alias or the full command.

    * Installing Robocheck's dependencies:
        a) Valgrind
        run: valgrind --version
        if the command is not found run:
            apt-get install valgrind

        b) Dr. Memory
        run: drmemory -version

        if the command is not found download Dr. Memory fron here:
            https://drmemory.googlecode.com/files/DrMemory-Linux-1.5.1-6.tar.gz

        after donwloading extract the files from the archive using
            tar -xzf DrMemory-Linux-1.5.1-6.tar.gz

        create a symbolic link to drmemory's binary in /bin so that it can be
        runned using drmemory command.

        ln -s /path/to/DrMemory-Linux-1.5.1-6/bin/drmemory.pl /bin/drmemory

        check to see if it's working by running drmemory -version

    * You have succesfully installed Robocheck! :)

    1.2 Windows installation
        Availiable soon!

2 Configure Robocheck

   2.1 If you have an alias in .bashrc run:
   
    robocheck --config

   2.2 Otherwise run:
   
    python /path/to/robocheck-core.py --config

3 Run Robocheck

  IMPORTANT!!! Never run Robocheck through a symbolic link!
Use either an alias or the full command.

    Robocheck receives a zip archive that must have a predefined structure!

    3.1 Zip Archive's structure
    
     The archive must have in the root two folders "src" and "bins". In
    the src folder there should be all the source files for the executables and
    in bins all the binaries/executables and if necessary their data files.

    3.2 Running robocheck
    
     After the archive was created using the specifications from 3.1 you can
    run Robocheck:
    
        -if you have an alias in .bashrc using:
        robocheck /path/to/Archive.zip

        -otherwise:
        python /path/to/robocheck-core.py /path/to/Archive.zip
