
# Flask app implementation

There are several processes that are required to deploy the app correctly. The automation tool used to develop this activity is ansible. We need an ansible controller to ensure that the playbook developed can be carried out. Please follow the next steps:

1. Run a docker container with the ansible controller
2. Deploy the playbook from the ansible controller
3. Access to the app deployed in a EC2 instance

Requirements:

Install Docker on the baseline OS (You can use a Windows Machine, MACOS or Linux OS. Please follow the instructions)
- https://docs.docker.com/install/linux/docker-ce/ubuntu/
- https://docs.docker.com/docker-for-mac/install/
- https://docs.docker.com/docker-for-windows/install/

**1. Run a docker container with the ansible controller**

Clone repo in the local machine.
```
git clone git@github.com:victorcardonaf/python-flask-mysql-app.git python-app
cd python-app
```
Build the ansible-controller docker image:
```
docker build -t centos-ansible ansible-image/
```
After the building process, run the container:
```
docker run  --privileged  -v /sys/fs/cgroup:/sys/fs/cgroup --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --name=centos-ansible -v $(pwd):/media -dti centos-ansible
```
Go inside from the container:
```
docker exec -ti centos-ansible /bin/bash
```

**2. Deploy the playbook from the ansible controller**

Inside from the container, the first thing that is required is to modify the export_aws_variables.sh file providing the access keys to deploy resources in AWS.
```
#!/bin/bash
export AWS_REGION=us-east-1
export EC2_ACCESS_KEY=xxxxxxx
export EC2_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxx
```

After modifying the file, execute it:
``` 
source export_aws_variables.sh
```
Verify with the env command if the variables were configured correctly:
```
env
```
Now inside from the container, execute:
```
ansible-playbook -i inventory/hosts provision_aws.yml
```

This playbook will deploy resources in AWS. It will install a VPC inside from Virginia region and an EC2 t2.medium instance. In the instance will be installed Docker and Docker-compose. 


**Access to the app deployed in a EC2 instance**

```
To connect to the server, open a web browser and copy the IP address and port that appears in the file **server.txt**. In this file will be posted the public IP address of the Server after deploying the ansible playbook files.

cat server.txt:
http://server-ip:5000

```
If you require to connect via ssh to the EC2 instance (Please replace **server-ip** from the file server.txt):

```
eval $(ssh-agent)
ssh-add inventory/keys/keypair.pem
ssh ec2-user@"server-ip"
```




