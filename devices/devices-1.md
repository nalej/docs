# Devices in Nalej

This section will talk about devices in Nalej.

> TODO write intro. What is a device? What does it do? Why do we need it?

## Getting device information

### Web Interface

As with the rest of the sections, we can find the Device view in the left-hand column.

![Devices view](../.gitbook/assets/dev_ppal.png)

The upper part of the screen displays the following:

- a **summary**, where we can see the total number of devices in the system, and the number of groups that contain them.
- a **status timeline**, where we can see the percentage of online devices in a given time.

The lower part of the screen is a list of devices divided by groups. The default group is `ALL`, and it shows all the devices in the system. But the rest of the groups appear there, easily clickable, and so when we click on one of them...

![dev_devgroup_view](../.gitbook/assets/dev_devgroup_view.png)

The view slightly changes. Now, the summary displays the information of only this group, like:

- its **availability**, with values like `ENABLED`or `DISABLED`.
- its **API_Key**.
- the **number of devices** in it.
- the **device connectivity**.

The status timeline is still there, but now it only refers to the devices in this group.

The list of devices also displays the devices in this group, with the following information for each one:

- its **ID**.
- the **date** it was added to the system.
- its current **status**.
- any associated **labels** it may have.
- an **`ENABLED`** flag, which allows us to quickly disable a given device.

We can also search by any `string` included in any part of the device information (for example, we can search `online` to see which devices are online at any given moment, or a specific date of inclusion in the system).







![dev_devgroup_config](../.gitbook/assets/dev_devgroup_config.png)



### Public API CLI

> TODO: find the correct instructions to manage devices and see their info.



## Adding a device group

### Web Interface

We can add a new device group easily, clicking on the option **"Add group"** in the main view (or in a group view).

![The "Add Group" option in the main Devices view](../.gitbook/assets/dev_add_devgroup_prev.png)



This opens a dialog like the one below:

![dev_add_devgroup](../.gitbook/assets/dev_add_devgroup.png)

To create a device group, we need:

- A **group name**.
- The **group device availability**.
- If the **devices** are **enabled by default**.

### Public API CLI

> TODO: find command



## Configuration of a device group

### Web Interface

In the device group view, we can easily access its configuration by clicking on the link highlighted below.

![dev_devgroup_config](../.gitbook/assets/dev_devgroup_config_prev.png)



The only options that can be changed in a group are:

- The **group device availability**.
- If the **devices** are **enabled by default**.

![dev_devgroup_config](../.gitbook/assets/dev_devgroup_config.png)

### Public API CLI

> TODO find appropriate commands



## Deleting a device group

### Web Interface

Now, we want to delete an entire device group. From that group view, we can click on "Delete group"...

![dev_delete_devgroup_confirm](../.gitbook/assets/dev_delete_devgroup_prev.png)

And the system will confirm the deletion with a notification in the upper right part of the screen.

![dev_delete_devgroup_confirm](../.gitbook/assets/dev_delete_devgroup_confirm.png)



### Public API CLI

> TODO find appropriate commands

