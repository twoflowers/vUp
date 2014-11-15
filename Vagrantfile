VAGRANTFILE_API_VERSION = "2"

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

  config.vm.define "vup" do |vup|
    vup.vm.box = "ubuntu/trusty64"
    vup.vm.box_url = "https://vagrantcloud.com/ubuntu/boxes/trusty64"

    vup.vm.network :private_network, ip: "192.168.4.2"
    vup.vm.hostname = "dev.vup"

    # Hosts management plugin for Vagrant
    # Use this to install: vagrant plugin install vagrant-hostmanager
    vup.hostmanager.enabled = true
    vup.hostmanager.manage_host = true
    vup.hostmanager.aliases = %w(dev.vup)
  end
end
