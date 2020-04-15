# Installation with Platformer

## Prerequisites

### Python 3.7

You need at least Python 3.7 installed on your computer to use this tool. This is the default version for macOS Catalina and newer Linux distributions (for additional platforms and versions, please check the [Python downloads page](https://www.python.org/downloads/release/python-377/)).

### KubeCTL

For the Platformer tool to interact with the underlying Kubernetes cluster, you will need the KubeCTL binaries.

To install it in macOS, you can use [Homebrew](https://brew.sh):

```shell
brew install kubectl
```

### Azure CLI

To deploy a platform in Azure and to download the required assets, you will need the Azure CLI.

To install it in macOS, you can use [Homebrew](https://brew.sh):

```shell
brew install azure-cli
```

#### Set your Azure credentials

To allow Platformer to use your Azure credentials, you must need to set up two environment variables:

* `AZURE_USERNAME`, with your Azure account email.
* `AZURE_PASSWORD`, with your Azure account password.

You can use tools like [envchain](https://github.com/sorah/envchain) to store those environment variables in a secure way.

### NALEJ Assets

To be able to deploy a platform, you will need the required assets. To download them, just execute:

```shell
az storage blob download-batch --source https://nalejartifacts.blob.core.windows.net/v050 --destination /tmp
```

You can change the destination path to another folder in your system.


## Install Platformer

You can install the Platformer tool from the Python official repository with `pip3`:

```shell
pip3 install --user nalej-platformer
```

Please make sure that `pip3` is the correct command in your system, or if you need to use `pip` instead.

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

## Using Platfomer

Once you have Platformer installed and a plan file defined, you can execute the Platformer tool to create your Nalej platform.

To launch Platfomer, you only need to execute the following command:

```shell
nalej-platformer --resources <ASSETS_PATH> apply <PLAN_FILE>
```

You may need to replace the `ASSETS_PATH` with the path where you downloaded the Nalej assets, and the `PLAN_FILE` with the path to the plan file.

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

