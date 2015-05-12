#!/bin/bash

cd /home/ubuntu
bash /home/ubuntu/_repopull.sh
cp -rf /home/ubuntu/GitRepo/PHP/* /home/ubuntu/csdi_www
cp -rf /home/ubuntu/GitRepo/Python/* /home/ubuntu/csdi_scripts
echo "Copied Github files to necessary directories"
cd -
