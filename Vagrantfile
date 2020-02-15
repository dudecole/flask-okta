$script = <<-SCRIPT

    yum -y update

    yum -y install python3-pip

    pip3 install --upgrade pip
    pip3 install wheel
    pip3 install -r /vagrant/vagrant-requirements.txt


    if [ ! -e /etc/pki/ca-trust/source/anchors/zscaler.cer ]
    then
        cp /vagrant/Zscaler.cer /etc/pki/ca-trust/source/anchors/zscaler.cer
        update-ca-trust
    fi

    if ! grep -q 'REQUESTS_CA_BUNDLE' /home/vagrant/.bashrc
    then
        echo 'export REQUESTS_CA_BUNDLE=/etc/pki/tls/certs/ca-bundle.crt' >> /home/vagrant/.bashrc
        echo 'export SSL_CERT_FILE=/vagrant/zscaler.pem' >> /home/vagrant/.bashrc
    fi

SCRIPT

$docker_script = <<-SCRIPT
    sudo apt update -y
    sudo apt install -y python3-pip

#    vagrant plugin install vagrant-docker-compose

#    yum -y remove docker \
#                  docker-client \
#                  docker-client-latest \
##                  docker-common \
#                  docker-latest \
#                  docker-latest-logrotate \
#                  docker-logrotate \
#                  docker-engine

#    yum -y install -y yum-utils \
#    device-mapper-persistent-data \
#    lvm2

#    yum-config-manager \
#    --add-repo \
#    https://download.docker.com/linux/centos/docker-ce.repo

#    yum -y install docker-ce docker-ce-cli containerd.io
#    sudo usermod -aG docker $USER

#    sudo systemctl start docker
#    systemctl enable docker.service


#    sudo curl -L "https://github.com/docker/compose/releases/download/1.25.3/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
#    sudo chmod +x /usr/local/bin/docker-compose

SCRIPT

Vagrant.configure("2") do |config|
  config.vm.define "flask" do |flask|
      flask.vm.box = "bento/centos-7.4"
      flask.vm.network "forwarded_port", guest: 8000, host: 8000
      flask.vm.network "forwarded_port", guest: 5000, host: 5000
      flask.vm.network "forwarded_port", guest: 443, host: 443
      flask.vm.network "forwarded_port", guest: 80, host: 80

      flask.vm.provider "virtualbox" do |vb|
        vb.name = 'flask-vm'
        vb.memory = 4096
        vb.cpus = 1
        vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
      end

      flask.vm.provision "shell", inline: $script
  end

  config.vm.define "docker" do |docker|
      docker.vm.box = "ubuntu/bionic64"
    #  config.vm.network "public_network",
    #    use_dhcp_assigned_default_route: true
      docker.vm.network "forwarded_port", guest: 8000, host: 8000
      docker.vm.network "forwarded_port", guest: 5000, host: 5000
      docker.vm.network "forwarded_port", guest: 443, host: 443
      docker.vm.network "forwarded_port", guest: 80, host: 80

      docker.vm.provider "virtualbox" do |vb|
        vb.name = 'docker-vm'
        vb.memory = 4096
        vb.cpus = 1
        vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
        vb.customize ["modifyvm", :id, "--natdnsproxy1", "on"]
      end

      docker.vm.provision "shell", inline: $docker_script
      docker.vm.provision :docker
      docker.vm.provision :docker_compose
  end
end



