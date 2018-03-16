#! /bin/sh
# Script for install the project dependencies
OPENFACE='/tmp/openface'

# Add pike repository
wget -qO- http://pike.esi.uclm.es/add-pike-repo.sh | sudo sh

# Install Python3
sudo apt-get install -y python3 python3-pip

# Install ZeroC Ice for Python 3
sudo apt-get install -y python3-zeroc-ice zeroc-ice36

# Install Scone
sudo apt-get install -y scone scone-server scone-wrapper 

# Install citisim libraries
sudo apt-get install -y dharma citisim-slice libcitisim citisim-wiring-service

# Upgrade pip3
sudo -H pip3 install --upgrade pip

# Clone openface repository
git clone --recursive https://github.com/cmusatyalab/openface.git $OPENFACE

# Install openface
cd $OPENFACE
sudo pip3 install -r requirements.txt
sudo python3 setup.py install

# Install opencv for Python3
sudo pip3 install opencv-python

# Install Python libraries
sudo pip3 install scikit-learn scipy watson-developer-cloud watchdog service_identity

# Install dlib for Python3
sudo apt-get install -y cmake
pip3 install dlib

echo "==================================="
echo "Dependencies installation finished."
echo "==================================="
