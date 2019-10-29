# Application Networking

Nalej platform allows the user to create point to point, secure connections between deployed applications.
If you want to connect applications, this is your section.

### Show connections

#### Public API CLI

To list the connections of an organization, invoke the CLI with the command `appnet list`.

```bash
./public-api-cli appnet list
```

It will show something like this:

```bash
SOURCE_INSTANCE_ID                     SOURCE_INSTANCE_NAME   OUTBOUND   TARGET_INSTANCE_ID                     TARGET_INSTANCE_NAME   INBOUND   STATUS
058d0a7c-4b92-4c9d-9dbe-83c5c60c7bb1   NP-2216_SOURCE04       out        eb945169-448e-4c4b-8f74-2f43c5fdca87   NP-2216_SINK           in        ESTABLISHED
7cf8da85-4bc0-499e-bfb5-2c9f9b332f5a   NP-2216_SOURCE02       out        eb945169-448e-4c4b-8f74-2f43c5fdca87   NP-2216_SINK           in        ESTABLISHED
b3ded11e-ab1d-48d9-b74e-9592fa4adcca   NP-2216_SOURCE01       out        eb945169-448e-4c4b-8f74-2f43c5fdca87   NP-2216_SINK           in        ESTABLISHED
b778f3f1-542d-4f94-91d6-a8724b022e63   NP-2216_SOURCE03       out        eb945169-448e-4c4b-8f74-2f43c5fdca87   NP-2216_SINK           in        ESTABLISHED
f9849ded-23c6-44be-ab32-75b65b47d86f   NP-2216_SOURCE11       out        eb945169-448e-4c4b-8f74-2f43c5fdca87   NP-2216_SINK           in        WAITING
```

The possible statuses are:
* WAITING: The connection is waiting for all the components to connect to the private network.
* ESTABLISHED: All the components are connected and the network is ready to transmit.
* TERMINATED: When an application is being undeployed for any reason, this status will raise before delete the connection.
* ERROR: If something failed when establishing the connection and the failure cannot be reversed or retry to connect.

#### Web interface

When you open the Applications view, the deployment graph will show the active connections as arrowed lines between applications.

![Main view of applications showing connections](../.gitbook/assets/tutorial_appnet_main_page.png)

If you click on the **Manage connections** button, it will show the **Manage connections** modal window.

![Manage connections modal window](../.gitbook/assets/tutorial_appnet_manage_connections_list.png)

The list will show all the connections. If the source interface name shows an asterisk `*`, that mean that the outbound
interface is marked as **required**.

### Create a new connection between applications

There are some rules that must be observed when creating a connection:
* A connection can only be created between an outbound net interface and an inbound net interface.
* An application instance can not be connected to itself.
* One outbound net interface can only be connected to one, and only one, inbound net interface.
* One inbound net interface can be attached to multiple outbound net interfaces.
* The target port listed in the rule that describes the interface, will be the port opened for the connection.

#### Public API CLI

To create a new connection, you must invoke the CLI with the command `appnet add`. You will need to specify
the following parameters:
* **source_instance_id**: The id of the source application instance, the one that describes the outbound interface.
* **outbound_iface_name**: The name of the outbound network interface that belongs to the source instance.
* **target_instance_id**: The id of the target application instance, the one that describes the inbound interface.
* **inbound_iface_name**: The name of the inbound network interface that belongs to the target instance.

```bash
./public-api-cli appnet add
    <source_instance_id>
    <outbound_iface_name>
    <target_instance_id>
    <inbound_iface_name>
```

Be aware that the request is asynchronous. The platform will answer with a `RESULT OK` message if the request was accepted
and it will do its best to create the connection as soon as possible. Run the command `appnet list` to follow the connection status. 

#### Web interface

![Manage connections window to add connection](../.gitbook/assets/tutorial_appnet_manage_connections_list_add.png)

On the **Manage connections** window, click on the **Add new connection** button to open the **Add new connection** dialog.

![Add new connection dialog](../.gitbook/assets/tutorial_appnet_add_connection.png)

Here you can define the source instance, the outbound interface name, the target instance, and the inbound interface name.
Then just clic on the button **Add new connection** to send an asyncronous message to the platform to create the connection.

When the connection is established, the main graph will show the connection with an arrowed edge between the instances.

### Remove a connection

#### Public API CLI

To remove a connection, you must invoke the CLI with the command `appnet remove`. You will need to specify the following parameters:
* **source_instance_id**: The id of the source application instance, the one that describes the outbound interface.
* **outbound_iface_name**: The name of the outbound network interface that belongs to the source instance.
* **target_instance_id**: The id of the target application instance, the one that describes the inbound interface.
* **inbound_iface_name**: The name of the inbound network interface that belongs to the target instance.

```bash
./public-api-cli appnet remove
    <source_instance_id>
    <outbound_iface_name>
    <target_instance_id>
    <inbound_iface_name>
```

Be aware that the request is asynchronous. The platform will answer with a `RESULT OK` message if the request was accepted
and it will do its best to remove the connection as soon as possible. Run the command `appnet list` to follow the connection status.

#### Web interface

![Manage connections window to remove connection](../.gitbook/assets/tutorial_appnet_manage_connections_list_remove.png)

On the **Manage connections** window, click on the **Disconnect** button to remove that connection. The platform will show
a confirmation popup to avoid accidental remotions.


