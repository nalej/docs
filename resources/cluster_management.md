# Cluster management

As far as we know, we can monitor clusters that belong to our organization, we can install them... but how do we manage them? Is there a way to decide which applications go to which clusters?

Well, of course there is, you know your wish is our feature. Just ask nicely.

## Cluster management commands

There are three CLI commands that will help you with the management, and you can get the most of them by combining them. They are:

### `cordon`

This command will isolate a specific cluster, and no new applications will be able to deploy in it while in this state. It's used like this:

```bash
./public-api-cli cluster cordon 
	[clusterID]
```

So, the only thing we need is the **cluster ID** of the cluster we want to isolate. The platform will return a `RESULT OK` if the instruction executed successfully, or if the cluster was already cordoned.

### `uncordon`

This command is to be used in a cordoned cluster, and as you may have guessed, it allows the applications to deploy in the cluster again.

```bash
./public-api-cli cluster uncordon 
	[clusterID]
```

As before, the **clusterID** is the only information we need to uncordon a cluster, and the platform will return a `RESULT OK` if the instruction executed successfully, or if the cluster wasn't cordoned in the first place.

### `drain`

This command moves the deployed services in the cluster to other clusters (if it's possible), leaving it empty.

```bash
./public-api-cli cluster drain 
	[clusterID]
```

Again, we need the **clusterID** to execute the command, and once we do, it will move the services to other clusters if possible. The users will be completely unaware of this process, since they won't stop executing.

For this to work it's **mandatory** that the **cluster is in the `cordon` state**. If it is not, the command will return with an error reminding you that you have to cordon the cluster first. This restriction helps us avoid situations like the draining of a cluster where there's a deployment in process, for example. So yeah, first `cordon` the cluster, and then `drain` it.

So, why wouldn't the services be able to deploy in other clusters? Well, apart from technical reasons like a connection failure, there are several reasons why this could happen.

- There are no more clusters available.
- The application has a **cluster selector** in its descriptor, and no other cluster matches with it.

What is a **cluster selector**, you ask? It is a parameter that can be included in the application descriptor, which contains a label that the cluster must have in order to be able to deploy a specific service. It looks like this:

```json
...
cluster_selector = “key1:value1”
...
```

So, if we try to deploy this application (with these services) and there are no clusters with that label, the deployment will end up in an error. The same will happen if, when we try to drain a cluster, there are no other clusters with that label.

## Examples of use cases

Let's imagine situations where these commands can be useful.

### Something goes wrong in the cluster

Everything is going smoothly, but suddenly something looks weird in a specific cluster. Maybe you monitor the cluster and there's an unexpected peak in the CPU usage, or the services in it are behaving in a strange way. What to do then?

First you should `cordon` the cluster, so it is isolated and no more services will be deployed there for now. After this, we could check the cluster as is, to see if we can detect what is happening.

If what we detect is not a service malfunction, but a malicious attack, the next step would be to `drain` the cluster, so the services are safe in another place, and then take the appropriate steps to protect that cluster.

Once the cluster is safe (and/or the problems are fixed), we could `uncordon` the cluster so it is available for other services to be deployed there.

### Reserving a cluster for some specific services

The first thing we must do is to assure that the cluster is labeled with the **cluster selector** that we're going to register in the application descriptor.

Once that is done, the next step is to `cordon` the cluster and `drain` it of the services that are already running there. We want it to be exclusive for our new services that we're about to deploy.

Then we `uncordon` the cluster and deploy the services as usual.

And the last thing we should do is `cordon` the cluster again, so our services keep on running there but no more new ones can be deployed.