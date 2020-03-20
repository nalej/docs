

# Adding, managing and deleting devices

What is a device for Nalej? The system understands the concept of **device** as an abstract entity that the user can manage as part of the applications installed in the cluster.

_The CLI responses are shown in this document with the text format, which can be obtain adding_ `--output="text"` _to the user options. If you need the responses in JSON format, you can get them by adding_ `--output="json"` _at the end of your requests, or as a user option._

## Getting device-related information

### Web Interface

As with the rest of the sections, we can find the Device view in the left-hand column.

![Devices view](../img/devices.png)

The upper part of the screen displays the following:

* a **summary**, where we can see the total number of devices in the system, and the number of groups that contain them.
* a **status timeline**, where we can see the percentage of online devices in a given time.

The lower part of the screen is a list of devices divided by groups, with the following information for each device:

* its **name**.
* the **attached date** it was added to the system.
* its current **status**.
* any associated **labels** it may have.

Each group, in the grey background row, has its own **Options** button. Clicking on it we can see more information related to the group, we can access its configuration settings (which will be explained in the [Configuration of a device group](#configuration-of-a-device-group) section of this document), or we can delete it.

![Devices group options](../img/devicesoptions.png)

When we choose the **More info** option, a dialog appears, where we can find the device group API key, its default connectivity and if it's enabled or not.

![Devices group info](../img/devinfo.png)

We can also search by any text string included in any part of the device information \(for example, we can search the term "`online`" to see which devices are online at any given moment, or a specific date of inclusion in the system\).

![Using the Search option with the string "471"](../img/searchdev.png)

### Public API CLI

The commands we can use to manage device groups and devices are `devicegroup` and `device`, respectively.

So, to obtain a list of the device groups in the system, the command needed is:

```bash
./public-api-cli devicegroup list
```

It returns a list with the following structure:

```javascript
ID      NAME              API_KEY        ENABLED   DEV_ENABLED
<id1>  <devgroup_name1>   <id_api_key>   true      true
<id2>  <devgroup_name2>   <id_api_key>   false     false
<id3>  <devgroup_name3>   <id_api_key>   true      true
```

Where we can see:

* the **device\_group\_id**.
* the human readable **name** we give the device group.
* the **device\_group\_api\_key**.
* whether it is **enabled** or not.
* a **default\_device\_connectivity** flag, which indicates whether the devices are connected by default or not.

Once we have obtained the list of device groups with their IDs, we can list the devices contained in each of them. To do so, we would use the command:

```bash
./public-api-cli devices list --deviceGroupId=<devgroup_id>
```

The response to this command is a list similar to this one:

```javascript
ID            DATE              STATUS    LABELS   ENABLED
<dev_id1>     <reg_date>        OFFLINE            false
<dev_id2>     <reg_date>        OFFLINE            true
<dev_id3>     <reg_date>        OFFLINE            true
<dev_id4>     <reg_date>        OFFLINE            true
...
```

Where we can see the timestamp where the device was registered \(in **DATE**\), the **STATUS**, which can be `ONLINE` or `OFFLINE`, and whether or not it is **ENABLED**.

We can update the information of a device with:

```bash
 ./public-api-cli device update
     --deviceGroupId=<devgroup_id>
     --deviceId=<dev_id>
     --disabled
     --enabled
```

The only thing we can change for a given device is whether the device is **enabled** or **disabled**.

The result to this command is the device information in a list, like so:

```javascript
ID            DATE              STATUS    LABELS   ENABLED
<dev_id2>     <reg_date>        OFFLINE            false
```

## Adding a device group

### Web Interface

We can add a new device group easily, clicking on the option **"Add group"** in the main view \(or in a group view\).

![The &quot;Add Group&quot; option in the main Devices view](../img/devices%20%281%29.png)

This opens a dialog like the one below:

![Add group dialog](../img/addgroup.png)

To create a device group, we need:

* A **group name**.
* The **group device availability**.
* If the **devices** are **enabled by default**.

Once the group is created, it will be displayed on the devices list.

![](../img/devcreated.png)

### Public API CLI

To add a device group through the CLI, the command needed is:

```bash
./public-api-cli devicegroup add
    --name <devgroup_name>
    --disabled
    --enabled
    --disabledDefaultConnectivity
    --enabledDefaultConnectivity
```

We don't need all these parameters, but we need:

* the **name** of the group.
* a flag indicating if the group is **enabled** or **disabled**.
* a flag indicating the default connectivity for the devices joining the group, whether it is enabled \(**enabledDefaultConnectivity**\) or disabled \(**disabledDefaultConnectivity**\).

The response to this command is something like this:

```javascript
ID      NAME              API_KEY        ENABLED   DEV_ENABLED
<id>    <devgroup_name>   <id_api_key>   true      true
```

This includes all the information related to the device group, which is, its **id**, its **name**, its **API key**, whether it is **enabled**, and whether the devices will be **enabled** by default when joining the group.

## Configuration of a device group

### Web Interface

In the main view, we can easily access the configuration of a specific device group by clicking on the **Configuration** button in the Options menu.

![Device group configuration option](../img/devicesoptions%20%282%29.png)

The only options that can be changed in a group are:

* The **group device availability**.
* If the **devices** are **enabled by default**.

![Device group configuration dialog](../img/devconfig.png)

### Public API CLI

To update the configuration of a device group, the command to use is:

```bash
./public-api-cli devicegroup update
    --deviceGroupId <devgroup_id>
    --disable
    --enable
    --disableDefaultConnectivity
    --enableDefaultConnectivity
```

This information is very similar to what we need to create the group.

* **deviceGroupId** \(when we create a group we need a **name** instead\).
* a flag indicating if we want to **enable** or **disable** the group.
* a flag indicating how to change the default connectivity for the devices joining the group, whether we want to enable it \(**enableDefaultConnectivity**\) or disable it \(**disableDefaultConnectivity**\).

The result of executing this command is the same as with the `devicegroup add` command but with the updated information:

```javascript
ID      NAME              API_KEY        ENABLED   DEV_ENABLED
<id>    <devgroup_name>   <id_api_key>   true      true
```

## Deleting a device group

### Web Interface

Let's say we want to delete an entire device group. From that group view, we can click on the Options menu, and then choose the **Delete group** option.

![Delete devices group](../img/devdeletegrou.png)

And the system will confirm the deletion with a notification in the upper right part of the screen.

### Public API CLI

To remove a device group from the system, we need:

```bash
 ./public-api-cli devicegroup delete 
     --deviceGroupId=<devgroup_id>
```

And, if this command exits successfully, it will return a message like this one:

```bash
RESULT
OK
```

