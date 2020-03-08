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

RUN echo "root:root" | chpasswd

# In case it isn't obvious, you do NOT need httpd, it is only
# an example implementation so can be safely ignored.
RUN yum groupinstall -y "Development Tools" && yum -y install make wget
WORKDIR /opt/
RUN yum -y install zlib-devel libffi-devel
RUN yum -y install httpd openssh-server openssh-clients; yum clean all; yum -y install sudo net-tools telnet;
RUN yum --enablerepo=extras install epel-release && yum clean all; yum install -y makecache gcc git python-devel libffi-devel openssl-devel; yum -y install make;
RUN yum install -y python-setuptools python-setuptools-devel; easy_install pip;
RUN pip install packaging boto3 boto; pip install setuptools --upgrade;
RUN yum install -y ansible;
ENV ANSIBLE_HOST_KEY_CHECKING=False

# You HAVE to enable your service PRIOR to calling "init"
# since the init call is what ultimately fires it up
RUN systemctl enable sshd.service
# Again, no need to expose port 80, it is used as part of the
# example implementation
EXPOSE 22

VOLUME /media
WORKDIR /media

#ENTRYPOINT systemctl ssh start && /bin/sh

# This here does the magic and starts your service
CMD ["/usr/sbin/init"]
