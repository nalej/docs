# Edge Controllers and Agents

The Edge Controllers and the Agents are both Nalej components that are installed in your side of the organization so the Nalej platform can have access to the assets there. Let's start with some basic definitions.

## What is an Edge Controller, and why do I need one?

An Edge Controller \(EC\) is a component installed in your organization. Its mission is to serve as an entry point for the Nalej Management Cluster, so it can receive data from the hardware installed there.

To do that \(to receive info from the hardware on the client's side\), we need a service in that hardware that sends it. That service is called an **Agent**.

![How the connection between the Nalej Management Cluster and the ECs work](https://github.com/nalej/docs/tree/fe15f85055d0b510a5d7775e7d88d07c007a7239/.gitbook/assets/infrastructure_inventory_EC_Agents.png)

As you can see in the diagram, the connection between the Nalej Management Cluster and the Edge Controllers in the customer's side is done through a VPN, thus securing the communications between them. This is the reason why the EC must have more logic than an Agent, and so it must be a \(light\) Virtual Machine.

## What is an Agent, then?

As stated before, an **Agent** is a service installed in a piece of hardware in the client's side. This agent is registered in an EC, and when it's live it sends a message saying so. The EC, then, replies with a set of operations this agent has to execute. When the agent finishes those operations, it sends the results to the EC, which then forwards them to the Nalej Management Cluster.

![Communication diagram Agent-EC-NMC](https://github.com/nalej/docs/tree/fe15f85055d0b510a5d7775e7d88d07c007a7239/.gitbook/assets/infrastructure_inventory_Agent_communication.png)

### What is the actual role of an Agent in the system?

An Agent will let the platform know about the client's hardware. This is useful for Nalej, because with this information it can obtain a hardware map from the client's side, and thus the managers can decide whether or not they want to use the assets they have available at any given time.

One of the services the Agent will have to execute is the monitorization of the hardware it's installed into, no matter if it's part of an application cluster or not. Thus, the Inventory view will be a collection of devices and assets in the client's company \(with their associated status and connectivity\), as well as the Edge Controllers that let us connect to said assets.

## Managing ECs

### Through CLI

The CLI command to manage the Edge Controllers is `ec` \(or `edgecontroller`\). Let's see what we can do with it.

#### `create-join-token`

First, we can create a join token, so when we install an EC we can join it to the Nalej Management Cluster. This is done with:

```bash
./public-api-cli ec create-join-token
  --outputPath /Users/user/folder/
```

With this, a token file is created and stored in the path that has been defined by the user. If that flag is not used, the token file will be stored in the current path.

#### `install-agent`

We can also install an agent in this EC. For this, we need:

```bash
./public-api-cli ec install-agent 
    [edgeControllerID] 
    [targetHost] 
    [username] 
    --agentType "type of hardware"
    --password <password>
    --publicKeyPath <publicKeyPath>
    --sudoer=true
```

* the ID of the EC we want to join.
* the IP address of the asset where we want to install the agent.
* the type of agent we want to install, to choose between the following: LINUX\_AMD64, LINUX\_ARM32, LINUX\_ARM64 or WINDOWS\_AMD64.

The agent will be installed through SSH, and for this we will need:

* the username, and one of these options:
  * a password
  * the path to the RSA key \(in the `—publicKeyPath` flag\)
* We also have a flag that indicates if the user has root permissions \(is a `sudoer`\) or not \(the default value is `false`\).

#### `update-location`

You can also update the location of a given EC:

```bash
./public-api-cli ec update-location 
    [edgecontrollerID] 
    --geolocation "new geolocation"
```

The only thing we need here, apart from the ID of the EC we want to update, is its new location.

#### `unlink`

Lastly, you can unlink a specific EC from the NMC.

```bash
./public-api-cli ec unlink
    [edgecontrollerID]
    --force=true
```

The only thing needed for this will be the ID of the EC we want to unlink. We can also indicate that we really, really want the EC to unlink with the `—force` flag \(which is set to `false` by default\).

### Through Web Interface

When in the Infrastructure view, we can use the **Quick Filters** available and click on the ECS filter. This will show a list of all the ECs in the organization.

![Main list of ECs](../.gitbook/assets/infrastructure_ec_ppal.png)

Once here, we can easily find the EC we want to manage, and:

* Check its basic information \(ID, geolocation, status\).
* Add or delete labels \(the same way as in the rest of the views\).

We can also access the **Actions** menu \(the three dots icon in the far right column\) and find several more options, like:

**More info**

![All the info about the EC](../.gitbook/assets/infrastructure_ec_moreinfo.png)

Here we can see, apart from the information we already had, the list of assets attached to a specific EC.

**Install agent**

![Info needed to install an agent](../.gitbook/assets/infrastructure_ec_installagent.png)

This allows us to install an agent directly from the EC. For this, we need:

* the agent **type**, which we can choose from the drop-down list.
* the **SSH username and password** that will grant us permission to install said agent.
* the **target host** where the agent will be installed.

**Create agent token**

![Agent join token](../.gitbook/assets/infrastructure_agent_createjointoken.png)

This view shows the certificate \(and when it expires\) and the token needed for an agent to join this EC.

**Unlink EC**

This option triggers a confirmation dialog, and when we confirm, it unlinks this EC from the Nalej Management Cluster.

## Managing Agents

The agents are managed a bit different than the ECs, since what we see is the asset where they are installed and not the agent itself. Nonetheless, let's see what we can do with them.

### Through CLI

We can manage the agents through the CLI with the command `ag` or \(you guessed it\) `agent`. And what can we do with it?

#### `create-join-token`

We can create a token for this agent to join a specific EC.

```bash
./public-api-cli agent create-join-token
    [edgecontrollerID]
    --outputPath /Users/user/folder/
```

With this, a token file is created and stored in the path that has been defined by the user. If that flag is not used, the token file will be stored in the current path.

#### `monitoring`

We can activate the monitor feature for the asset the agent is installed in.

```bash
./public-api-cli agent monitoring 
    [edgecontrollerID]
    [assetID]
    --activate=false
```

For this we will need:

* the ID of the EC associated to the agent.
* the ID of the asset we want to monitor.
* a flag indicating whether we want to activate or deactivate the asset monitoring \(the default value is `true`\) \(don't forget the `=` sign when dealing with boolean flags!\).

#### `uninstall`

We can, also, uninstall an agent from the asset it is in.

```bash
./public-api-cli agent uninstall 
    [assetID]
    --force=true
```

For this, we will only need the ID of the asset where the agent is installed. As you can see, we can force the uninstallation in case something goes wrong and we really really want to uninstall that agent \(the default value for this flag is `false`\).

### Through Web Interface

In the Infrastructure view, we will click on the **Quick Filter** made for the Assets, and so we will be able to see the list with all the assets installed in our organization. If we know the asset ID or other type of information \(for example, a specific label\), we can also filter by that in the **Search** box.

Once we find the asset where our agent is installed, we can:

* get the asset ID, its geolocation and its status \(in a first glance\).
* add and delete tags \(using the same procedure as in other parts of the web interface\).

Also, in the far right column we can click on the three dots icon to access the **Actions** menu, which allows us access to the following:

**More info**

![Agent info view](../.gitbook/assets/infrastructure_agent_moreinfo.png)

Here we can find an extensive list of data that may be relevant to define this specific asset, for example:

* the **Edge Controller** it is linked to.
* its **creation date**.
* its **OS**.
* the details of its **CPU**.
* its **RAM** capacity.
* its **Storage** type and capacity.
* its **networking specifications**.

**Last operation log**

![Last operation info](../.gitbook/assets/infrastructure_agent_lastopinfo.png)

Here we can see the information obtained from the last operation the asset executed, with when it was, what was the status, and the extra info that went attached to it.

**Uninstall agent**

As with the ECs, this option prompts a browser dialog for us to confirm the action, and when we do, the agent gets uninstalled and the asset disappears from the list.

