VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  unless Vagrant.has_plugin?("vagrant-hostmanager")
      raise 'vagrant-hostmanager is not installed. run: vagrant plugin install vagrant-hostmanager'
  end

  config.vm.define "vup" do |vup|
    vup.vm.box = "ubuntu/trusty64"
    vup.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64"

    vup.vm.network :private_network, ip: "192.168.4.2"
    vup.vm.hostname = "vup.dev"

    vup.vm.network "forwarded_port", guest: 80, host: 80
    vup.vm.network "forwarded_port", guest: 3306, host: 3306
    vup.vm.network "forwarded_port", guest: 9000, host: 9000
    vup.vm.network "forwarded_port", guest: 8080, host: 8080
    vup.vm.network "forwarded_port", guest: 5000, host: 5000

    vup.vm.synced_folder ".", "/usr/local/vup"
    vup.vm.synced_folder "salt/roots", "/srv"

    # Hosts management plugin for Vagrant
    # Use this to install: vagrant plugin install vagrant-hostmanager
    vup.hostmanager.enabled = true
    vup.hostmanager.manage_host = true
    vup.hostmanager.aliases = %w(vup.dev)
    vup.vm.provision :salt do |salt|
        salt.minion_config = "salt/minion"
        salt.run_highstate = true
        salt.log_level = "debug"
        salt.colorize = true
        salt.verbose = true
    end
  end

  config.vm.define "docker1" do |docker1|
    docker1.vm.box = "ubuntu/trusty64"
    docker1.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64"

    docker1.vm.network :private_network, ip: "192.168.4.20"
    docker1.vm.hostname = "docker1.dev"

    docker1.vm.synced_folder "salt/roots", "/srv"

    # Hosts management plugin for Vagrant
    # Use this to install: vagrant plugin install vagrant-hostmanager
    docker1.hostmanager.enabled = true
    docker1.hostmanager.manage_host = true
    docker1.hostmanager.aliases = %w(docker1.dev)
    docker1.vm.provision :salt do |salt|
        salt.minion_config = "salt/minion_docker"
        salt.run_highstate = true
        salt.log_level = "debug"
        salt.colorize = true
        salt.verbose = true
    end
  end
end
