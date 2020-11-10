# Application cluster installation

## Previous structure in the system

This installation requires that there is already:

* a Kubernetes cluster available, where the structure for a Nalej application cluster will be installed.
* working connectivity between the Nalej management cluster and this brand new Kubernetes cluster.

The management cluster must know that an application cluster will be installed, and the user must log in the system with a role that allows them to execute the required actions.

Currently the platform supports adding Azure Kubernetes clusters as application clusters.

## Installation of an application cluster

For this process, we need some information from the Nalej management department, which is a configuration file for the Kubernetes cluster. This configuration file is commonly called **kubeconfig**, it's a YAML file, and it contains all the information the cluster needs to be configured as an application cluster.

Once we have this file, we can execute the installation command, which is:

```bash
./bin/public-api-cli cluster install 
    --targetPlatform=AZURE 
    --ingressHostname=<new_appcluster_url> 
    --kubeConfigPath=/path/to/kubeconfig_file.yaml 
    --useStaticIPAddresses 
    --ipAddressIngress=<static_ip_address>
```

Which uses these parameters:

* **targetPlatform** indicates the platform of the cluster, between `minikube`,  `azure` and `aws` \(default `minikube`\).
* **ingressHostname** states the new URL for the application cluster. This URL must be unique in the system.
* **kubeConfigPath** indicates the path to the configuration file mentioned above. Notice that the kubeconfig file must contain a single entry for the new cluster.

These are the mandatory parameters. There are two more optional ones:

* **useStaticIPAddresses**, which is a flag stating that static IP addresses will be used in the installation.
* **ipAddressIngress**, which establishes the static IP address for the URL indicated in the _ingressHostname_ parameter.

  This static IP address, if it exists, must be provided by the Nalej management department. If it's not given, the Kubernetes cluster will ask for an IP while executing this command, and then tell the management cluster about the obtained IP.

The response to this command looks like this:

```javascript
{
  "install_id": <installation_id>,
  "organization_id": <org_id>,
  "cluster_id": <cluster_id>,
  "state": 1
}
```



## Provisioning and installing a cluster

For v0.6.0 onwards, however, the recommended command is `provision-and-install`, which has a lot more available options depending on the platform the cluster will be installed into. 

For example, for an AWS application cluster, we would execute:

```bash
./public-api-cli cluster provision-and-install 
	--clusterName="clusterName" 
	--clusterType=KUBERNETES 
	--kubernetesVersion="1.16" 
	--targetPlatform=AWS 
	--nodeType="t3a.medium"
	--numNodes 3 
	--zone "eu-west-2" 
	--awsDnsName "[AWS_DNS_NAME]" 
	--awsEksSecurityGroupId "[AWS_EKS_SECURITY_GROUP_ID]" 
	--awsHostedZoneId "[AWS_HOSTED_ZONE_ID]" 
	--awsVpcIdentifier "[AWS_VPC_ID]" 
	--awsControlPlaneRole "path:to:role/EKSClusterRole" 
	--awsNodeRole "path:to:role/EKSNodeGroupRole" 
	--awsRoute53Region "eu-west-2"  
	--awsPublicSubnets "[PUBLIC_SUBNET]" 
	--awsPrivateSubnets "[PRIVATE_SUBNET_1,PRIVATE_SUBNET_2]" 
	--metadataLabels "label1:value1"
```

These parameters are:

- **clusterName**: The name of the cluster.
- **clusterType**: The type of the cluster we want (to choose between `KUBERNETES` and `BAREMETAL`)
- **kubernetesVersion**: The Kubernetes version currently in use in the platform.
- **targetPlatform**: This indicates the platform of the cluster, between `minikube`,  `azure` and `aws` \(default `minikube`\). The parameters change for each platform.
- **nodeType**: the type of machine that will be reserved. For more information regarding this paramenter, please take a look at the [official Amazon EC2 Instance Types documentation](https://aws.amazon.com/ec2/instance-types/).
- **numNodes**: The number of nodes for this cluster. The minimum number of nodes is 3.
- **zone**: The region where the clusters will be located.
- **awsDnsName**: This is the DNS Zone that Nalej will use to register the required DNS records. This DNS Zone must be registered on your AWS account.
- **awsEksSecurityGroup**: The EKS security group ID.
- **awsHostedZoneID**: The hosted zone ID.
- **awsVpcIdentifier**: The VPC where the subnets are declared.
- **awsControlPlaneRole**: The EKS Cluster Role created when the platform was deployed.
- **awsNodeRole**: The EKS Node Group Role created when the platform was deployed.
- **awsRoute53Region**: The Route 53 region should be the same in the management cluster and in the application clusters. If you want them to be different, be aware that you will need to modify the Route 53 configuration in order to make it work.
- **publicSubnets**: The public subnets available.
- **privateSubnets**: The private subnets available. There must be two. 
- **metadataLabels**: The labels for this cluster. 

It is recommended that a platform operator performs this operation, since the information needed will be more readily available for them.

## Is the cluster running?

To check the availability through the CLI we just have to list the clusters in the system with the command:

```bash
./public-api-cli cluster list
```

This will print a response similar to this one:

```bash
NAME               ID                                     NODES   LABELS                    STATE       STATUS
<cluster_name_1>   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx   3       key1:value1,key2:value2   INSTALLED   ONLINE
<cluster_name_2>   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx   1       key3:value3,key4:value4   INSTALLED   ONLINE
<cluster_name_3>   xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx   4       key5:value5,key6:value6   INSTALLED   ONLINE
```

This response is already analyzed in the [Cluster monitoring](cluster_monitoring.md) section of the documentation, and it should show the information of the newly installed cluster.

