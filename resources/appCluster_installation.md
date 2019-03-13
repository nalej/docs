# Application cluster installation

## Previous structure in the system

This installation requires that there is already:

- a Kubernetes cluster available, where the structure for a Nalej application cluster will be installed.
- working connectivity between the Nalej management cluster and this brand new Kubernetes cluster.

The management cluster must know that an application cluster will be installed, and the user must log in the system with a role that allows them to execute the required actions.

## Installation of an application cluster

For this process, we also need some information from the Nalej management department, which is a configuration file for the Kubernetes cluster. This configuration file is commonly called **kubeconfig**, it's a YAML file, and it contains all the information the cluster needs to be configured as an application cluster.

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

- **targetPlatform** indicates the platform of the cluster. By now, the most common value for this parameter is `AZURE`.
- **ingressHostname** states the new URL for the application cluster. This URL must be unique in the system.
- **kubeConfigPath** indicates the path to the configuration file mentioned above.

These are the mandatory parameters. There are two more optional ones:

- **useStaticIPAddresses**, which is a flag stating that static IP addresses will be used in the installation.
- **ipAddressIngress**, which establishes the static IP address for the URL indicated in the *ingressHostname* parameter.

 This static IP address, if it exists, must be provided by the Nalej management department. If it's not given, the Kubernetes cluster will ask for an IP while executing this command, and then tell the management cluster about the obtained IP.

The response to this command looks like this:

```json
{
  "install_id": <installation_id>,
  "organization_id": <org_id>,
  "cluster_id": <cluster_id>,
  "state": 1
}
```

## Is the cluster running?

We can check if the installation was successful and the cluster is up and running through the Web Interface and through the CLI.

### Web Interface

We just have to navigate to the Resources view.

![Resources list view.](../.gitbook/assets/res_list.png)

Here, we can see the list of available application clusters in the system, and our brand new cluster should appear on the list.

### Public API CLI

To check the availability through the CLI we just have to list the clusters in the system with the command:

```bash
./public-api-cli cluster list
```

This will print a response similar to this one:

```json
{
  "clusters": [
    {
      "organization_id": <org_id>,
      "cluster_id": <cluster_id>,
      "name": <cluster_name>,
      "cluster_type_name": <cluster_type_name>,
      "multitenant_support": "YES",
      "status_name": "RUNNING",
      "total_nodes": x,
      "running_nodes": x
    },
   ...
  ]
}
```

which is already analyzed in [this page of the documentation](resources.md), and in this JSON document the information of the new cluster should appear.