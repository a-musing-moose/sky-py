# -*- mode: ruby -*-
# vi: set ft=ruby :

# Vagrantfile API/syntax version. Don't touch unless you know what you're doing!
VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|
  config.vm.box = "precise64"
  config.vm.box_url = "http://files.vagrantup.com/precise64.box"

  # Share the Sky port with the host machine.
  config.vm.network :forwarded_port, guest: 8585, host: 8585

  # The bootstrap script configures the box with Go, installs dependencies,
  # and starts the Sky server as a daemon.
  config.vm.provision "shell", path: "bootstrap.sh"

  # Share GOPATH between vagrant and the host machine. This is
  # useful when developing on Sky. You must run "vagrant reload"
  # after changing this.
  #
  # config.vm.synced_folder ENV["GOPATH"], "/gocode"
end
