# How to deploy a Docker Compose app in Nalej

You have Nalej as your system, but there are some apps that you have in Docker Compose and don't know how to deploy in Nalej. No worries! It's easier than it seems.

## The App Descriptor

The first thing that needs to be tackled is the app descriptor, which is what you need to include the app in the system. 

[Remember how to create your own app descriptor?](../applications/app_descriptors.md) I'm sure you do. I'm also sure you still have nightmares from trying to get the correct structure for your application. The thing is, just by modifying and adding a couple of sections your descriptor will be good to go.

So, your app descriptor for a normal app would be something like this:

```json
{
  "name": "Sample application",
  "labels": {
    "app": "simple-app"
  },
  "rules": [
    {
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
          "config_file_name": "saludo",
          "content": "SG9sYQo=",
          "mount_path": "/config/saludo.conf"
        },
        {
          "config_file_name": "despedida",
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
              "internal_port": 3316,
              "exposed_port": 3316
            }
          ],
          "environment_variables": {
            "MYSQL_ROOT_PASSWORD": "pass"
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
            "WORDPRESS_DB_HOST": "SIMPLE-MYSQL:3316",
            "WORDPRESS_DB_PASSWORD": "pass"
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
        "replicas": 1
      }
    }
  ]
}
```

This is perfect... if this app wasn't in Docker. But it is, and we need to modify the descriptor so it fits our necessities. 

### Declaring the use of a private image

So, we need to declare that we're going to use a private image, which is somewhere else, and we need to give the system a way to access this resource. This is established in a piece of the JSON that looks like this:

```javascript
{            
    "name": "performance-server",            
    "image": "myrepo/myorg/performance-server:v0.2.0",      
    "credentials": {         
        "username": <username>,         
        "password": <password>,         
        "email": <email@email.com>,         
        "docker_repository": "https://myrepo.url"       
    },        
 ...     
 },
```

Where:

- **username** and **password** are the credentials to log into the remote repository.
- **email** is the email of the user. Depending on the type of remote repository, use the email of the user required to log into the system.
- **docker\_repository** contains the HTTPS url of the remote repository.

This is the bare minimum and, depending on the application, the only thing you need to add to your already beautifully done app descriptor. 

### Passing arguments to the images

Oh, but it's never that easy, isn't it. Your Docker app needs some arguments, and you are sure that we didn't think of *that* situation, did we. Well, of course we did!

To pass arguments to the docker images, use the **run\_arguments** attribute as in the following example:

```javascript
{       
    "name": "Sample image accepting run arguments",       
    "image": "run-test:v0.1.0",       
    "run_arguments" : [
        "arg1", 
        "arg2", 
        ..., 
        "argN"] 
        ...     
 },
```

And that's everything you need for the application descriptor of your Docker app.

## Deploying the application

Now you have to deploy it in the system. 

### Through the Public API CLI

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

### Web Interface

#### Adding the app to the system

> sfdasdfasdfasdfasdfasdf (capturas)

#### Deploying the associated instance

> Asdfasdfasdfasdfasdf (todo esto con capturas)

## Is the application up in the system?

Now an instance of the application should be up and running in Nalej. You can check its status through the API CLI and through the Web Interface.

### Public API CLI

One of the things we could do to know if the instance is running is getting its information, which we can do with:

```bash
./public-api-cli app inst get --instanceID=XXXXXXXXXX
```

This command returns a JSON with all the information related to the instance we are checking, which looks like this:

```javascript
{
  "organization_id": <org_id>,
  "app_descriptor_id": <app_desc_id>,
  "app_instance_id": <app_inst_id>,
  "name": <name>,
  "labels": {
    "app": "simple-app"
  },
  "rules": [
    {
      "organization_id": <org_id>,
      "app_descriptor_id": <app_desc_id>,
      "rule_id": <rule_id>,
      "name": <name>,
      "target_service_group_name": <service_group_name>,
      "target_service_name": <service_name>,
      "target_port": <port>,
      "access_name": "PUBLIC"
    },
    ...
    
  ],
  "groups": [
    {
      "organization_id": <org_id>,
      "app_descriptor_id": <app_desc_id>,
      "app_instance_id": <app_inst_id>,
      "service_group_id": <service_group_id>,
      "service_group_instance_id": <service_group_instance_id>,
      "name": <service_group_name>,
      "service_instances": [
        {
          "organization_id": <org_id>,
          "app_descriptor_id": <app_desc_id>,
          "app_instance_id": <app_inst_id>,
          "service_group_id": <service_group_id>,
          "service_id": <service_id>,
          "service_instance_id": <service_instance_id>,
          "name": <service_name>,
          "type_name": "DOCKER",
          "image": <image>,
          "specs": {
            "replicas": 1
          },
          "exposed_ports": [
            {
              "name": "simple-app-port",
              "internal_port": <port>,
              "exposed_port": <port>
            }
          ],
          "environment_variables": {
            ...
          },
          "labels": {
            "app": "simple-app",
            "component": "simple-app"
          },
          "status_name": "SERVICE_RUNNING",
          "endpoints": [
            	"xxxx.xxxxx.appcluster.<yourcluster>.com"
          ],
          "deployed_on_cluster_id": <cluster_id>
        },
        ...  
      ],
      "policy_name": "SAME_CLUSTER",
      "status_name": "SERVICE_SCHEDULED",
      "specs": {
        "replicas": 1
      }
    }
  ],
  "status_name": "RUNNING"
}
```

Here you can see several interesting things, like the user and password for the admin in this instance of MySQL, but one of the most important parameters is:

```javascript
"status_name": "RUNNING"
```

Where it tells you the status of the current instance. Since it is "RUNNING", we can start working with it immediately!

### Web Interface

> Asdfasdfasdfasdfasdf (con capturas)





### 