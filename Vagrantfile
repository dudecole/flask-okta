$script = <<-SCRIPT
    #sudo apt update -y
    #sudo apt install -y python3-pip
    sudo yum -y update
    sudo yum -y install python3-pip
    pip3 install --upgrade pip
    pip3 install wheel
    pip3 install -r /vagrant/vagrant-requirements.txt

 #   if [ ! -e /etc/pki/ca-trust/source/anchors/zscaler.cer ]
 #   then
 #       cp /vagrant/Zscaler.cer /etc/pki/ca-trust/source/anchors/zscaler.cer
 #       update-ca-trust
 #   fi

 #   if ! grep -q 'HTTPLIB_CA_CERTS_PATH' /home/vagrant/.bashrc
 #   then
 #       echo 'export HTTPLIB_CA_CERTS_PATH=/etc/pki/tls/certs/ca-bundle.crt' >> /home/vagrant/.bashrc
 #   fi

 #   cd /vagrant
 #   GUNICORN_CMD_ARGS="--bind=0.0.0.0 --workers=3" gunicorn -chdir /vagrant/app:app
SCRIPT

#$gunicorn = <<-SCRIPT
#    gunicorn -w 2 -b 0.0.0.0:8000 --chdir /vagrant app:app --reload --timeout 900
#SCRIPT

Vagrant.configure("2") do |config|
  #config.vm.box = "ubuntu/trusty64"
  config.vm.box = "bento/centos-7.4"
  config.vm.network "public_network", #ip: "192.168.1.101",
    use_dhcp_assigned_default_route: true
   # netmask: "255.255.255.0", auto_config: false
   # use_dhcp_assigned_default_route: true
# config.vm.network "private_network", ip: "192.168.56.143"
  config.vm.network "forwarded_port", guest: 8000, host: 8000
  #config.vm.network "forwarded_port", guest: 5000, host: 5000
  #config.vm.network "forwarded_port", guest: 443, host: 443
  #config.vm.network "forwarded_port", guest: 80, host: 80

  config.vm.provider "virtualbox" do |vb|
    vb.name = 'docker-vm'
    vb.memory = 4096
    vb.cpus = 1
    #vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    #vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
  end
  #config.vm.provision "shell",
  #  run: "always",
  #  inline: "sudo route add default gw 192.168.1.1"
  config.vm.provision "shell", inline: $script
  config.vm.provision :docker
  config.vm.provision :docker_compose
#  config.vm.provision "shell", inline: "gunicorn -w 2 -b 0.0.0.0:8000 --chdir /vagrant app:app"
#  config.vm.provision :docker_compose #, yml: "/vagrant/docker-compose.yml", run: "always"
end
# Marvell AVASTAR Wireless-AC Network Controller