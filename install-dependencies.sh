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
sudo apt-get install -y citisim-slice libcitisim citisim-wiring-server property-service-simple

# Upgrade pip3
sudo -H pip3 install --upgrade pip

# Install openface
# Clone openface repository
git clone --recursive https://github.com/cmusatyalab/openface.git $OPENFACE
# Install openface
cd $OPENFACE
sudo pip3 install -r requirements.txt
sudo python3 setup.py install

# Install opencv for Python3
sudo pip3 install opencv-python

# Install torch
if type "th" > /dev/null; then
   echo 'Torch is installed.'
else
   git clone https://github.com/torch/distro.git ~/torch --recursive
   cd ~/torch; bash install-deps;
   ./install.sh
   source ~/.bashrc
   for NAME in dpnn nn optim optnet csvigo cutorch cunn fblualib torchx tds; do luarocks install $NAME; done
fi

# Install Python libraries
sudo pip3 install watson-developer-cloud watchdog service_identity apiai scipy

# Install dlib for Python3
sudo apt-get install -y cmake
sudo pip3 install dlib

echo "==================================="
echo "Dependencies installation finished."
echo "==================================="
