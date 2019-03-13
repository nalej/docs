# Initial login

Before getting started with the different parts of the platform, we're going to tackle the very first step of the way: the first time we log in the platform. There are two ways we can log in: through the command line interface (CLI) and through the web management interface.

## CLI Login

#### Setting your user options

The very first time you log in the system there are some variables that need to be established. They are needed for each interaction, so setting them up before starting lets us omit them in each request. These variables are the **certificate** you received, and the addresses of the **Nalej login server** and the **Nalej API server**. Gather all data (from the information the Nalej administration provided when signing up for the service), go to the `public-api-cli/bin` folder in your computer and execute the following instructions:

```bash
./public-api-cli options set 
	--key=cacert 
	--value=/Users/youruser/.../certificate.crt

./public-api-cli options set 
	--key=loginAddress 
	--value=login.server.nalej.com

./public-api-cli options set 
	--key=nalejAddress 
	--value=api.server.nalej.com
```

To check if these commands have executed correctly and the options are in fact set, you can use the command:

```bash
./public-api-cli options list
```

### Login

After this, we can log in normally:

```bash
./public-api-cli login 
    --email=user@nalej.com 
    --password=password
```



## Web Platform login

With a browser, we can go to the login page provided by the Nalej administration team, and use our Nalej user and password to get in the system.

![Login page](../.gitbook/assets/login_web.png)

Once you enter, you can see the platform structure at a glance, and start interacting with it.

#### Components and terminology

The first screen is the **Organization** section, which contains a view of all members of the organization and its subscription plan. There is a section column in the left part of the screen.

From here you can go to the **Resources** view and interact with the clusters in the system, and the nodes they manage.

You can also go to the **Devices** view, where you can see all the devices in the system and the device groups that contain them.

Finally, in the **Applications** view you can interact with the registered and deployed apps.

For more information on any of these views, please go to the corresponding section of this documentation, where the different views are described in detail.