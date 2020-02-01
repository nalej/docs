# Installation guide

This document is structured to be executed in order. The steps to follow are:

To install a management cluster:

1. [Install the Certificate Manager.](#install-certificate-manager)
2. [Create Certificate Issuers.](#create-certificate-issuers)
3. [Execute the platform installer.](#install-the-platform)
4. [Create certificates for ingress.](#create-certificate-for-ingress)
5. [Create the organization in the platform.](#create-organization-in-the-platform)
6. [Validate the platform installation.](#validate-the-platform-installation)

To install an application cluster:

1. [Install the Certificate Manager.](#install-certificate-manager-1)
2. [Create Certificate Issuers.](#create-certificate-issuers-1)
3. [Install the application cluster.](#install-application-cluster)
4. [Create certificates for ingress.](#create-certificates-for-ingress-1)
5. [Validate the platform installation.](#validate-platform-installation-1)

## Management cluster

### Install Certificate Manager

If the system is running Kubernetes v1.15 of below,  the flag `--validate=false` needs to be added or you will receive a validation error relating to the `x-kubernetes-preserve-unknown-fields` field in our `CustomResourceDefinition` resources. This is a benign error and happens due to the way `kubectl` performs resource validation.

Before applying the manifest, check which is the latest version for cert-manager [here](https://github.com/jetstack/cert-manager/releases), and install it.

```shell
# Create namespace for cert-manager
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> create namespace cert-manager

# Install CustomResourceDefinitions and cert-manager itself
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> apply --validate=false -f https://github.com/jetstack/cert-manager/releases/download/v0.12.0/cert-manager.yaml
```

### Create Certificate Issuers

ClusterIssuer represents a certificate authority from which signed x509 certificates (such as Let’s Encrypt) can be obtained. At least one ClusterIssuer or Issuer is required in order to begin issuing certificates within a Kubernetes cluster.

The main difference between ClusterIssuer and Issuer is that ClusterIssuers do not belong to a single namespace and can be referenced by Certificate resources from different namespaces.

The `cert-manager` configuration will depend on the user’s requirements and it will be highly customized, so a standardized procedure is not provided in this guide.

The supported ClusterIssuer types are:

| Name        | Description                                                  |
| ----------- | ------------------------------------------------------------ |
| ACME        | Supports obtaining certificates from an ACME server, validating them with HTTPS01 or DNS01. |
| CA          | Supports issuing certificates using a simple signing keypair, stored in a Secret in the Kubernetes API server. |
| Vault       | Supports issuing certificates using HashiCorp Vault          |
| Self signed | Supports issuing self-signed certificates                    |
| Venafi      | Supports issuing certificates from Venafi Cloud & TPP        |

All the configuration possibilities are documented in the [cert-manager site](https://docs.cert-manager.io/en/latest/tasks/issuers/index.html). Take into account that this link refers to Issuers; to set a ClusterIssuer instead, the only difference in configuration would be to change `kind:` to `ClusterIssuer`.

For reference, below you can find the setup for Nalej, with Azure as DNS provider with Let’s Encrypt CA, and using an ACME type of ClusterIssuer. You can find the `cert-manager` official documentation regarding this situation [here](https://docs.cert-manager.io/en/latest/tasks/issuers/setup-acme/dns01/azuredns.html).
However, if this creates more doubts rather than clarify them, please check with the DevOps team the best approach for certificate management.

First we create the Secret. Here we will store the Service Principal password previously created, with access to Azure DNS, and encoded in base64.

**`#SP_Secret.yaml`**

```yaml
apiVersion: v1
kind: Secret
metadata:
	name: k8s-service-principal  
	namespace: cert-manager
data:  
	client-secret: <Base64ServicePrincipalPassword>
```

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> create -f SP_Secret.yaml
```

Then it's the turn of the ClusterIssuer. First, we define the parameters for it, like the DNS providers we are using and how to connect with them.

**`#clusterIssuer.yaml`**

```yaml
apiVersion: certmanager.k8s.io/v1alpha1
kind: ClusterIssuer
metadata:  
	name: letsencrypt
spec:
	acme:
  	server: <letsencrypt_server_URL>   
  	email: <contact_email>
    privateKeySecretRef:     
    	name: letsecrypt   
    dns01:     
    	providers:   
    		- name: azuredns       
    			azuredns:         
    				clientID: <SERVICEPRINCIPAL_ID>         
    				clientSecretRef:          
    					name: k8s-service-principal          
    					key: client-secret         
    				subscriptionID: <SUBSCRIPTIONID>         
    				tenantID: <TENANTID>         
    				resouceGroupName: <DNSRESOURCEGROUP>         
    				hostedZoneName: <AZHOSTEDZONE>     
```

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> create -f clusterIssuer.yaml
```

If the ClusterIssuer has been created correctly, this command should respond with `ACMEAccountRegistered`. 

Lastly, we can check if the ClusterIssuer has been created correctly with the command:

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> get clusterissuer letsencrypt -o jsonpath='{.status.conditions[0].reason}'
```

### Install the platform

Next, we install the Nalej Platform itself. We need to consider the following parameters before executing the `install management` command, so please be sure that you have all the information before proceeding. 

| Parameter            | Value                                                 |
| -------------------- | ----------------------------------------------------- |
| INSTALLER_PATH       | $HOME/go/src/github.com/nalej                         |
| KUBECONFIG_PATH      |                                                       |
| INGRESS_IP_ADDRESS   |                                                       |
| DNS_IP_ADDRESS       |                                                       |
| COREDNS_IP_ADDRESS   |                                                       |
| VPNSERVER_IP_ADDRESS |                                                       |
| DNS_ZONE             | nalej.io<br>nalej.tech<br>nalej.net                   |
| USER_DOMAIN          | CLUSTER_NAME.DNS_ZONE<BR>e.g: mngtcluster01nalej.tech |
| TARGET_PLATFORM      | MINIKUBE<BR>AZURE<BR>BAREMETAL                        |
| ENVIRONMENT          | PRODUCTION<BR>STAGING<BR>DEVELOPMENT                  |

Now, fill in the command parameters with the specific data you recollected.

```SHELL
<INSTALLER_PATH>/bin/installer-cli install management
	--binaryPath ~/development/ 
	--componentsPath ../<INSTALLER_PATH>/assets 
	--managementClusterPublicHost=<USER_DOMAIN> 
	--dnsClusterPublicHost=dns.<USER_DOMAIN> 
	--targetPlatform=<TARGET_PLATFORM> 
	--useStaticIPAddresses 
	--ipAddressIngress=<INGRESS_IP_ADDRESS> 
	--ipAddressDNS=<DNS_IP_ADDRESS> 
	--ipAddressCoreDNS=<COREDNS_IP_ADDRESS> 
	--ipAddressVPNServer=<VPNSERVER_IP_ADDRESS> 
	--kubeConfigPath=<MNGTKUBECONFIG_PATH> 
	--targetEnvironment=<ENVIRONMENT>
```

After that, we need to create a Secret in the Kubernetes cluster with the certificate provided by the user in advance. This will be of internal use, letting the platform communicate with Let's Encript to obtain the certificates needed for the system to work.

**`CA_Secret.yaml`**

```yaml
apiVersion: v1
kind: Secret
metadata:
   name: ca-certificate
   namespace: nalej
data:
   ca.crt: <EncodedBase64_CA_PATH>
type: Opaque
```

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> create -f - CA_Secret.yaml
```

As before, the data in the Secret is encoded in base64.

### Create Certificates for Ingress

The creation of the certificate for ingress needs to be aligned with the configuration followed in the [creation of certificate issuers](#create-certificate-issuers). Depending on the ClusterIssuer configuration, the content in the `Certificate.yaml` will change. 

Again, for Nalej with Azure as DNS provider with Let’s Encrypt CA and using an ACME type of ClusterIssuer, the file would look like this: 

**`Certificate.yaml`**

```yaml
apiVersion: certmanager.k8s.io/v1alpha1
kind: Certificate
metadata:
   name: tls-client-certificate
   namespace: nalej
spec:
   secretName: tls-client-certificate
   issuerRef: 
      name: letsencrypt
      kind: ClusterIssuer
   dnsNames:
      - '*.<USER_DOMAIN>'
   acme:
      config:
         - dns01:
              provider: azuredns
           domains:
              - '*.<USER_DOMAIN>'

```

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> create -f - Certificate.yaml
```

### Create organization in the platform

To create the organization you need the following parameters:

| Parameter            | Value                         |
| -------------------- | ----------------------------- |
| SIGNUP_PATH          | $HOME/go/src/github.com/nalej |
| ORGANIZATION_NAME    |                               |
| OWNER_EMAIL          |                               |
| OWNER_NAME           |                               |
| OWNER_PASSWORD       |                               |
| NALEJ_ADMIN_EMAIL    |                               |
| NALEJ_ADMIN_NAME     |                               |
| NALEJ_ADMIN_PASSWORD |                               |
| CA_PATH              |                               |

```shell
<SIGNUP_PATH>/bin/signup-cli signup 
	--signupAddress=signup.$1:443 
	--orgName=<ORGANIZATION_NAME> 
	--ownerEmail=<OWNER_EMAIL> 
	--ownerName=<OWNER_NAME> 
	--ownerPassword=<OWNER_PASSWORD> 
	--nalejAdminEmail=<NALEJ_ADMIN_EMAIL> 
	--nalejAdminName=<NALEJ_ADMIN_NAME> 
	--nalejAdminPassword=<NALEJ_ADMIN_PASSWORD> 
	--caPath=<CA_PATH>
```

At this point of the installation, the management cluster should be ready and login would be available both through API or browser.

### Validate the platform installation

In order to validate that the management platform has been installed correctly, run the following commands. The result for all of them should be `true`.

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> -nnalej get deployments 
	-o json | jq 'reduce .items[].spec.replicas as $replicas (0; . + $replicas) == reduce .items[].status.readyReplicas as $ready (0; . + $ready)'
```

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> -nnalej get statefulset 
	-o json | jq 'reduce .items[].spec.replicas as $replicas (0; . + $replicas) == reduce .items[].status.readyReplicas as $ready (0; . + $ready)'
```

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> -nnalej get jobs 
	-o json | jq '(.items | length) <= reduce .items[].status.succeeded as $completed (0; . + $completed)'
```

## Application Clusters

This process should be repeated for as many application clusters as the user wants to have available.

### Install certificate manager

The process is the same as in the management cluster. The only change needed is to use the application cluster `kubeconfig.yaml` file when creating the namespace and applying the manifest. 

### Create Certificate Issuers

The process is the same as in the management cluster. The only change needed is to use the application cluster `kubeconfig.yaml` file when creating the secret and the ClusterIssuer. 

### Install Application Cluster

The required parameters for this command are:

| Parameter              | Value                                                        |
| ---------------------- | ------------------------------------------------------------ |
| PUBLIC_API_PATH        | $HOME/go/src/github.com/nalej                                |
| APP_KUBECONFIG_PATH    |                                                              |
| INGRESS_APP_IP_ADDRESS |                                                              |
| APP_CLUSTER_NUMBER     | From 0 to n                                                  |
| DNS_ZONE               | nalej.io<br/>nalej.tech<br/>nalej.net                        |
| USER_DOMAIN            | USER_DOMAIN  CLUSTER_NAME.DNS_ZONE<BR>e.g: appcluster01.nalej.tech |
| TARGET_PLATFORM        | MINIKUBE<BR>AZURE<BR>BAREMETAL                               |
| CA_PATH                |                                                              |

The command we have to execute this time is:

```shell
<PUBLIC_API_PATH>/bin/public-api-cli  
	--nalejAddress=api.<USER_DOMAIN> 
	--port=443 
	cluster install 
	--targetPlatform=<TARGET_PLATFORM> 
	--ingressHostname=app<APP_CLUSTER_NUMBER>.<USER_DOMAIN> 
	--cacert=<CA_PATH> 
	--kubeConfigPath=<APP_KUBECONFIG_PATH> 
	--useStaticIPAddresses 
	--ipAddressIngress=<INGRESS_APP_IP_ADDRESS>
```

Also, in the case of the Application Cluster, the secret doesn't need to be created.

### Create certificates for ingress

 The YAML will be similar to the one for the management cluster, and the only change needed would be the `dnsNames` and `domains` parameters with the ingress domain for the application cluster.

**`Certificate.yaml`**

```yaml
apiVersion: certmanager.k8s.io/v1alpha1
kind: Certificate
metadata:
   name: tls-client-certificate
   namespace: nalej
spec:
   secretName: tls-client-certificate
   issuerRef: 
      name: letsencrypt
      kind: ClusterIssuer
   dnsNames:
      - '*.app<APP_CLUSTER_NUMBER>.<USER_DOMAIN>'
   acme:
      config:
         - dns01:
              provider: azuredns
           domains:
              - '*.app<APP_CLUSTER_NUMBER>.<USER_DOMAIN>'

```

### Validate the platform installation

In order to validate that the application cluster has been installed correctly, run the following commands. The result for all of them should be true:

```shell
kubectl --kubeconfig <APPKUBECONFIG.yaml> -nnalej get deployments 
	-o json | jq 'reduce .items[].spec.replicas as $replicas (0; . + $replicas) == reduce .items[].status.readyReplicas as $ready (0; . + $ready)'
```

```shell
kubectl --kubeconfig <APPKUBECONFIG.yaml> -nnalej get statefulset 
	-o json | jq 'reduce .items[].spec.replicas as $replicas (0; . + $replicas) == reduce .items[].status.readyReplicas as $ready (0; . + $ready)'
```

```shell
kubectl --kubeconfig <APPKUBECONFIG.yaml> -nnalej get jobs 
	-o json | jq '(.items | length) >= reduce .items[].status.succeeded as $completed (0; . + $completed)'
```



