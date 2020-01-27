# Prerequisites

## Engineer's laptop

- Confirm that `kubectl` is correctly configured in your Mac (run in your terminal `kubectl` version). If it is not, follow the installation guide for macOS in the following link: https://kubernetes.io/docs/tasks/tools/install-kubectl/
- Confirm that `go` and `dep` are installed in your Mac.

| Validate installation commands | Installation commands | Env Variables                                            |
| ------------------------------ | --------------------- | -------------------------------------------------------- |
| go version                     | brew install go       | export GOPATH=$HOME/go<br/>export PATH=$PATH:$GOPATH/bin |
| dep version                    | brew install dep      |                                                          |

- The user should provide `kubeconfig.yml` file for management and application clusters

- To download all the assets and Nalej CLIs, the user should execute the following command:

  ```bash
  az storage blob download-batch 
  --source https://nalejartifacts.blob.core.windows.net/edge 
  --destination /tmp/nalej-edge/
  ```

  Where `/tmp/nalej-edge/` is the folder where everything will be stored, and as such can be modified.

- In order to run the script for updating Persistent Volume (that is, Kubernetes' persistent storage), the Python YAML library would be required.

### List of required components for a Nalej Platform installation

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

### Requirements sheet

| parameter                 | value                                                     |
| ------------------------- | --------------------------------------------------------- |
| INSTALLER_PATH            | `$HOME/go/src/github.com/nalej`                           |
| MNGT_KUBECONFIG_PATH      |                                                           |
| MNGT_INGRESS_IP_ADDRESS   |                                                           |
| MNGT_DNS_IP_ADDRESS       |                                                           |
| MNGT_VPNSERVER_IP_ADDRESS |                                                           |
| DNS_ZONE                  | nalej.io<BR>nalej.tech<BR>nalej.net                       |
| USER_DOMAIN               | <CLUSTERNAME>.<DNS_ZONE><BR>e.g: mngtcluster01.nalej.tech |
| TARGET_PLATFORM           | MINIKUBE<BR>AZURE<BR>BAREMETAL                            |
| ENVIRONMENT               | PRODUCTION<BR>STAGING<BR>DEVELOPMENT                      |

| parameter                  | value                           |
| -------------------------- | ------------------------------- |
| SIGNUP_PATH                | `$HOME/go/src/github.com/nalej` |
| ORGANIZATION_NAME          |                                 |
| OWNER_EMAIL                |                                 |
| OWNER_NAME                 |                                 |
| OWNER_PASSWORD             |                                 |
| NALEJ_ADMIN_EMAIL          |                                 |
| NALEJ_ADMIN_NAME           |                                 |
| NALEJ_ADMING_PASSWORD      |                                 |
| CA_PATH                    |                                 |
| PUBLIC_API_PATH            | `$HOME/go/src/github.com/nalej` |
| APP_KUBECONFIG_PATH        |                                 |
| APP_INGRESS_APP_IP_ADDRESS |                                 |
| APP_CLUSTER_NUMBER         | From 0 to n                     |

## User's infrastructure

### Hardware

The baseline scenario will require 6 different servers (bare metal or VM instances) with the following specifications:

- **CPU**: 2 CPU Cores (Intel® Xeon® E5-2673 v4 2.3 GHz or similar).
- **RAM**: 8 GB.
- **Storage**:
  - 30 GB for OS storage.
  - 100 GB for additional storage.

### OS and software

The on-premise installation of the Nalej Platform has been tested in **Ubuntu 18.04.3 LTS**. The **Kubernetes version** required is **1.11** or higher.

The user should provide **at least 5 IP addresses** (4 for management use, 1 for application use), although **we recommend 9** (6 for management use, 3 for application use). DNS records need to be set before starting the installation.

| service               | ip address | dns records                                                  |
| --------------------- | ---------- | ------------------------------------------------------------ |
| Mngt Ingress IP add   |            | A: <CLUSTERNAME>.<DNS_ZONE><BR>A: *.<CLUSTERNAME>.<DNS_ZONE> |
| Mngt DNS IP add       |            | A: dns.<CLUSTERNAME>.<DNS_ZONE>                              |
| Mngt CoreDNS IP add   |            | A: app-dns.<CLUSTERNAME>.<DNS_ZONE><br>NS: ep.<CLUSTERNAME>.<DNS_ZONE><br>app-dns.<CLUSTERNAME>.<DNS_ZONE> |
| Mngt VPNserver IP add |            | A: vpn-server.<CLUSTERNAME>.<DNS_ZONE>                       |
| App Ingress IP add    |            | A: app<APP_CLUSTER_NUMBER>.<CLUSTERNAME>.<DNS_ZONE><BR>A: *.app<APP_CLUSTER_NUMBER>.<CLUSTERNAME>.<DNS_ZONE> |

