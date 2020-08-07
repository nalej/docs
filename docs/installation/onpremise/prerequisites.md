# Getting started

There are several things you have to consider if you decide to install Nalej platform in a server of your own, instead of in the cloud. In the following tutorials, we are going to walk you through the on-premise platform installation process

## Engineer's laptop

Your laptop must have the following tools already installed:

| Tool      | Check if installed with... | Install with...                                              | Env Variables                                                |
| --------- | -------------------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| `kubectl` | `kubectl version`          | [Installation guide for macOS](https://kubernetes.io/docs/tasks/tools/install-kubectl/). |                                                              |
| `go`      | `go version`               | `brew install go`                                            | `export GOPATH=$HOME/go`<br/>`export PATH=$PATH:$GOPATH/bin` |
| `dep`     | `dep version`              | `brew install dep`                                           |                                                              |

The `kubeconfig.yml` file will be needed for management and application clusters, so please locate it and be ready to provide it when the moment comes.

Also, in order to run the script for updating Persistent Volume (that is, Kubernetes' persistent storage), the **Python YAML library** will also be required.

To download all the assets and Nalej CLIs, you need to execute the following command:

```bash
az storage blob download-batch 
--source https://nalejartifacts.blob.core.windows.net/edge 
--destination /tmp/nalej-edge/
```

Here, `/tmp/nalej-edge/` is the folder where everything will be stored, and as such can be modified.

### List of required components for a Nalej Platform installation

The following is the list of tools that will be downloaded (but not installed yet) after executing that last command. 

- nalej-bus
  - pulsar
- dns-server
- device-controller
- connectivity-manager
- public-api
- app-cluster-api
- user-manager
- authx
- application-manager
- device-api
- infrastructure-manager
- device-manager
- edge-controller
- eic-api
- signup
- system-mode
- edge-inventory-proxy
  - edge-inventory-proxy
  - eip-sidecar
- inventory-manager
- conductor
  - conductor
  - monitoring
  - musician
- cluster-api
- network-manager
- deployment-manager
- unified-logging
  - unified-logging-coord
  - unified-logging-slave
- vpn-server
- monitoring
  - metrics-collector
  - monitoring-manager
- installer
- connectivity-checker
- device-login-api
- login-api
- web
- provisioner
- coredns-nalej-plugin
  - core-dns
- scylla-deploy
  - scylla
- zt-nalej

### Configuration parameters

The platform needs some parameters already established before proceeding with the installation. Some of them must contain a specific value, and others will be filled during the installation, but all of them need to be created beforehand. 

| Parameter                 | Value                                                  |
| ------------------------- | ------------------------------------------------------ |
| INSTALLER_PATH            | `$HOME/go/src/github.com/nalej`                        |
| MNGT_KUBECONFIG_PATH      |                                                        |
| MNGT_INGRESS_IP_ADDRESS   |                                                        |
| MNGT_DNS_IP_ADDRESS       |                                                        |
| MNGT_VPNSERVER_IP_ADDRESS |                                                        |
| DNS_ZONE                  | nalej.io<BR>nalej.tech<BR>nalej.net                    |
| USER_DOMAIN               | CLUSTER_NAME.DNS_ZONE<BR>e.g: mngtcluster01.nalej.tech |
| TARGET_PLATFORM           | MINIKUBE<BR>AZURE<BR>BAREMETAL                         |
| ENVIRONMENT               | PRODUCTION<BR>STAGING<BR>DEVELOPMENT                   |

| parameter              | value                           |
| ---------------------- | ------------------------------- |
| SIGNUP_PATH            | `$HOME/go/src/github.com/nalej` |
| ORGANIZATION_NAME      |                                 |
| OWNER_EMAIL            |                                 |
| OWNER_NAME             |                                 |
| OWNER_PASSWORD         |                                 |
| NALEJ_ADMIN_EMAIL      |                                 |
| NALEJ_ADMIN_NAME       |                                 |
| NALEJ_ADMING_PASSWORD  |                                 |
| CA_PATH                |                                 |
| PUBLIC_API_PATH        | `$HOME/go/src/github.com/nalej` |
| APP_KUBECONFIG_PATH    |                                 |
| APP_INGRESS_IP_ADDRESS |                                 |
| APP_CLUSTER_NUMBER     | From 0 to n                     |

## Infrastructure

Now we need to talk about what is needed to install Nalej in terms of equipment and software.

### Hardware

The baseline scenario will require **6 different servers** (bare metal or VM instances) with the following specifications:

- **CPU**: 2 CPU Cores (Intel® Xeon® E5-2673 v4 2.3 GHz or similar).
- **RAM**: 8 GB.
- **Storage**:
  - 30 GB for OS storage.
  - 100 GB for additional storage.

### OS and software

The on-premise installation of the Nalej Platform has been tested in **Ubuntu 18.04.3 LTS**. The **Kubernetes version** required is **1.11** or higher.

The user should provide **at least 5 IP addresses** (4 for management and 1 for application), although **we recommend 9** (6 for management and 3 for application). DNS records need to be set before starting the installation.

| service               | ip address | dns records                                                  |
| --------------------- | ---------- | ------------------------------------------------------------ |
| Mngt Ingress IP add   |            | A: CLUSTER_NAME.DNS_ZONE<BR>A: *.CLUSTER_NAME.DNS_ZONE       |
| Mngt DNS IP add       |            | A: dns.CLUSTER_NAME.DNS_ZONE                                 |
| Mngt CoreDNS IP add   |            | A: app-dns.CLUSTER_NAME.DNS_ZONE<br>NS: ep.CLUSTER_NAME.DNS_ZONE<br>app-dns.CLUSTER_NAME.DNS_ZONE |
| Mngt VPNserver IP add |            | A: vpn-server.CLUSTER_NAME.DNS_ZONE                          |
| App Ingress IP add    |            | A: appAPP_CLUSTER_NUMBER.CLUSTER_NAME.DNS_ZONE<BR>A: *.appAPP_CLUSTER_NUMBER.CLUSTER_NAME.DNS_ZONE |

