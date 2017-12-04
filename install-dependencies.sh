#! /bin/sh
OPENFACE='/tmp/openface'
BOOST='/tmp/boost'
DLIB='/tmp/dlib'

echo "=================================================="
echo "       Añadiendo el repositorio pike de ARCO"
echo "=================================================="
wget -qO- http://pike.esi.uclm.es/add-pike-repo.sh | sudo sh
sudo apt-get update

echo "=================================================="
echo "            Instalando Python2.7 y Python3"
echo "=================================================="
sudo apt-get install -y python2.7 python3

echo "=================================================="
echo "            Instalamos Ice para Python"
echo "=================================================="
sudo apt-get install -y python-zeroc-ice36 python3-zeroc-ice zeroc-ice36

echo "=================================================="
echo "                 Instalando Scone"
echo "=================================================="
sudo apt-get install -y scone scone-server scone-wrapper 

echo "=================================================="
echo "Instalando Dharma, interfaces de Citisim y Wiring Service"
echo "=================================================="
sudo apt-get install -y dharma citisim-slice libcitisim citisim-wiring-service

echo "=================================================="
echo "        Instalando paquetes necesarios"
echo "=================================================="
sudo apt-get install -y curl git graphicsmagick libssl-dev libffi-dev python-dev python-pip python-numpy python-nose python-scipy \
python-pandas python-protobuf python-openssl wget zip python3-pip

echo "=================================================="
echo "                Actualizando PIP"
echo "=================================================="
sudo -H pip2 install --upgrade pip
sudo -H pip3 install --upgrade pip

echo "=================================================="
echo "    Descargando el repositorio de Openface"
echo "=================================================="
git clone --recursive https://github.com/cmusatyalab/openface.git $OPENFACE

echo "=================================================="
echo "    Instalando dependencias de Openface"
echo "=================================================="
cd $OPENFACE
sudo pip2 install -r requirements.txt
sudo python setup.py install
sudo pip2 install --user --ignore-installed -r ./demos/web/requirements.txt
sudo pip2 install -r ./training/requirements.txt

echo "=================================================="
echo "          Instalando OpenCV para Python"
echo "=================================================="
sudo apt-get install -y libopencv-dev python-opencv

echo "=================================================="
echo "    Instalando librerias de python para Openface"
echo "=================================================="
sudo pip install scikit-learn
sudo pip3 install scipy watson-developer-cloud watchdog

echo "=================================================="
echo "           Instalando libreria Boost"
echo "=================================================="
wget -P $BOOST https://dl.bintray.com/boostorg/release/1.64.0/source/boost_1_64_0.tar.bz2
tar xf $BOOST/boost_1_64_0.tar.bz2 -C $BOOST/
cd $BOOST/boost_1_64_0/
sh bootstrap.sh --with-libraries=python
./b2
sudo ./b2 install

echo "=================================================="
echo "         Instalando dependencias para DLIB"
echo "=================================================="
sudo apt-get install -y libopenblas-dev liblapack-dev cmake

echo "=================================================="
echo "                 Instalando DLIB"
echo "=================================================="
wget -P $DLIB http://dlib.net/files/dlib-19.4.tar.bz2
tar xf $DLIB/dlib-19.4.tar.bz2 -C $DLIB/
cd $DLIB/dlib-19.4/python_examples/
mkdir build
cd build
cmake ../../tools/python
cmake --build . --config Release
sudo cp dlib.so /usr/local/lib/python2.7/dist-packages

echo "=================================================="
echo "                Instalando Torch"
echo "=================================================="
git clone https://github.com/torch/distro.git ~/torch --recursive
cd ~/torch; bash install-deps
echo "yes" | ./install.sh
source ~/.bashrc

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
sudo rm -rf $OPENFACE $BOOST $DLIB
