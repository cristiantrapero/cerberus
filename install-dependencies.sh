#! /bin/sh
OPENFACE='/tmp/openface'

echo "=================================================="
echo "       Añadiendo el repositorio pike de ARCO"
echo "=================================================="
wget -qO- http://pike.esi.uclm.es/add-pike-repo.sh | sudo sh
sudo apt-get update

echo "=================================================="
echo "            Instalando Python3"
echo "=================================================="
sudo apt-get install -y python3 python3-pip

echo "=================================================="
echo "            Instalamos Ice para Python"
echo "=================================================="
sudo apt-get install -y python3-zeroc-ice zeroc-ice36

echo "=================================================="
echo "                 Instalando Scone"
echo "=================================================="
sudo apt-get install -y scone scone-server scone-wrapper 

echo "=================================================="
echo "Instalando Dharma, interfaces de Citisim y Wiring Service"
echo "=================================================="
sudo apt-get install -y dharma citisim-slice libcitisim citisim-wiring-service

echo "=================================================="
echo "                Actualizando PIP"
echo "=================================================="
sudo -H pip3 install --upgrade pip

echo "=================================================="
echo "    Descargando el repositorio de Openface"
echo "=================================================="
git clone --recursive https://github.com/cmusatyalab/openface.git $OPENFACE

echo "=================================================="
echo "    Instalando dependencias de Openface"
echo "=================================================="
cd $OPENFACE
sudo pip3 install -r requirements.txt
sudo python3 setup.py install

echo "=================================================="
echo "          Instalando OpenCV para Python"
echo "=================================================="
sudo pip3 install opencv-python

echo "=================================================="
echo "    Instalando librerias de python para Openface"
echo "=================================================="
sudo pip3 install scikit-learn scipy watson-developer-cloud watchdog

echo "=================================================="
echo "         Instalando DLIB"
echo "=================================================="
sudo apt-get install -y cmake
pip3 install dlib

echo "=================================================="
echo "                Instalando Torch"
echo "=================================================="
pip3 install http://download.pytorch.org/whl/cu80/torch-0.3.1-cp36-cp36m-linux_x86_64.whl 
pip3 install torchvision

echo "=================================================="
echo "              Instalando Luarocks"
echo "=================================================="
sudo apt-get install -y luarocks

echo "=================================================="
echo "        Instalando modulos Lua"
echo "=================================================="
for NAME in dpnn nn optim optnet csvigo cutorch cunn fblualib torchx tds; do luarocks install $NAME; done

echo "=================================================="
echo "        Limpiamos los directorios de descarga"
echo "=================================================="
sudo rm -rf $OPENFACE
