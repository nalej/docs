# Application Deployment with Nalej

So, you just got Nalej and are itching to start working with it, but don't know where to start. No worries! This document will walk you through the process of deploying your very first application with Nalej.

### Environment setup

For this tutorial we are assuming that there is at least one deployed cluster, and that you are already registered in the system. Also, to use Nalej you need to install the `public-api-cli`package that was sent to you by an administrator. This is what will allow us to interact with the system.

#### Setting your user options

Is this the very first time you log in the platform? There are some variables that are needed for each interaction, so establishing them before starting means we won't have to write them down in each request. These variables, or options, are the **certificate** you received, and the addresses of the **Nalej login server** and the **Nalej API server**. Gather all this data, go to the `public-api-cli/bin` folder in your computer and execute the following instructions:

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

Now you can log in with only your email and password:

```bash
./public-api-cli login 
    --email=user@nalej.com 
    --password=password
```

### Application descriptor

Congratulations! You're in the system. Now, the first thing you should do is create your own application descriptor. Then, you have to add it to the system, and after that the app will be deployed in what we call an instance. Let's go through this process.

![This is the process to follow when deploying an instance of an application.](/Users/svillanueva/nalej_docs/docs/.gitbook/assets/screen-shot-2019-02-11-at-5.58.28-pm.png)

#### Creating an application descriptor

An **application descriptor** is a file with all the essential info to deploy a complex app on Nalej. A very basic application descriptor would look like this:

```javascript
{
  "name": "Sample application",
  "description": "This is a basic descriptor of an application",
  "labels": {
    "app": "simple-app"
  },
  "rules": [
    {
      "rule_id": "001",
      "name": "allow access to wordpress",
      "source_service_id": "2",
      "source_port": 80,
      "access": 2
    }
  ],
  "services": [
    {
      "service_id": "1",
      "name": "simple-mysql",
      "description": "A MySQL instance",
      "image": "mysql:5.6",
      "specs": {
        "replicas": 1
      },
      "storage": [
        {
          "mount_path": "/tmp"
        }
      ],
      "exposed_ports": [
        {
          "name": "mysqlport",
          "internal_port": 3306,
          "exposed_port": 3306
        }
      ],
      "environment_variables": {
        "MYSQL_ROOT_PASSWORD": "root"
      },
      "labels": {
        "app": "simple-mysql",
        "component": "simple-app"
      }
    },
    {
      "service_id": "2",
      "name": "simple-wordpress",
      "description": "A Wordpress instance",
      "image": "wordpress:5.0.0",
      "specs": {
        "replicas": 1
      },
      "storage": [
        {
          "mount_path": "/tmp"
        }
      ],
      "exposed_ports": [
        {
          "name": "wordpressport",
          "internal_port": 80,
          "exposed_port": 80,
          "endpoints": [
            {
              "type": 2,
              "path": "/"
            }
          ]
        }
      ],
      "environment_variables": {
        "WORDPRESS_DB_HOST": "NALEJ_SERV_1:3306",
        "WORDPRESS_DB_PASSWORD": "root"
      },
      "labels": {
        "app": "simple-wordpress",
        "component": "simple-app"
      }
    }
  ]
}
```

This example is the output of the following command:

```bash
./public-api-cli app desc help > appDescExample.json
```

It creates a basic application descriptor for you \(called `appDescExample.json`in this case\), with a Wordpress instance and a mySQL database associated to it. To learn more about them, please visit [this link](app_descriptors.md), where you can find an extensive tutorial on how to make your own.

