# Application deployment, management and removal.

This section will have all the documents related to app deployment, management and removal. You will also find what you need about application descriptors: what they are, how to create one, and how to use one in the system.

Now that we know how the clusters work, it's time to start deploying applications in the system. Let's see how to do this.

## Application deployment

The management of the life cycle of an application is only available through the Public API CLI by now. The Web Interface allows us to check the current status of the different applications already deployed in the system. With that in mind, we will focus in the commands needed to manage the life cycle through the CLI, and afterwards we will show how to check the information related to the application in the Web Interface.

The process of deploying an application is as follows:

![This is the process to follow when deploying an instance of an application.](../.gitbook/assets/app_deployment.png)

So, first you need to create an application descriptor. The documentation for doing so is [over here](app_descriptors.md), but by now let's just say that it should be a JSON file with more or less this aspect:

```json
{
  "name": "Sample application",
  "labels": {
    "app": "simple-app"
  },
  "rules": [
    {
      "rule_id": "001",
      "name": "allow access to wordpress",
      "target_service_group_name": "g1",
      "target_service_name": "2",
      "target_port": 80,
      "access": 2
    }
  ],
  "groups": [
    {
      "name": "g1",
      "services": [
        {
          "name": "simple-mysql",
          "image": "mysql:5.6",
          "specs": {
            "replicas": 1
          },
          "configs": [
        {
          "config_file_id": "1",
          "content": "SG9sYQo=",
          "mount_path": "/config/saludo.conf"
        },
        {
          "config_file_id": "2",
          "content": "QWRpb3MK",
          "mount_path": "/config/despedida.conf"
        }
      ],
          "storage": [
            {
              "size": 104857600,
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
          "name": "simple-wordpress",
          "image": "wordpress:5.0.0",
          "specs": {
            "replicas": 1
          },
          "storage": [
            {
              "size": 104857600,
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
            "WORDPRESS_DB_HOST": <db_host>,
            "WORDPRESS_DB_PASSWORD": <db_password>
          },
          "labels": {
            "app": "simple-wordpress",
            "component": "simple-app"
          },
          "deploy_after": [
            "1"
          ]
        }
      ],
      "specs": {
        "num_replicas": 1
      }
    }
  ]
}
```

This is the descriptor of a WordPress server with an associated MySQL database. Your should look similar, depending on the services you want to deploy.

### Adding the application to the system

Let's suppose you have the application description already covered, and you want to deploy your application now. As stated before, the next step of the process is adding the application to the system. That will be done with the command:

```bash
./public-api-cli app desc add --descriptorPath=/pathtodescriptor
```

It returns a JSON with an application **descriptor ID** inside, which we will need for deploying an instance of this application.

###Deploying the application

Now the application is ready to be deployed! We can do this with:

```bash
./public-api-cli app inst deploy --descriptorID=xxxxxxx --name=name-app
```

Here, as you may have noticed, is also the moment where we name the app with a human-readable name. When this command exits, it returns a JSON with an application **instance ID**, which is what we will use to work with the deployed instance.

## Application management

We can interact with the application in several ways, now that it's deployed. One of the actions we can take is getting its related info, which can be done with:

```bash
./public-api-cli app inst get --instanceID=XXXXXXXXXX
```

This will return a JSON with all the information related to the instance we are checking, for example:

```javascript
"status_name": "RUNNING"
```

will tell us that the application is running correctly, and 

```javascript
"endpoints": [
          "xxxx.xxxxx.appcluster.<yourcluster>.com"
      ],
```

will tell us where the instance is deployed, so we can navigate to it and start working.

### Getting logs from the instance

Once the application is running, it's generating logs and storing them in the system. To access these logs, we can use:

```bash
./public-api-cli log search --instanceID=xxxx > appLogs.json
```

This will return a (most likely) very long JSON file, with the following format:

```json
{
  "organization_id": <org_id>,
  "app_instance_id": <app_inst_id>,
  "entries": [
    {
      "timestamp": {
        "seconds": 1551796628,
        "nanos": 902000000
      },
      "msg": "<logged_info> "
    },
    ...
  ]
}
```

Where each **entry** has a **timestamp** and a **msg**, which is completely dependant on the application that generates the log. Typically, the logged info contains the **log_level**, which can be useful to differentiate an informative log from an error one. Please check the log message format of the application you're consulting before diving in this file.



## Application removal

### Undeploying the instance

OK, so we finished working with this instance, and don't want it to be in the system anymore. In this case, we need to undeploy it. For this, we will need its instance ID.

```bash
./public-api-cli app inst undeploy --instanceID=xxxx
```

That may be all the cleanup needed if this application is something we will use again in the system, since we can deploy it again tomorrow with the same application descriptor.

### Deleting the app

But what if we just don't want the application to be available again? In that case, we need to delete the application from the system, undoing the `add` we executed before. This needs the descriptor ID we got as a response when we added the application to the system.

```bash
./public-api-cli app desc delete  --descriptorID=xxxxx
```

This last step is optional, only needed if we want to delete a specific app from the system, and doesn't need to be done every time we undeploy an instance.



## Application management through web interface

We can see the information related to all the deployed instances of an organization through the web interface. If we click on the "Application" option at the left column of the screen, a screen similar to this one will appear:

> TODO: image

This screen has the following areas:

- A **summary**, where the number of deployed instances and registered applications are shown.
- An **app status timeline**, where the down time of the different instances is displayed.
- A **deployed app list**, where we can see all the info regarding each instance, including its ID, tags and status.

Once an application instance is deployed, it is listed in the main application dashboard. The platform provides users with operational information about the deployed instances. 

By clicking on the info button, the user can view the cluster modal window, where application information is performed.

**Applications graph**

The application graph provides users with a visualization of deployed and running application instances. 

