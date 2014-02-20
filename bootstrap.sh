#!/usr/bin/env bash

SKY=sky-unstable
DEPS=sky-deps-unstable

export GOPATH=/gocode
GO=/usr/local/go/bin/go

# Setup profile.
echo "export GOPATH=$GOPATH" | sudo tee /etc/profile.d/go.sh > /dev/null
echo "PATH=\$PATH:/usr/local/go/bin:$GOPATH/bin" | sudo tee -a /etc/profile.d/go.sh > /dev/null
source /etc/profile

# Create man1 directory for LMDB.
sudo mkdir -p /usr/local/man/man1

# Setup build environment.
if [ ! -f ".provisioned" ]; then
	sudo apt-get -y update
	sudo apt-get install -y build-essential git
	touch .provisioned
fi

# Download and install Go.
if [ ! -d "/usr/local/go" ]; then
	wget https://go.googlecode.com/files/go1.1.2.linux-amd64.tar.gz
	sudo tar -C /usr/local -xzf go1.1.2.linux-amd64.tar.gz
fi

# Download and install Sky dependencies.
if [ ! -d "$DEPS" ]; then
	rm -rf ${DEPS}
	wget -O ${DEPS}.tar.gz https://github.com/skydb/sky-deps/archive/unstable.tar.gz
	tar zxvf ${DEPS}.tar.gz
	sudo make -C ${DEPS} clean install
fi

# Update the linker to recognize the library location.
echo '/usr/local/lib' | sudo tee /etc/ld.so.conf.d/sky.conf > /dev/null
sudo ldconfig

# Download Sky and its dependencies.
if [ ! -d "$GOPATH" ]; then
	mkdir -p $GOPATH/src/github.com/skydb
	git clone -b unstable https://github.com/skydb/sky.git $GOPATH/src/github.com/skydb/sky
	$GO get github.com/skydb/sky/...
fi

# Install and run Sky.
$GO install github.com/skydb/sky/skyd

sudo killall -9 skyd > /dev/null 2>&1
sudo $GOPATH/bin/skyd >> /var/log/skyd.log &

