#!/bin/bash

ANACONDA_FILE=Anaconda3-4.2.0-Linux-x86_64.sh
ANACONDA_LOCAL_FILE=/tmp/$ANACONDA_FILE
ANACONDA_REMOTE_FILE=https://repo.anaconda.com/archive/$ANACONDA_FILE
ANACONDA_MD5=4692f716c82deb9fa6b59d78f9f6e85c
ANACONDA_BKP=https://public.pic.es/s/dyD4bNomgRAQlqC/download

# Download and install Anaconda
CONDA_VERSION=$(conda --version 2> /dev/null)
if [ "$CONDA_VERSION" != "conda 4.2.9" ]
then
  wget -P /tmp $ANACONDA_REMOTE_FILE
  FILE_MD5=$(md5sum $ANACONDA_LOCAL_FILE | awk '{print $1}')
  if [ "$ANACONDA_MD5" != "$FILE_MD5" ]
  then
      echo "Download of file: $ANACONDA_FILE failed, trying from backup"
      rm -f $ANACONDA_LOCAL_FILE
      wget -O $ANACONDA_LOCAL_FILE $ANACONDA_BKP
      FILE_MD5=$(md5sum $ANACONDA_LOCAL_FILE | awk '{print $1}')
      if [ "$ANACONDA_MD5" != "$FILE_MD5" ]
      then
          echo "Download of file: $ANACONDA_FILE from backup failed, contact support"
          rm -f $ANACONDA_LOCAL_FILE
          exit 1
      fi
  fi

  bash $ANACONDA_LOCAL_FILE
  rm -f $ANACONDA_LOCAL_FILE
  
  # Add environment variables to .bashrc
  if ! grep -Fq "PYSPARK_DRIVER_PYTHON=" ~/.bashrc
  then
    echo 'export PYSPARK_DRIVER_PYTHON=jupyter' >> ~/.bashrc
  fi
  if ! grep -Fq "PYSPARK_DRIVER_PYTHON_OPTS=" ~/.bashrc
  then
    echo "export PYSPARK_DRIVER_PYTHON_OPTS='notebook'" >> ~/.bashrc
  fi
else
  echo "Anaconda already installed and at the convenient version"
fi

# Source .bashrc to set environement variables and add Anaconda binaries to path
. ~/.bashrc

# Add some extra configuration needed by pyspark
if ! grep -Fq "^spark.driver.memory" /etc/spark/conf/spark-defaults.conf
then
  echo 'spark.driver.memory     2g' | sudo tee -a /etc/spark/conf/spark-defaults.conf >> /dev/null
fi

