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

  config.vm.define "vocker1" do |vocker1|
    vocker1.vm.box = "ubuntu/trusty64"
    vocker1.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64"

    vocker1.vm.network :private_network, ip: "192.168.4.20"
    vocker1.vm.hostname = "vocker1.dev"
    vocker1.vm.synced_folder "salt/roots", "/srv"

    # Hosts management plugin for Vagrant
    # Use this to install: vagrant plugin install vagrant-hostmanager
    vocker1.hostmanager.enabled = true
    vocker1.hostmanager.manage_host = true
    vocker1.hostmanager.aliases = %w(docker1.dev)
    vocker1.vm.provision :salt do |salt|
        salt.minion_config = "salt/minion_vocker"
        salt.run_highstate = true
        salt.log_level = "debug"
        salt.colorize = true
        salt.verbose = true
    end
  end
end
