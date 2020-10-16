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



## Using Platformer

Once you have Platformer installed and a plan file defined, you can execute the Platformer tool to create your Nalej platform.

To launch Platfomer, you only need to execute the following command:

```shell
nalej-platformer --platform AWS --resources <ASSETS_PATH> apply <PLAN_FILE.yaml>
```

You may need to replace the `ASSETS_PATH` with the path where you downloaded the Nalej assets, and the `PLAN_FILE` with the path to the plan file.

It takes between 20 and 25 minutes to deploy and validate the provision and installation of each cluster, depending on the time it takes to AWS to process the commands that Platformer sends. For example, for an architecture of one Management Cluster and two Application Clusters, the whole process could take a bit more than an hour.

Once Platformer finishes, the platform is deployed and ready to use. The information needed to access the platform (the URLs) will be stored in the plan file.