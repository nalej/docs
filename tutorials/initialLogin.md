# Initial login

Before getting started with the different parts of the platform, we're going to tackle the very first step of the way: the first time we log in the platform. There are two ways we can log in: through the command line interface (CLI) and through the web management interface.

## CLI Login

#### Setting your user options

The very first time you log in the system there are some variables that need to be established. They are needed for each interaction, so setting them up before starting lets us omit them in each request. These variables are the **certificate** you received, and the addresses of the **Nalej login server** and the **Nalej API server**. Gather all data (from the information the Nalej administration provided when signing up for the service), go to the `public-api-cli/bin` folder in your computer and execute the following instructions:

```bash
./public-api-cli options set --key=cacert --value=/Users/youruser/.../certificate.crt

./public-api-cli options set --key=loginAddress --value=login.server.nalej.com

./public-api-cli options set --key=nalejAddress --value=api.server.nalej.com
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

![Login page](Users/svillanueva/nalej_docs/docs/.gitbook/assets/login_web.png)

Once you enter, you can see the platform structure at a glance, and start interacting with it.

#### Components and terminology

The first screen we see is the **Organization** section, which contains a view of all members of the organization and its subscription plan.

> TODO: revise this. It's copied from the doc in the Drive.

- Organization info card: the most relevant organization information.
- Members card: organization members card allows the Owner to create, edit or delete users from the organization. 

**Resources** - a view that contains the clusters that contain nodes.

- Summary card: briefing of applications information that includes deployed applications and registered apps count.
- Clusters card: extended information related to a specific cluster.
- Nodes timeline: line chart that enables the user to know the nodes current status.
- Cluster list: an updated list that contains the clusters information. This card allows the user to edit name and description.

**Applications** - a view that contains the registered and deployed apps.

- Summary card: a briefing of the organization resources, including a number of total clusters and nodes, and clusters status.
- Status timeline: aggregation of applications current status represented as a line chart
- Deployed app list: list of deployed applications that shows some basic information.
- App extended info: a partial view that shows a specific application extended info, including a graph with the services relations and an endpoints list. 

