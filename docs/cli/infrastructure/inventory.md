# The inventory: what it is and how it can help you

The Infrastructure section gathers all the information of what your company has in Nalej, and lets you see the information related to it.

## What is the Inventory?

To access the Inventory list through the CLI, you just need to execute:

```bash
./public-api-cli inventory list
```

This will produce a table with the following data:

```bash
TYPE     ID         LOCATION         LABELS           STATUS
DEVICE   <dev_id>   Madrid, Spain    sprint14:demo    OFFLINE
...
EC       <ec_id>    Demoland                          OFFLINE
...
ASSET    <a_id>     Getxo, ES        l1:v1,l2:v2...   OFFLINE
...
```

This table is essentially the same table we can see through the Web Interface, with the **devices**, the **Edge Controllers** and the **assets** in the current organization.

The assets can be managed from here, with the `inventory asset` command. 

The system will return the information of the asset with:

```bash
./public-api-cli inventory asset info [assetID]
```

We can add or delete labels with:

```bash
./public-api-cli inventory asset label add [assetID] "label1:value1;label2:value2"

./public-api-cli inventory asset label delete [assetID] "label2:value2"
```

Please note that the different labels are expressed like pairs `key:value`, and the separator between two labels is `;`.

Lastly, we can update the location of an asset with:

```bash
./public-api-cli inventory asset update-location [assetID] "Office 23"
```

That is the asset management provided by the platform. To manage devices and Edge Controllers we encourage you to read the documentation written with that purpose in mind, which is ["Adding, managing and deleting devices"](../devices/dev_deploy_mgmt_removal.md) for the former and ["Edge Controllers and Agents"](ecandagents.md) for the latter. However, you will find a brief introduction to the topic of the Edge Controllers and Agents later in this document.

To finish this section, you can also visualize a summary of the organization in terms of storage and computing capacity with:

```bash
./public-api-cli inventory summary
```

This returns a table like this one:

```bash
CPUs   STORAGE (GB)   RAM (GB)
25     1346           66
```

which tells you the resources available in the organization \(number of CPUs, storage in GB, and RAM availability in GB\).

## What is an Edge Controller, and why do I need one?

An Edge Controller \(EC\) is a component installed in your organization. Its mission is to serve as an entry point for the Nalej Management Cluster, so it can receive data from the hardware installed there. More information about Edge Controllers can be found in [the Edge Controller and Agents documentation](ecandagents.md), where there's a more thorough explanation.

### How can I install an Edge Controller in my organization?

First, you need to ask for an Edge Controller to the Nalej Management. This EC is a light Virtual Machine \(VM\), and can be installed in two ways:

- It can be installed **in the client cloud**. Right now the only supported cloud provider is **Azure**, although Nalej is working to adapt its technology to other providers. 
- Since it's a VM, it can also be installed **in a physical server** in the client side.

To deploy the EC in the cloud, you need to generate a `cloud-init.yaml` file. This file would look like this:

```yaml
write_files:
  - content: |
      # edge-controller configuration file

      joinTokenPath: /etc/edge-controller/joinToken.json
      useBBoltProviders: true
      bboltpath: /var/lib/edge-controller/database.db
      name: EdgeController001
      #labels: "name:test"
      #geolocation: "Madrid, Madrid, Spain"
    path: /etc/edge-controller/config.yaml
  - encoding: b64
    content: <joinToken.json BASE64 ENCODED CONTENTS>
    path: /etc/edge-controller/joinToken.json

runcmd:
  - [ systemctl, restart, edge-controller.service ]
```

What do you need to know about this file? Well...

* All the parameters with `path` in their name \(`joinTokenPath`, `bboltpath`, and the two `path` parameters\) must remain as they appear in this example.
* To customize your EC, the parameters you can change are:
  * `name`, the name you give it.
  * `labels`, in case you want it to have some specific labels.
  * `geolocation`, its location, in case you have several in different places and want to have that extra information registered here.

The `content` parameter deserves a longer explanation. When you want your EC to join the Nalej Management Controller \(NMC\), you should request a token. After receiving it, you should convert it to base64 and include in this parameter.

To convert this file to base64 you can use this command:

```bash
cat joinToken.json | base64 | tr -d ‘\n’
```

The result of this command would be what needs to be included in the `cloud-init.yaml` file, in the `content` parameter.

When deploying the VM in the cloud, at some point this `cloud-init.yaml` file will be requested, so you only have to upload it. The EC will be configured according to this file, and it will join the NMC with the token included in it.

This configuration file is structured in a way that, whenever you want to install another EC in your organization, the only thing you need is a new `cloud-init.yaml`, with different name, labels and geolocation, and a new `joinToken.json`, since the VM is the same for both of them.

In the setting up process, before starting, the EC will execute the `join` operation that registers it in the system with the token we obtained and included in the configuration file, and so the Management Cluster will register the EC and start working with it.

### Additional requirements

When deploying this kind of VM in the cloud we have to make sure that the cloud will allow the communication with it. This means that the ports used by the VM must be also enabled in the cloud, with the security rules needed at a **security group level** so that the communication with the NMC and the Agents is possible.

The VM will be using the default ports, which are **5577** and **5588**, so the cloud must allow the communication with them. If you want to change them for whatever reason, you need to edit the `cloud-init.yaml` file, adding the following parameters under the `geolocation` data:

```yaml
port: XXXX
agentport: XXXX
```

## What is an Agent, then?

As we stated before, an **Agent** is a service installed in a piece of hardware in the client's side, and it lets the platform know about the client's hardware. To know more about agents, please take a look at [the Edge Controller and Agents documentation](ecandagents.md), where there's a more thorough explanation.

### I have a server in my organization, how can I install an Agent in it?

You can use a token procedure, similar to what we used before to register the EC in the Nalej Management Cluster. In this case, the Agent will ask the EC for a token and, upon receiving it, will use said token to join the EC.

!!! note 
    In the future, there will be a **discovery** feature where the Agents will be installed automatically, so this process is invisible to the user. There will also be a feature where the asset can register manually to the EC, withouth having an Agent actively monitoring the asset. This will be useful for network hardware, for example, and will align with Nalej's intention of having this view as a complete inventory of the organization's assets.



