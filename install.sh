#!/bin/bash
#chmod a+x install.sh

sudo apt-get install python
wget https://github.com/redding1/lifxcontrol/archive/rev0.2.zip
unzip file.zip lifxcontrol-rev0.2.zip
cd lifxcontrol-rev0.2
sudo python setup.py install
cd ..
sudo wget http://xael.org/pages/python-nmap-0.1.4.tar.gz
tar xvzf python-nmap-0.1.4.tar.gz
cd python-nmap-0.1.4.tar.gz
sudo python setup.py install
