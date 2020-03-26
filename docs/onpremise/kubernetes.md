# Kubernetes in the Nalej Platform

## Kubernetes on Bare Metal

Some Kubernetes clusters need to be installed as a prerequisite for the Nalej platform. At least:

-  **2 clusters** must be available (1 for management, 1 for application), 
- with **version 1.11 or higher**, and 
- each cluster needs at least **one master and 3 worker nodes**. 

Please note that connectivity is required between all clusters. 

The official installation guide with `kubeadm` can be found [here](https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/install-kubeadm/). To confirm that your cluster specifications fit Nalej platform requirements, the following commands can be useful:

- To check if there are at least 3 nodes with `STATUS=ready`:

```shell
kubectl get nodes 
```

- To check node capacity and system info:

```shell
kubeckt describe node <node_name>
```

The response to this last command will give us the capacity info:

```shell
cpu: 2
memory: 8GB
```

And the system info:

```SHELL
Kubelet Version: <1.11 or higher>
Kube-Proxy Version: <1.11 or higher>
OS Image: 18.04.3 LTS
```

## MetalLB

Kubernetes does not offer an implementation of network load-balancers ([Services of type LoadBalancer](https://kubernetes.io/docs/tasks/access-application-cluster/create-external-load-balancer/)) for bare metal clusters. The implementations of Network LB that Kubernetes does ship with are all glue code that calls out to various IaaS platforms (GCP, AWS, Azure…). If you’re not running on a supported IaaS platform (GCP, AWS, Azure…), LoadBalancers will remain in the “pending” state indefinitely when created.

Bare metal cluster operators are left with two lesser tools to bring user traffic into their clusters, “NodePort” and “externalIPs” services. Both of these options have significant downsides for production use, which makes bare metal clusters second class citizens in the Kubernetes ecosystem.

MetalLB aims to redress this imbalance by offering a Network LB implementation that integrates with standard network equipment, so that external services on bare metal clusters also “just work” as much as possible.

### Requirements

MetalLB requires the following to work:

- A [Kubernetes](https://kubernetes.io/) cluster, running Kubernetes 1.13.0 or later, that does not already have network load-balancing functionality.
- A [cluster network configuration](https://metallb.universe.tf/installation/network-addons/) that can coexist with MetalLB. (*)
- Some IPv4 addresses for MetalLB to hand out.
- Depending on the operating mode, you may need one or more routers capable of speaking [BGP](https://en.wikipedia.org/wiki/Border_Gateway_Protocol). To know more about this characteristic, please read the [documentation about MetalLB](./metallb.md) that we've confectioned.

(*) Generally speaking, MetalLB doesn’t care which network addon you choose to run in your cluster, as long as it provides the standard behaviors that Kubernetes expects from network addons. 

The following is a list of network addons that have been tested with MetalLB, for your reference. The list is presented in alphabetical order, we express no preference for one addon over another. Addons that are not on this list probably work, we just haven’t tested them.

| Network AddOn | Compatible                                               |
| ------------- | -------------------------------------------------------- |
| Calico        | Mostly (issues with BGP)                                 |
| Canal         | Yes                                                      |
| Cilium        | Yes                                                      |
| Flannel       | Yes                                                      |
| Kube-router   | Mostly (not working with external BGP peering mode)      |
| Romana        | Yes                                                      |
| Weave Net     | Mostly (not working with `externalTrafficPolicy: Local`) |

### Installation	

*Consider that the latest release of MetalLB by the time of writing this document is **v0.8.3**. Modify if required before installing. If you're thinking of upgrading to a higher version, please consult this decision with the DevOps team beforehand.* 

MetalLB must be set up before installing Nalej, and it will be required both in management and application clusters. To install MetalLB, apply the manifest in the management cluster:

```shell
kubectl apply --kubeconfig <KUBECONFIG.yaml> -f https://raw.githubusercontent.com/google/metallb/v0.8.3/manifests/metallb.yaml
```

This will deploy MetalLB to your cluster, under the `metallb-system` namespace. The components in the manifest are:

- The `metallb-system/controller` deployment. This is the cluster-wide controller that handles IP address assignments.
- The `metallb-system/speaker` daemon set. This is the component that speaks the protocol(s) of your choice to make the services reachable.
- Service accounts for the controller and speaker, along with the RBAC permissions that the components need to function.

You can check if MetalLB is running with the following command:

```shell
kubectl get pods -n metallb-system
```

The installation manifest doesn't include a configuration file. MetalLB's components will still start, but will remain idle until you define and deploy a `configmap` into the same namespace. In the section related to MetalLB in our documentation, we provide an [example](https://docs.nalej.com/on-premise-platform-installation/metallb#metallb-config-map).

#### Layer 2 configuration

Layer 2 mode is the simplest to configure: in many cases, you don’t need any protocol-specific configuration, only IP addresses.

Layer 2 mode does not require the IPs to be bound to the network interfaces of your worker nodes. It works by responding to ARP requests on your local network directly, to give the machine’s MAC address to clients.

For example, the following configuration gives MetalLB control over IPs from `192.168.1.240` to `192.168.1.250`, and configures Layer 2 mode:

**`#layer2-config.yaml`**

```yaml
apiVersion: v1
kind: ConfigMap
metadata: 
	namespace: metallb-system 
	name: config
data: 
	config: |  
		address-pools:  
		- name: default   
			protocol: layer2   
			addresses:   
			- 192.168.1.240-192.168.1.250
```

Modify the addresses range to match the Public IP addresses of the nodes in your Kubernetes cluster, and create a `layer2-config.yaml` file with the user’s configuration. Once you are satisfied, apply it:

```shell
kubectl apply -f layer2-config.yaml
```

After this, MetalLB takes ownership of one of the IP addresses in the pool and updates the `loadBalancer` IP field of the service accordingly. You can check and change this configuration later with:

```shell
kubectl describe configmaps -n metallb-system

kubectl edit configmap config -n metallb-system
```
