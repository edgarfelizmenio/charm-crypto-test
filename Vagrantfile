VAGRANTFILE_API_VERSION = "2"
DEFAULT_BOX = "ubuntu/trusty64"

ENV["LC_ALL"] = "en_US.UTF-8"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.define("CHARM") do |charm|
        charm.vm.box = DEFAULT_BOX
        charm.vm.provider "virtualbox" do |v|
            v.name = "CHARM"
            v.customize ["modifyvm", :id, "--memory", 512]
        end

        charm.vm.network "public_network", ip: "192.168.1.100"

        charm.vm.synced_folder ".", "/home/CHARM-TEST"

        charm.vm.provision "update", type: :shell do |shell|
            shell.inline = "apt-get -y -q update"
        end

        charm.vm.provision "install_htop", type: :shell do |shell|
            shell.inline = "apt-get -y -q install htop"
        end

        charm.vm.provision "install", type: :shell do |shell|
            shell.path = "install.sh"
        end

    end
    
end
