# The Inventory: what it is, and how it can help you

The Infrastructure section gathers all the information of what your company has in Nalej, and lets you see the information related to it.

## What is the Inventory?

The Inventory is the main view of the Infrastructure section. It consists of a list of the resources your organization has in the system. This list has:

- The **devices**, as in components of the IoT.
- The **assets** you have, as in the hardware registered in the platform.
- The **Edge Controllers** installed in your organization. We'll talk more about this component later in this document.

The main objective of this section is the monitorization of the hardware that's already registered in the platform, so we can have, in one place, the status and availability of every piece of hardware connected to it.

## What is an Edge Controller, and why do I need one?

> - what it is, with purpose and all
> - how to join one

An Edge Controller (EC) is a light Virtual Machine installed in your organization. Its mission is to serve as an entry point for the Nalej Management Cluster, so it can receive data from the hardware installed there.

To do that (to receive info from the hardware on the client's side), we need a service in that hardware that sends it. That service is called an **Agent**.

### What is an Agent, then?

As we stated before, an **Agent** is a service installed in a piece of hardware in the client's side. This agent is registered in an EC, and when it's live it sends a message saying so. The EC, then, replies with a set of operations this agent has to execute. When the agent finishes those operations, it sends the results to the EC, which then forwards them to the Nalej Management Cluster.

> diagram?

> how to install an agent:
>
> i ask the EC for a token, and I use that token to install the agent.

