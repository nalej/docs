# Installation with Platformer

## Prerequisites

For this tutorial we used a computer with macOS Catalina 10.15.5 and the [Homebrew package manager](https://brew.sh). These steps will create a Kubernetes cluster as part of the installation process, so you don't need to already have one.

### Python 3.7

You need at least Python 3.7 installed on your computer to use Platformer. This is the default version for macOS Catalina and newer Linux distributions (for additional platforms and versions, please check the [Python downloads page](https://www.python.org/downloads/release/python-377/)).

To check the version installed in your computer please execute:

```zsh
python3 --version
```

To install Python 3.7 or higher:

```zsh
brew install python3
```

After installing, please make sure that you have the Python `bin` folder in your local path. To check that, execute:

```bash
echo $PATH
```

If you can't see the `bin` folder in this environment variable (the path would look like this: `/Users/user/Library/Python/3.7/bin`), include it before going any further. 

### KubeCTL

For the Platformer tool to interact with the underlying Kubernetes cluster, you will need the KubeCTL binaries.

```zsh
brew install kubectl
```

### NALEJ Assets

Currently we still need to download the Nalej assets from Azure, so we recommend going to the NALEJ installation tutorial in Azure and follow the steps described there. You need to download the assets and give execution permissions to the binaries in the assets folder.

### Environment variables

The Platformer needs a couple of environment variables that need to be established before deploying an AWS environment, which are `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID`. 

The AWS Access Key and Secret Access Key can be created from the AWS Management Console. It is recommended that you create a new administrator IAM user with access keys for yourself (instead of using the root user access keys). The only time that you can view or download the secret access key is when you create the keys. You cannot recover them later. However, you can create new access keys at any time.

To establish them as variables in your system, please execute the following (changing the values to yours):

```bash
 export AWS_SECRET_ACCESS_KEY=+WZX1Y90Z2X2345YabcY6defXYZghijkXYZl78mn
 export AWS_ACCESS_KEY_ID=ASDFASDFASDFASDFASD3
```

### AWS CLI

To deploy a platform in AWS you will need the `aws-cli`. Please install it executing the following commands.

```bash
curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"

sudo installer -pkg AWSCLIV2.pkg -target /
```

After that, you need to configure the AWS CLI. Run:

```bash
aws configure 
```

 This command will prompt you for four pieces of information:

- Access key ID
- Secret access key
- AWS Region
- Output format

The Access key ID and the secret access key need to match the values in your system variables. You can consult the region in the AWS Management Console, and if you don't specify an output format, `json` is used as the default.

### Amazon Web Services 

Now that everything is installed in our computer, we need to make sure that NALEJ can be deployed in our AWS environment.

The very first thing we need to do is an account with full administrator rights. For that, in the IAM, we should go to **Users**, and there we can create the Service Admin account. Now we can start managing our resources depending on the architecture we want to deploy.

For example, for an architecture consisting on **one management cluster and two application clusters**, the resources needed would be:

#### 7 available [Elastic IPs](https://docs.aws.amazon.com/vpc/latest/userguide/vpc-eips.html). 

We need 3 EIPs for the management cluster, and 2 for each application cluster. Each AWS account has 5 EIPs for free, and then there is a small fee for each extra EIP you want to allocate. 

#### An [Internet Gateway](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Internet_Gateway.html). 

This component routes traffic between the outside world and your architecture. AWS accounts come with this already set up, so just make sure you have it before moving on.

#### 3 [Subnets](https://docs.aws.amazon.com/vpc/latest/userguide/working-with-vpcs.html).

Under the VPC section, go to Subnets, and once you're there create 3 subnets: one of them public, the other 2 private. 

Take into account that the public subnet and one of the private subnets need to share the same availability zone. The other private subnet doesn't need to share it too.

#### An [EKS security Group](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_SecurityGroups.html) created in the VPC.

Under the VPC section, go to Security, and then go to Security Group. There, you should be able to create one. Its configuration should be as follows:

- **Inbound**: all traffic, all protocols, all range, the source is the ID of the security group.

- **Outbound**: all traffic, all protocols, all range, the destination is 0.0.0.0/0

This is a requirement for the Platformer, so make sure you write down the group ID to use later when you work with it.

#### Roles to add to the system

##### EKS Cluster Role – EKS Service

Under IAM you need to go to the Roles section. There, you should create a new one, select the EKS service (in the services list, click on EKS and then again on EKS), and call it **EKS Cluster Role**. When this is done, you need to attach the following policy:

* Amazon EKS Cluster Policy.

##### EKS Node Group Role – EC2 Service 

To add worker nodes to an Amazon EKS cluster, you need to create an EKS Node Group Role with the following policies attached:

- Amazon EKS Worker Node Policy 
- Amazon EC2 Container Registry Read Only
- Amazon EKS CNI Policy

Again, under IAM you go to the Roles section and create a new Role. This time, you need to select the EC2 service, and call it the **EKS Node Group Role**. After that, just attach the policies stated above.



## Installing Platformer

!!! note "Deprecated information!"
    Currently, the `platformer` package in `pip` is not updated. Please ask for the updated package to the Nalej team, and install it with `python setup.py install`.

Now it's time to install the Platformer tool from the Python official repository. But first, we need to check our package administration tool. We can use `pip` or `pip3`, and the difference resides in the version of Python the command is using. To be sure we're using the correct command, we need to execute:

```bash
pip --version

pip3 --version
```

The responses to these two commands will tell us the command's version of Python, and we will choose the command that uses Python 3.7 or higher. In this tutorial we will be using `pip3`.

```shell
pip3 install --user nalej-platformer
```

Please remember to NOT use `sudo pip install`, and manage your dependencies correctly (you can find more information about this topic [here](https://dev.to/elabftw/stop-using-sudo-pip-install-52mn)).

## The platform plan file

To define the platform you want to deploy using Nalej, Platformer uses a YAML **plan file** where all the required information for a platform is defined. We recommend to keep a copy of the plan file as a backup, in case something goes wrong during the installation.

The file is divided in three different parts: **management**, **organization** and **application**.

### Management

This section defines the required information for the management cluster.

```yaml
management:
  aws:
    awsEksSecurityGroup: xx-00x00xx0xx0x00x0
    awsHostedZoneID: Z00427232C000TM14LMST
    awsNodeRole: arn:aws:iam::396651306611:role/EKSNodeGroupRole
    awsNodeType: t3a.medium
    awsRegion: eu-west-2
    controlPlaneRole: arn:aws:iam::396651306611:role/EKSClusterRole
    dnsZoneName: aws.nalejlabs.io
    privateSubnets: subnet-0d63cb0f7d7b32875,subnet-0a87c5184dd9d7522
    publicSubnets: subnet-03c570fa33be1ded9
    route53Region: eu-west-2
    vpcID: vpc-0c836f541e9afe76f
  environment: development
  kubernetes:
    nodes: 5
    version: 1.16
  name: mymanager
```

The parameters in this section are:

#### name

This is the name of the cluster, and some resources will use this parameter to create their names.

#### environment

You can choose what kind of environment is in deployment (the options are: *production*, *staging* and *development*). This is mainly to tell Nalej what type of TLS certificates will be in use and other parameters related to this.

#### kubernetes

This section defines the underlying Kubernetes requirements for the management cluster.

- **nodes**: You can choose how many nodes the management cluster will have. The minimum node count is 3.
- **version**: You can choose the Kubernetes version from the ones available at the cloud provider.

#### aws

This section defines required information for deploying the platform in AWS:

- **awsEksSecurityGroup**: the EKS security group ID.
- **awsHostedZoneID**: the hosted zone ID.
- **awsNodeRole**: the EKS Node Group Role you created before.
- **awsNodeType**: the type of machine that will be reserved. For more information regarding this paramenter, please take a look at the [official Amazon EC2 Instance Types documentation](https://aws.amazon.com/ec2/instance-types/).
- **awsRegion**: the region where the clusters will be located.
- **controlPlaneRole**: the EKS Cluster Role you created before.
- **dnsZoneName**: This is the DNS Zone that Nalej will use to register the required DNS records. This DNS Zone must be registered on your AWS account.
- **privateSubnets**: The private subnets available. There must be two. 
- **publicSubnets**: The public subnets available.
- **route53Region**: The Route 53 region should be the same in the management cluster and in the application clusters. If you want them to be different, be aware that you will need to modify the Route 53 configuration in order to make it work.
- **vpcID**: The VPC where the subnets are declared.

### Organization

This section defines the list of organizations that will be created in the platform.

```yaml
organization:
- name: Example Org
  users:
    nalejAdmin:
      email: admin@example.com
      name: Example admin
      password: password
    owner:
      email: owner@example.com
      name: Example owner
      password: password
```

This is how the Organization section looks like. You can create as many organizations as you need, adding them as a list in this scheme.

#### name

Name of the organization.

#### users

This section defines the two main users for this organization, the **Nalej Administrator** and the **Organization Owner**. For both users you need to define their name, email and password.

**IMPORTANT**: The password is stored in this file in plain text, but these password are not transferred or stored anywhere else. We encourage you to secure this file properly.

### Application

This section defines the list of application clusters that will be deployed for the platform.

```yaml
application:
- aws:
    awsEksSecurityGroup: sg-0314a6d6451927f41
    awsHostedZoneID: Z00427232C000TM14LMST
    awsNodeRole: arn:aws:iam::396651306611:role/EKSNodeGroupRole
    awsNodeType: t3a.medium
    awsRegion: eu-west-2
    controlPlaneRole: arn:aws:iam::396651306611:role/EKSClusterRole
    dnsZoneName: aws.nalejlabs.io
    privateSubnets: subnet-0c606fc07b8b2dcea,subnet-09be4d63bf4992908
    publicSubnets: subnet-0d90fb2b7d51660c2
    route53Region: eu-west-2
    vpcID: vpc-05140aa4172996ef6
  environment: development
  kubernetes:
    nodes: 3
    version: 1.16
  name: mycluster1
  organization: Nalej
```

This is how the Application section looks like. You can create as many application clusters as you may need, adding them as a list in this scheme.

#### name

Name of this application cluster.

#### organization

This is the name of the organization that owns this application cluster. This name needs to match one of the organizations defined in the Organization section.

#### kubernetes

This section defines the underlying Kubernetes requirements for the management cluster.

- **nodes**: You can choose how many nodes the management cluster will have. The minimum node count is 3.
- **version**: You can choose the Kubernetes version from the ones available at the cloud provider.

#### aws

This section defines required information for deploying the platform in AWS. These parameters should coincide with the parameters already defined in the management section. If they do not, please be aware that there will be conflicts in the configuration of AWS that you will need to address.

## Using Platformer

Once you have Platformer installed and a plan file defined, you can execute the Platformer tool to create your Nalej platform.

To launch Platfomer, you only need to execute the following command:

```shell
nalej-platformer --platform AWS --resources <ASSETS_PATH> apply <PLAN_FILE.yaml>
```

You need to replace the `ASSETS_PATH` with the path where you downloaded the Nalej assets, and the `PLAN_FILE` with the path to the plan file.

It takes between 20 and 25 minutes to deploy and validate the provision and installation of each cluster, depending on the time it takes to AWS to process the commands that Platformer sends. For example, for an architecture of one Management Cluster and two Application Clusters, the whole process could take a bit more than an hour.

Once Platformer finishes, the platform is deployed and ready to use. The information needed to access the platform (the URLs) will be stored in the plan file.



## AWSGov: Special information

If you are deploying the platform for AWSGov, there are some modifications to be made to this process.

### Platform plan file

The platform plan file is a bit different, because every time `aws:` appears (in the management and application sections, at the beginning of the description of each cluster) it has to be substituted by `awsGov:`. The rest of the platform plan stays the same.

### Environment variables

Apart from including `AWS_SECRET_ACCESS_KEY` and `AWS_ACCESS_KEY_ID`, you will need two variables more, which are `AWS_STANDARD_SECRET_ACCESS_KEY` and `AWS_STANDARD_ACCESS_KEY`. You will have access to these two variables when you have access to the AWS Gov environment.

To establish them as variables in your system, please execute the following (changing the values to yours):

```bash
 export AWS_SECRET_ACCESS_KEY=XXXXXXXXXXXXXXX
 export AWS_ACCESS_KEY_ID=XXXXXXXXXXXXXXX
 export AWS_STANDARD_SECRET_ACCESS_KEY=XXXXXXXXXXXX
 export AWS_STANDARD_ACCESS_KEY=XXXXXXXXXXXXXXX
```

### Using Platformer

Once Platformer is installed, the plan file is checked, and the environment variables are in place, to launch Platfomer, you only need to execute the following command:

```shell
nalej-platformer --platform AWSGOV --resources <ASSETS_PATH> apply <GOV_PLAN_FILE.yaml>
```

You need to replace the `ASSETS_PATH` with the path where you downloaded the Nalej assets, and the `GOV_PLAN_FILE` with the path to the plan file.

## Plan file examples

For an architecture of two application clusters and one management cluster in one organization, these are the plan files for AWS and AWSGov.

### AWS plan file

```yaml
application:
- aws:
    awsEksSecurityGroup: sg-XXXXXXXXXXXXXX
    awsHostedZoneID: XXXXXXXXXXXXXX
    awsNodeRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSNodeGroupRole
    awsNodeType: t3a.medium
    awsRegion: eu-west-2
    controlPlaneRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSClusterRole
    dnsZoneName: aws.XXXXXXXXXXXXXX.com
    privateSubnets: subnet-XXXXXXXXXXXXXX,subnet-YYYYYYYYYYYYYY
    publicSubnets: subnet-ZZZZZZZZZZZZZZZ
    route53Region: eu-west-2
    vpcID: vpc-XXXXXXXXXXXXXX
  environment: development
  kubernetes:
    nodes: 3
    version: 1.16
  name: mycluster1
  organization: Nalej
- aws:
    awsEksSecurityGroup: sg-XXXXXXXXXXXXXX
    awsHostedZoneID: XXXXXXXXXXXXXX
    awsNodeRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSNodeGroupRole
    awsNodeType: t3a.medium
    awsRegion: eu-west-1
    controlPlaneRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSClusterRole
    dnsZoneName: aws.nalejlabs.io
    privateSubnets: subnet-XXXXXXXXXXXXXX,subnet-YYYYYYYYYYYYYY
    publicSubnets: subnet-ZZZZZZZZZZZZZZZ
    route53Region: eu-west-2
    vpcID: vpc-XXXXXXXXXXXXXX
  environment: development
  kubernetes:
    nodes: 3
    version: 1.16
  name: mycluster2
  organization: Nalej
management:
  aws:
    awsEksSecurityGroup: sg-XXXXXXXXXXXXXX
    awsHostedZoneID: XXXXXXXXXXXXXX
    awsNodeRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSNodeGroupRole
    awsNodeType: t3a.medium
    awsRegion: eu-west-2
    controlPlaneRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSClusterRole
    dnsZoneName: aws.nalejlabs.io
    privateSubnets: subnet-XXXXXXXXXXXXXX,subnet-YYYYYYYYYYYYYY
    publicSubnets: subnet-ZZZZZZZZZZZZZZZ
    route53Region: eu-west-2
    vpcID: vpc-XXXXXXXXXXXXXX
  environment: development
  kubernetes:
    nodes: 5
    version: 1.16
  name: mymanager
organization:
- name: Nalej
  users:
    nalejAdmin:
      email: admin@nalej.tech
      name: Example Administrator
      password: password
    owner:
      email: owner@nalej.tech
      name: Example Owner
      password: password
```



### AWSGov plan file

```yaml
application:
- awsGov:
    awsEksSecurityGroup: sg-XXXXXXXXXXXXXX
    awsHostedZoneID: XXXXXXXXXXXXXX
    awsNodeRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSNodeGroupRole
    awsNodeType: t3a.medium
    awsRegion: eu-west-2
    controlPlaneRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSClusterRole
    dnsZoneName: aws.XXXXXXXXXXXXXX.com
    privateSubnets: subnet-XXXXXXXXXXXXXX,subnet-YYYYYYYYYYYYYY
    publicSubnets: subnet-ZZZZZZZZZZZZZZZ
    route53Region: eu-west-2
    vpcID: vpc-XXXXXXXXXXXXXX
  environment: development
  kubernetes:
    nodes: 3
    version: 1.16
  name: mycluster1
  organization: Nalej
- awsGov:
    awsEksSecurityGroup: sg-XXXXXXXXXXXXXX
    awsHostedZoneID: XXXXXXXXXXXXXX
    awsNodeRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSNodeGroupRole
    awsNodeType: t3a.medium
    awsRegion: eu-west-1
    controlPlaneRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSClusterRole
    dnsZoneName: aws.nalejlabs.io
    privateSubnets: subnet-XXXXXXXXXXXXXX,subnet-YYYYYYYYYYYYYY
    publicSubnets: subnet-ZZZZZZZZZZZZZZZ
    route53Region: eu-west-2
    vpcID: vpc-XXXXXXXXXXXXXX
  environment: development
  kubernetes:
    nodes: 3
    version: 1.16
  name: mycluster2
  organization: Nalej
management:
  awsGov:
    awsEksSecurityGroup: sg-XXXXXXXXXXXXXX
    awsHostedZoneID: XXXXXXXXXXXXXX
    awsNodeRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSNodeGroupRole
    awsNodeType: t3a.medium
    awsRegion: eu-west-2
    controlPlaneRole: arn:aws:iam::XXXXXXXXXXXXXX:role/EKSClusterRole
    dnsZoneName: aws.nalejlabs.io
    privateSubnets: subnet-XXXXXXXXXXXXXX,subnet-YYYYYYYYYYYYYY
    publicSubnets: subnet-ZZZZZZZZZZZZZZZ
    route53Region: eu-west-2
    vpcID: vpc-XXXXXXXXXXXXXX
  environment: development
  kubernetes:
    nodes: 5
    version: 1.16
  name: mymanager
organization:
- name: Nalej
  users:
    nalejAdmin:
      email: admin@nalej.tech
      name: Example Administrator
      password: password
    owner:
      email: owner@nalej.tech
      name: Example Owner
      password: password
```

