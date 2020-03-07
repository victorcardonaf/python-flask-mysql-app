FROM centos:7

# This bit is exactly as per the documentation and can be stuck
# existing Dockerfiles without issue
ENV container docker
RUN (cd /lib/systemd/system/sysinit.target.wants/; for i in *; do [ $i == \
  systemd-tmpfiles-setup.service ] || rm -f $i; done); \
  rm -f /lib/systemd/system/multi-user.target.wants/*;\
  rm -f /etc/systemd/system/*.wants/*;\
  rm -f /lib/systemd/system/local-fs.target.wants/*; \
  rm -f /lib/systemd/system/sockets.target.wants/*udev*; \
  rm -f /lib/systemd/system/sockets.target.wants/*initctl*; \
  rm -f /lib/systemd/system/basic.target.wants/*;\
  rm -f /lib/systemd/system/anaconda.target.wants/*;
VOLUME [ "/sys/fs/cgroup" ]

RUN echo "root:viticor" | chpasswd

# In case it isn't obvious, you do NOT need httpd, it is only
# an example implementation so can be safely ignored.
RUN yum groupinstall -y "Development Tools" && yum -y install make && yum -y install wget
WORKDIR /opt/
RUN yum -y install zlib-devel libffi-devel
RUN wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz 
RUN tar -xzf Python-3.7.2.tgz
RUN cd Python-3.7.2 && ./configure --enable-optimizations
RUN cd /opt/Python-3.7.2 && make altinstall
RUN yum -y install httpd; yum -y install openssh-server openssh-clients; yum clean all; yum -y install sudo; yum -y install net-tools; yum -y install telnet; yum -y install git
RUN yum -y install epel-release; yum -y install ansible; yum -y install gcc git python-pip python-devel libffi-devel openssl-devel; pip install setuptools --upgrade; yum install make; pip install packaging; 
RUN cd /opt && git clone https://github.com/ansible/ansible.git --recursive  
RUN cd /opt/ansible && make install  
RUN yum -y install vim
RUN pip install boto3 boto
ENV ANSIBLE_HOST_KEY_CHECKING=False
RUN echo "docker-admin-ansible" > /etc/hostname
#ADD files/ssh_config /etc/ssh/ssh_config

# You HAVE to enable your service PRIOR to calling "init"
# since the init call is what ultimately fires it up
RUN systemctl enable sshd.service

# Again, no need to expose port 80, it is used as part of the
# example implementation
EXPOSE 22

VOLUME /media
WORKDIR /media

RUN echo "alias python=/usr/local/bin/python3.7" >> /root/.bashrc && source /root/.bashrc

#ENTRYPOINT systemctl ssh start && /bin/sh

# This here does the magic and starts your service
CMD ["/usr/sbin/init"]
