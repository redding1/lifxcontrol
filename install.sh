#!/bin/bash
#chmod a+x install.sh
#Install Python
sudo apt-get install python
#Download the programs, unzip, and install
wget https://github.com/redding1/lifxcontrol/archive/rev0.3.zip
unzip file.zip lifxcontrol-rev0.2.zip
cd lifxcontrol-rev0.2
sudo python setup.py install
cd ..
#Download, extract and install python-nmap 
sudo wget http://xael.org/pages/python-nmap-0.1.4.tar.gz
tar xvzf python-nmap-0.1.4.tar.gz
cd python-nmap-0.1.4.tar.gz
sudo python setup.py install
#Updated python install package
easy_install -U distribute
