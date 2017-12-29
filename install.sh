#! /bin/bash -x

apt-get install -y -q lzip
apt-get install -y -q flex bison
apt-get install -y -q python3-setuptools
apt-get install -y -q python3-dev
apt-get install -y -q python3.4-venv

cd ../CHARM-TEST

# Install GMP
tar --lzip -xvf gmp-6.1.2.tar.lz;
cd gmp-6.1.2;
./configure;
make;
make check;
make install; # sudo make install

# Install PBC from source
cd ..
tar -xvf pbc-0.5.14.tar.gz
cd pbc-0.5.14
./configure
./configure LDFLAGS="-lgmp"
make
make install
ldconfig

# Install OpenSSL

cd ..
tar -xvf openssl-1.1.0g.tar.gz
cd openssl-1.1.0g
./config
make
make test
make install
ldconfig

# Now we can build and install Charm:
cd ..
python3 -m venv env
source env/bin/activate
pip3 install --upgrade setuptools

cd charm
./configure.sh
make install
make test

pip3 freeze