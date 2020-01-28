# Installation steps

## Management cluster

### Install Certificate Manager

If the system is running Kubernetes v1.15 of below,  the flag `--validate=false` needs to be added or you will receive a validation error relating to the `x-kubernetes-preserve-unknown-fields` field in our `CustomResourceDefinition` resources. This is a benign error and occurs due to the way `kubectl` performs resource validation.

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

For reference, below you can find the setup for Nalej when using Azure as DNS provider with Let’s Encrypt CA. You can find the `cert-manager` official documentation regarding this situation [here](https://docs.cert-manager.io/en/latest/tasks/issuers/setup-acme/dns01/azuredns.html).
However, if this creates more doubts rather than clarify them, please check with the DevOps team the best approach for certificate management.

First we create the Secret.

**`#SP_Secret.yaml`**

```yaml
apiVersion: v1
kind: Secret
metadata:
	name: k8-service-principal  
	namespace: cert-manager
data:  
	client-secret: <Base64ServicePrincipalPassword>
```

`client-secret` will be the service principal password previously created, with access to Azure DNS, and encoded in base64.

After that, we create the signing keypair with the Secret.

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> create -f SP_Secret.yaml
```

Then it's the turn of the ClusterIssuer.

**#clusterIssuer.yaml`**

```yaml
apiVersion: certmanager.k8s.io/v1alpha1
kind: ClusterIssuer
metadata:  
	name: letsencrypt
spec:
	acme:
  	server: <letsencrypt_server_URL>   
  	email: email@nalej.com
    privateKeySecretRef:     
    	name: letsecrypt   
    dns01:     
    	providers:   
    		- name: azuredns       
    			azuredns:         
    				clientID: <SERVICEPRINCIPAL_ID>         
    				clientSecretRef:          
    					name: k8-service-principal          
    					key: client-secret         
    				subscriptionID: <SUBSCRIPTIONID>         
    				tenantID: <TENANTID>         
    				resouceGroupName: <DNSRESOURCEGROUP>         
    				hostedZoneName: <AZHOSTEDZONE>     
```

We create the ClusterIssuer from that YAML file.

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> create -f clusterIssuer.yaml
```

If the ClusterIssuer has been created correctly, this command should respond with `ACMEAccountRegistered`.

Lastly, we can check if the ClusterIssuer has been created correctly with the command:

```shell
kubectl --kubeconfig <MNGTKUBECONFIG.yaml> get clusterissuer letsencrypt -ojsonpath='{.status.conditions[0].reason}'
```



