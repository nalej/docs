# Docker Compose application

You have Nalej as your system, but there are some apps that you have in Docker Compose and don't know how to deploy in Nalej. No worries! It's easier than it seems.

## The App Descriptor

The first thing that needs to be tackled is the app descriptor, which is what you need to include the app in the system.

[Do you remember how to create your own app descriptor?](../applications/app_descriptors.md) I'm sure you do. I'm also sure you still have nightmares from trying to get the correct structure for your application. The thing is, just by modifying and adding a couple of sections your descriptor will be good to go.

So, your app descriptor for a normal app would be something like this:

```javascript
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

* **username** and **password** are the credentials to log into the remote repository.
* **email** is the email of the user. Depending on the type of remote repository, use the email of the user required to log into the system.
* **docker\_repository** contains the HTTPS url of the remote repository.

This is the bare minimum and, depending on the application, the only thing you need to add to your already beautifully done app descriptor.

### Passing arguments to the images

Oh, but it's never that easy, isn't it. Your Docker app needs some arguments, and you are sure that we didn't think of _that_ situation, did we. Well, of course we did!

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

## Adding & deploying the app to the system

Once this is done, the only thing left to do is adding the application to the system and deploying an instance of it. These steps are the same for every application, so our suggestion is to check out our [Application deployment](appdeployment_wclusters.md) tutorial to see how to do it.