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

### Azure CLI

To deploy a platform in Azure and to download the required assets, you will need the Azure CLI.

```shell
brew install azure-cli
```

#### Set your Azure credentials

If you're using Azure, your Azure Cloud Admin has probably provided you with an Azure account email and password. To allow Platformer to use your Azure credentials, you must set up two environment variables in your system:

* `AZURE_USERNAME`, with your Azure account email.
* `AZURE_PASSWORD`, with your Azure account password.

You can use tools like [envchain](https://github.com/sorah/envchain) to store those environment variables in a secure way.

#### Login in Azure

After setting up your credentials, you need to:

1. close the console and open it again. 
2. log in Azure, executing:

```bash
az login
```

This command will open a browser window, ask for your Azure credentials, and then redirect back to the console, where all the subscriptions you have access to will appear. These subscriptions look like this:

```json
[
  {
    "cloudName": "AzureCloud",
    "homeTenantId": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "id": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "isDefault": false,
    "managedByTenants": [],
    "name": "Master subscription",
    "state": "Enabled",
    "tenantId": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "user": {
      "name": "user@company.com",
      "type": "user"
    }
  },
  {
    "cloudName": "AzureCloud",
    "homeTenantId": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "id": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "isDefault": true,
    "managedByTenants": [],
    "name": "Microsoft Azure Sponsorship",
    "state": "Disabled",
    "tenantId": "xxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "user": {
      "name": "user@company.com",
      "type": "user"
    }
  }
]
```

Here we can see two subscriptions. One of the problems that can arise in this phase is that, looking at the `state` attribute, the default subscription is `disabled` (as we can see above). If this happens, we need to change to another one that is  `enabled`, and we will do it with:

```bash
az account set --subscription "Name of enabled subscription"
```



### NALEJ Assets

Once you are logged in to an enabled suscription, you will need the required assets to deploy a platform. To download them, just execute:

```shell
az storage blob download-batch --source https://nalejartifacts.blob.core.windows.net/v051 --destination /tmp
```

We recommend that you change the destination folder for a new one created in your user folder.

```bash
az storage blob download-batch --source https://nalejartifacts.blob.core.windows.net/v051 --destination <ASSETS_PATH>
```

It's time to give execution permissions to the binaries you just downloaded, getting into the assets folder and executing:

```bash
chmod -R +x binaries
```


## Install Platformer

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

To define the platform you want to deploy using Nalej, Platformer uses a YAML **plan file** where all the required information for a platform is defined.

The file is divided in three different parts: **management**, **organization** and **application**.

### Management

This section defines the required information for the management cluster.

```yaml
management:
  name: example-management
  kubernetes:
    nodes: 3
    version: 1.15.10
  azure:
    dnsZone: example.com
    region: West Europe
    resourceGroup: production
    vmSize: Standard_DS2_v2
  environment: production
```

The parameters in this section are:

#### name

This is the name of the cluster, and some resources will use this parameter to create their names (for example, the related Azure AKS cluster will base its name on this parameter).

#### environment

You can choose what kind of environment is in deployment (the options are: *production*, *staging* and *development*). This is mainly to tell Nalej what type of TLS certificates will be in use and some other related things.

#### kubernetes

This section defines the underlying Kubernetes requirements for the management cluster.

- **nodes**: You can choose how many nodes the management cluster will have. The minimum node count is 3.
- **version**: You can choose the Kubernetes version from the ones available at the cloud provider.

#### azure

This section defines required information for deploying the platform in Azure.

- **dnsZone**: This is the DNS Zone that Nalej will use to register the required DNS records. This DNS Zone must be registered on your Azure account.
- **region**: The Azure region where the cluster will be deployed.
- **resourceGroup**: The Azure resource group where the cluster will be deployed.
- **vmSize**: The Azure virtual machine size for the cluster nodes.

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
- name: app1-example
  organization: Example Org
  azure:
    dnsZone: example.com
    region: West Europe
    resourceGroup: production
    vmSize: Standard_DS2_v2
  kubernetes:
    nodes: 3
    version: 1.15.10
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

#### azure

This section defines required information for deploying the platform in Azure.

- **dnsZone**: This is the DNS Zone that Nalej will use to register the required DNS records. This DNS Zone must be registered on your Azure account.
- **region**: The Azure region where the cluster will be deployed.
- **resourceGroup**: The Azure resource group where the cluster will be deployed.
- **vmSize**: The Azure virtual machine size for the cluster nodes.

## Using Platformer

Once you have Platformer installed and a plan file defined, you can execute the Platformer tool to create your Nalej platform.

To launch Platfomer, you only need to execute the following command:

```shell
nalej-platformer --resources <ASSETS_PATH> apply <PLAN_FILE>
```

You may need to replace the `ASSETS_PATH` with the path where you downloaded the Nalej assets, and the `PLAN_FILE` with the path to the plan file.

It takes between 20 and 25 minutes to deploy and validate the provision and installation of each cluster, depending on the time it takes to Azure to process the commands that Platformer sends. For example, for an architecture of one Management Cluster and two Application Clusters, the whole process could take a bit more than an hour.

Once Platformer finishes, the platform is deployed and ready to use. The information needed to access the platform (the URLs) will be stored in the plan file.



## Plan file examples

These are some examples of plan files to deploy the Nalej Platform.

### One organization with two application clusters

```yaml
management:
  name: example-management
  environment: production
  azure:
    dnsZone: example.com
    region: West Europe
    resourceGroup: production
    vmSize: Standard_DS2_v2
  kubernetes:
    nodes: 3
    version: 1.15.10
organization:
- name: Example
  users:
    nalejAdmin:
      email: admin@example.com
      name: Example Administrator
      password: password
    owner:
      email: owner@example.com
      name: Example Owner
      password: password
application:
- name: app1-example
  organization: Example
  azure:
    dnsZone: example.com
    region: West Europe
    resourceGroup: production
    vmSize: Standard_DS2_v2
  kubernetes:
    nodes: 3
    version: 1.15.10
- name: app2-example
  organization: Example
  azure:
    dnsZone: example.com
    region: West Europe
    resourceGroup: production
    vmSize: Standard_DS2_v2
  kubernetes:
    nodes: 3
    version: 1.15.10
```

Here, the two application clusters are called `app1-example` and `app2-example`, and both belong to the `Example` organization declared in the same file. Both have 3 nodes, are in the same zone (West Europe) and are using the resources from the *production* group.

### Two organizations with one application cluster each

```yaml
management:
  name: example-management
  environment: production
  azure:
    dnsZone: example.com
    region: West Europe
    resourceGroup: production
    vmSize: Standard_DS2_v2
  kubernetes:
    nodes: 3
    version: 1.15.10
organization:
- name: Example
  users:
    nalejAdmin:
      email: admin@example.com
      name: Example Administrator
      password: password
    owner:
      email: owner@example.com
      name: Example Owner
      password: password
- name: Example 2
  users:
    nalejAdmin:
      email: admin2@example.com
      name: Example Administrator
      password: password
    owner:
      email: owner2@example.com
      name: Example Owner
      password: password
application:
- name: app1-example
  organization: Example
  azure:
    dnsZone: example.com
    region: West Europe
    resourceGroup: production
    vmSize: Standard_DS2_v2
  kubernetes:
    nodes: 3
    version: 1.15.10
- name: app1-example2
  organization: Example 2
  azure:
    dnsZone: example.com
    region: West Europe
    resourceGroup: production
    vmSize: Standard_DS2_v2
  kubernetes:
    nodes: 3
    version: 1.15.10
```

The two organizations here are called `Example` and `Example 2`, the two application clusters are called `app1-example` and `app2-example`, and each organization owns one cluster.