> this needs to be another document in the system and not redirect to our private documentation.
>
> To learn more about them, please visit [this link](https://daisho.atlassian.net/wiki/spaces/NP/pages/582713431/Application+descriptors), where you can find an extensive tutorial on how to make your own.

#### Adding the application descriptor to the system

After creating the application descriptor, the next step is adding it to the system, which can be done with the following command:

```bash
./public-api-cli app desc add --descriptorPath=/pathtodescriptor
```

It returns an application descriptor ID, which we will need for deploying an instance of this application.

#### Deploying the associated instance

And how would we deploy that instance? With this other command:

```bash
./public-api-cli app inst deploy --descriptorID=xxxxxxx --name=name-app
```

Here, as you may have noticed, is also the moment where we name the app with a human-readable name. When this command exits, it returns a JSON with an application **instance** ID, which is what we will use to work with the deployed instance.

### Working with the deployed instance: getting related info

Now we can start working with the deployed instance, doing things like, for example, getting all the information related to it in the system.

```bash
./public-api-cli app inst get --instanceID=XXXXXXXXXX
```

This command returns a JSON with all the information related to the instance we are checking. Below you can see the JSON obtained while getting the information of an application instance composed by a WordPress server and a MySQL server associated to it:

```javascript
{
  "organization_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "app_descriptor_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "app_instance_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  "name": "wordpress-for-testing",
  "description": "testing instance of WordPress",
  "labels": {
    "app": "simple-app"
  },
  "rules": [
    {
      "app_descriptor_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "rule_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "name": "allow access to wordpress",
      "source_service_id": "2",
      "source_port": 80,
      "access_name": "PUBLIC"
    }
  ],
  "services": [
    {
      "organization_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "app_descriptor_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "app_instance_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "service_id": "1",
      "name": "simple-mysql",
      "description": "A MySQL instance",
      "type_name": "DOCKER",
      "image": "mysql:5.6",
      "specs": {
        "replicas": 1
      },
      "storage": [
        {
          "size": 104857600,
          "mount_path": "/tmp",
          "type_name": "EPHEMERAL"
        }
      ],
      "exposed_ports": [
        {
          "name": "mysqlport",
          "internal_port": 3306,
          "exposed_port": 3306
        }
      ],
      "environment_variables": {
        "MYSQL_ROOT_PASSWORD": "xxxxxx"
      },
      "labels": {
        "app": "simple-mysql",
        "component": "simple-app"
      },
      "status_name": "SERVICE_RUNNING",
      "deployed_on_cluster_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    },
    {
      "organization_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "app_descriptor_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "app_instance_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
      "service_id": "2",
      "name": "simple-wordpress",
      "description": "A Wordpress instance",
      "type_name": "DOCKER",
      "image": "wordpress:5.0.0",
      "specs": {
        "replicas": 1
      },
      "storage": [
        {
          "size": 104857600,
          "mount_path": "/tmp",
          "type_name": "EPHEMERAL"
        }
      ],
      "exposed_ports": [
        {
          "name": "wordpressport",
          "internal_port": 80,
          "exposed_port": 80,
          "endpoints": [
            {
              "type_name": "WEB",
              "path": "/"
            }
          ]
        }
      ],
      "environment_variables": {
        "WORDPRESS_DB_HOST": "YOUR_SERVER:xxxx",
        "WORDPRESS_DB_PASSWORD": "xxxx"
      },
      "labels": {
        "app": "simple-wordpress",
        "component": "simple-app"
      },
      "deploy_after": [
        "1"
      ],
      "status_name": "SERVICE_RUNNING",
      "endpoints": [
          "xxxx.xxxxx.appcluster.<yourcluster>.com"
      ],
      "deployed_on_cluster_id": "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
    }
  ],
  "status_name": "RUNNING"
}
```

Here you can see several interesting things, like the user and password for the admin in this instance of MySQL, or the size of the instance in the cluster, but one of the most important parameters is:

```javascript
"status_name": "RUNNING"
```

Where it tells you the status of the current instance. Since it is "RUNNING", we can start working with it immediately!

### Navigating to the endpoint

The JSON obtained with `app inst get` has another piece of information that can be very useful for us, which is the **endpoint** where the instance is deployed. This information looks like this:

```javascript
"endpoints": [
          "xxxx.xxxxx.appcluster.<yourcluster>.com"
      ],
```

This collection of addresses is where the instance is deployed, and you can access it from any browser and get more information about the instance and the services it uses.

### Undeploying the instance

OK, so we finished working with this instance, and don't want it to be in the system anymore. In this case, we need to undeploy it:

```bash
./public-api-cli app inst undeploy --instanceID=xxxx
```

That may be all the cleanup needed if this application is something we will use again in the system, since we can deploy it again tomorrow with the same application descriptor.

### Deleting the app

But what if we just don't want the application to be available again? In that case, we need to delete the application from the system, undoing the `add` we executed before:

```bash
./public-api-cli app desc delete  --descriptorID=xxxxx
```

This last step is optional, only needed if we want to delete a specific app from the system, and doesn't need to be done every time we undeploy an instance.

## Troubleshooting

### Invalid credentials

_I tried to log in and there is a fatal error saying_ `Invalid credentials`, _what is going on?_

The email or password you entered is wrong, or you are simply not in the system yet. Double-check the email and password you entered, and if you are sure that they are correct, then talk to an administrator to see if you're already registered.

### Error loading CA certificate

_Ok, I got the credentials right, but now there is another error saying_ `Error loading CA certificate`. _Does the system hate me?_

No, it doesn't \(remember, it doesn't know you exist, since you're not logged in yet\). The problem now is that it can't find the certificate. The most common reason for this is that the path is incorrect.

### Unable to login into the platform

_I finally got the credentials and the certificate right, and there's a new error:_ `unable to login into the platform`. _What is happening now?_

There's a problem with the server address. Is it correctly written?

### Cannot load application descriptor

_I got in the system! But now there's something wrong with the application descriptor. The message is_ `cannot load application descriptor`. _What can it possibly mean?_

It can mean that the path to the application descriptor is not right. It can also mean that the application descriptor you're trying to use is empty. Check both possibilities, just in case.

### Cannot add a new application descriptor

_Now there's another error related to the application descriptor. The message now is_ `cannot add a new application descriptor`. _I'm sure about the path and the file has something in it, so it should work, right?_

Not necessarily. The format of the application descriptor must be correct. If there's something essential missing \(like the name of the appilcation to deploy, for example\), it won't work. Compare your application descriptor with the one shown above as an example, and check if there is something missing.

### Cannot deploy application

_I got the descriptorID! But when I try to deploy an instance of the app, there's a message that says:_ `cannot deploy application`. _Please tell me the truth, does the system hate me?_

I seriously doubt so \(but we will check its feelings matrix, just in case\). The problem may have appeared because the descriptorID is not correct. Copy and paste it exactly as it is returned from the `app desc add` command.

### Error 404 when trying to access the endpoint

_Everything went ok, and I fixed all the problems that have appeared until now. But as I was ready to access the endpoint, a_ `404 Not Found` _hit me from out of nowhere. I'm determined to do this. What's happening now?_

There are several variables that can be the issue here, but I'm sure you have already checked any connectivity problems that may be happening. If everything seems fine and it should be working, please get the instance info again with `app inst get` and check if the status is still `"RUNNING"`.

