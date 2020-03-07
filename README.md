
# Ansible and Jenkins Implementation

There are several processes that are required to deploy the app correctly. The automation tool used to develop this activity is ansible. We need an ansible controller to ensure that the playbook developed can be carried out. Please follow the next steps:

1. Run a docker container with the ansible controller
2. Deploy the playbook from the ansible controller
3. Connect to Jenkins Web Interface to create credentials and the pipeline job
4. Check the app running accessing from the web browser

Requirements:

Install Docker on the baseline OS (You can use a Windows Machine, MACOS or Linux OS. Please follow the instructions)
- https://docs.docker.com/install/linux/docker-ce/ubuntu/
- https://docs.docker.com/docker-for-mac/install/
- https://docs.docker.com/docker-for-windows/install/

**Run a docker container with the ansible controller**

Clone repo in the local machine.
```
git clone git@github.com:victorcardonaf/application.git ansible-deployment
cd ansible-deployment
```
Build the ansible-controller docker image:
```
docker build -t centos-ansible ansible-base-build/
```
After the building process, run the container:
```
docker run  --privileged  -v /sys/fs/cgroup:/sys/fs/cgroup --cap-add=SYS_ADMIN --cap-add=NET_ADMIN --name=centos-ansible -v $(pwd)/personal_project:/media -dti centos-ansible
```
Go inside from the container:
```
docker exec -ti centos-ansible /bin/bash
```

**Deploy the playbook from the ansible controller**

Inside from the container, the first thing that is required is to modify the export_aws_variables.sh file providing the access keys to deploy resources in AWS.
```
#!/bin/bash
export AWS_REGION=us-east-1
export EC2_ACCESS_KEY=xxxxxxx
export EC2_SECRET_KEY=xxxxxxxxxxxxxxxxxxxxxx
```

After modifying the file, execute it:
``` 
./export_aws_variables.sh
```
Verify with the env command if the variables were configured correctly:
```
env
```
Now inside from the container, execute:
```
ansible-playbook -i inventory/hosts provision_aws.yml
```

This playbook will deploy resources in AWS. It will install a VPC inside from Virginia region and an EC2 t2.medium instance. In the instance will be installed Java, Docker and Jenkins. 


**Connect to Jenkins Web Interface to create credentials and the pipeline job**

The Jenkins public ip can be taken from the jenkins_ip.txt file. You can see the existing value below from [jenkins]  value. This value is replaced when jenkins is deployed. 
```
example:
[jenkins]
3.80.142.181

```
To connect to the Jenkins Server, open a web browser using 8080 port and http protocol:
```
http://jenkins-ip:8080
username: admin
password: admin
```

**Configure dockerhub Credentials**

Go to Credentials -> Add Credentials -> Configure username, password, ID and Description
```
username: "username used in dockerhub"
password: "password used in dockerhub"
ID: dockerhub -> Variable used in Jenkinsfile
```
**NOTE: Please use the same value to ID. This value is used in the Jenkinsfile**


**Create the pipeline job**

New Item -> Choose pipeline project and define a job name. Define the next parameters:

```
Build Triggers Section
Check Poll SCM and put in the schedule * * * * * to check the repo each minute.
```

```
Pipeline Section
In definition choose Pipeline script from SCM
In SCM choose git
```

```
Repositories Section
Repository URL: https://github.com/victorcardonaf/application.git
```

```
Script Path Section
Ensure that Jenkinsfile appears here
```

Save Changes.The pipeline job is ready. Jenkins is now configured to deploy the app each time that a new commit occurs.

**Check the app running accessing from the web browser**

The execution of the pipeline shows you how to access to the app from the web browser according to the execution process:
```
http://jenkins-ip:3004
```


