# -*- mode: ruby -*-
# vi: set ft=ruby :

$script = <<-SCRIPT

    if [ ! -e /etc/pki/ca-trust/source/anchors/zscaler.cer ]
    then
        cp /vagrant/Zscaler.cer /etc/pki/ca-trust/source/anchors/zscaler.cer
        update-ca-trust
    fi

    yum -y install python3-pip

    pip3 install --upgrade pip
    pip3 install wheel
    pip3 install -r /vagrant/vagrant-requirements.txt

    # Eschew zScaler
    if ! grep -q 'zscaler.pem' /home/vagrant/.bashrc
    then
       echo 'export HTTPLIB2_CA_CERTS=/vagrant/zscaler.pem' >> /home/vagrant/.bashrc
       echo 'export SSL_CERT_FILE=/vagrant/zscaler.pem' >> /home/vagrant/.bashrc
       echo 'export REQUESTS_CA_BUNDLE=/vagrant/zscaler.pem' >> /home/vagrant/.bashrc
    fi

SCRIPT

$docker_script = <<-SCRIPT

    if [ ! -e /etc/pki/ca-trust/source/anchors/zscaler.cer ]
    then
        cp /vagrant/Zscaler.cer /etc/pki/ca-trust/source/anchors/zscaler.cer
        sudo update-ca-trust
    fi

    # Eschew zScaler
    if ! grep -q 'zscaler.pem' /home/vagrant/.bashrc
    then
        echo 'export HTTPLIB2_CA_CERTS=/vagrant/zscaler.pem' >> /home/vagrant/.bashrc
        echo 'export HTTPLIB2_CA_CERTS=/vagrant/zscaler.pem' >> ~/.bashrc

        echo 'export SSL_CERT_FILE=/vagrant/zscaler.pem' >> /home/vagrant/.bashrc
        echo 'export SSL_CERT_FILE=/vagrant/zscaler.pem' >> ~/.bashrc

        echo 'export REQUESTS_CA_BUNDLE=/vagrant/zscaler.pem' >> /home/vagrant/.bashrc
        echo 'export REQUESTS_CA_BUNDLE=/vagrant/zscaler.pem' >> ~/.bashrc

    fi

    if ! which docker
    then
        curl -fsSL https://get.docker.com | sudo bash -s
        systemctl enable docker
        systemctl start docker
        usermod -aG docker vagrant
    fi

    if ! which docker-compose
    then
        yum install -y python3-pip
        pip3 install docker-compose
    fi


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
      docker.vm.box = "bento/centos-7.4"
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
  end
end



