# Clusters and nodes

All the information related to cluster managing will be available in this section.

- Navigate through clusters
- Explain what a label is at cluster/node level.
- List nodes
- Install application cluster commands. The full cluster install guide should be another document in itself.

Notice:

- Adding/removing labels to nodes may produce collateral damage. Labels have also a meaning in kubernetes

----

The application you're deploying will be deployed in a **cluster**. A cluster is a logical group of **nodes**, which are physical devices. When an application is deployed, the cluster will decide if there is a need to deploy it in one or several nodes, and will manage it accordingly.

## Cluster monitoring

In the web management interface, click on Resources on the left column, so the Resources view is displayed.

> TODO: image

In the upper part of the screen we can see:

- **Summary card**: the number of clusters and nodes in the system.
- **Clusters card**: a carousel of charts with information about each cluster and the nodes in it (like how many nodes are running in the cluster).
- **Node status timeline**: a timeline of the status of all the nodes.

> TODO: image

The lower section displays a **cluster list**. Each row of the list refers to a different cluster, with some information about it:

- its **name**.
- its **identifier**.
- the number of **nodes** it has inside.
- a list of **labels**.
- the **type** of cluster (the system only accepts *kubernetes* by now).
- the **status** of the cluster (it can be *running*, *processing* or *error*).
- [NOT ACTIVE] **multitenant**, a flag to say if the cluster belongs to more than one organization.

In the same list, on the far right, each cluster has an Edit button. When clicked, a dialog appears where we can change the name and the labels associated to the cluster.

When we click on the name of the cluster, the view changes, and the information displayed refers to that specific cluster and its nodes.

> TODO: image

In the upper part of the screen we can see the **status** of the cluster (which is "RUNNING" only if all the nodes in it are running, and if not it shows the most serious problem in the clusters), and a **summary** of the cluster information we saw in the previous list.

In the lower part of the screen we can see another list, this time of nodes. The information displayed is as follows:

- The **node ID**.
- The **IP** associated to it.
- The current **state** of the node.
- The **labels** it has.
- Its current **status** (again, it can be *running*, *processing* or *error*).