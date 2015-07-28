#! /bin/bash

if [ $0 != './install-robocheck-linux.sh' ]; then
  echo 'ERROR: The script must be executed directly from the folder!'
  exit 1
fi

if touch /bin &> /dev/null ; then :
else
  echo 'ERROR: You must be root!'
  exit 1
fi
echo "Starting..."
echo "Installing python..."
  apt-get install python

echo
echo "Installing python-pip..."
  apt-get install python-pip
echo
echo "Installing mock python library..."
  pip install -U mock

echo
echo "Installing DrMemory..."
  if drmemory -version &> /dev/null; then
    echo 'Ok!'
  else
    mkdir Tools
    cd Tools
    wget https://drmemory.googlecode.com/files/DrMemory-Linux-1.5.1-6.tar.gz
    tar -xzf DrMemory-Linux-1.5.1-6.tar.gz
    rm DrMemory-Linux-1.5.1-6.tar.gz
    currentPath=$(pwd)
    drmemoryPath=$currentPath'/DrMemory-Linux-1.5.1-6/bin/drmemory.pl'
    ln -s $drmemoryPath /bin/drmemory
    cd ..
    echo 'Ok!'
  fi
currentPath=$(pwd)

echo
echo "Installing Valgrind..."
apt-get install valgrind

echo
echo "Finishing..."
echo "Creating alias..."
robocheckPath=$currentPath'/robocheck-core.py'
if grep $robocheckPath ~/.bashrc; then :
else
  echo "alias robocheck='python $robocheckPath'" >> ~/.bashrc
fi

echo
echo "Robocheck was succefully installed!"
echo "Warning: Never run robocheck through a symbolic link!"
echo "         Use robocheck command directly!"
