#!/bin/bash

CURDIR=$PWD
ANACONDA_FILE=Anaconda3-4.2.0-Linux-x86_64.sh
ANACONDA_MD5=4692f716c82deb9fa6b59d78f9f6e85c
cd /tmp

# Download and install Anaconda
curl -O https://repo.continuum.io/archive/$ANACONDA_FILE
FILE_MD5=$(md5sum $ANACONDA_FILE | awk '{print $1}')
if [ "$ANACONDA_MD5" != "$FILE_MD5" ]
then
    echo "Download of file: $ANACONDA_FILE failed, try again"
    rm $ANACONDA_FILE
    exit 1
fi
bash $ANACONDA_FILE
rm -f $ANACONDA_FILE

# Add environment variables to .bashrc
if ! grep -Fq "PYSPARK_DRIVER_PYTHON=" ~/.bashrc
then
  echo 'export PYSPARK_DRIVER_PYTHON=jupyter' >> ~/.bashrc
fi
if ! grep -Fq "PYSPARK_DRIVER_PYTHON_OPTS=" ~/.bashrc
then
  echo "export PYSPARK_DRIVER_PYTHON_OPTS='notebook'" >> ~/.bashrc
fi

# Source .bashrc to set environement variables and add Anaconda binaries to path
. ~/.bashrc

cd $CURDIR

