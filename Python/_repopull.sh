#!/bin/bash

cd /home/ubuntu
sudo rm -r /home/ubuntu/GitRepo
git clone https://github.com/pwalker91/CSUMB_Capstone-CPUC-Database-Management.git GitRepo
echo "Repository cloned into 'ubuntu' home folder"
cd -
