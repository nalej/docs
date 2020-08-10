# Docker Compose application

You have Nalej as your platform, but there are some apps that you have in a Docker Compose repository and don't know how to deploy in Nalej. Don't worry, it's easier than it seems. Let's go through it together, shall we?

## The App Descriptor

The first thing that needs to be tackled is the app descriptor, which is what you need to register the application in the system.

Do you remember how to [create your own app descriptor](../cli/applications/app_descriptors.md)? Perfect! You just have to modify and add a couple of sections, and your descriptor will be good to go.

So, your app descriptor for a normal app would be something like this:

```javascript
{
  "name": "Simple wordpress",
  "description": "Wordpress with a mySQL database"
  "labels": {
    "app": "simple-wordpress-mysql"
  },
  "rules": [
    {
      "name": "allow access to wordpress",
      "target_service_group_name": "group1",
      "target_service_name": "simplewordpress",
      "target_port": 80,
      "access": 2
    },
    {
      "name": "allow access to mysql",
      "target_service_group_name": "group1",
      "target_service_name": "simplemysql",
      "target_port": 3306,
      "access": 1,
      "auth_service_group_name": "group1",
      "auth_services": [
        "simplewordpress"
        ]
    }
  ],
  "groups": [
    {
      "name": "group1",
      "services": [
        {
          "name": "simplewordpress",
          "image": "wordpress:5.0.0",
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
            "WORDPRESS_DB_HOST": "NALEJ_SERV_SIMPLEMYSQL:3306",
            "WORDPRESS_DB_PASSWORD": "root"
          },
          "deploy_after": [
            "simplemysql"
          ],
          "labels": {
            "app": "simple-wordpress",
            "component": "simple-app"
          }
        },
        {
          "name": "simplemysql",
          "image": "mysql:5.6",
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
        }
      ]
    }
  ]
}
```

This would be perfect... if this app was in our platform. But it isn't, so let's modify the descriptor to fit our necessities.

### Declaring the use of a private image

We need to declare that we're going to use a private image (which is somewhere else in a Docker repository), and we need to give the system a way to access this resource. This is established when declaring the service, in a piece of the JSON that looks like this:

```javascript
{            
    "name": "performance-server",            
    "image": "myrepo/myorg/performance-server:v0.2.0",      
    "credentials": {         
        "username": admin,         
        "password": 123pword,         
        "email": sara.v@company.com,         
        "docker_repository": "https://myrepo.url"       
    },        
 ...     
 },
```

Where:

* **username** and **password** are the credentials to log into the remote repository.
* **email** is the email of the user. Depending on the type of remote repository, use the email of the user required to log into the system.
* **docker\_repository** contains the HTTPS url of the remote repository.

As you can see, another change is that the `image` parameter contains the path to the Docker image we want to use.

This is the bare minimum and, depending on the application, maybe it's also the only thing you need to add to your already beautifully done app descriptor.

### Passing arguments to the images

In case your app needs arguments to work, you can use the **run\_arguments** attribute to provide them, as in the following example:

```javascript
{
  "name": "Docker-Stress",
  "labels": {
    "app": "stress"
  },
  "groups": [
    {
      "name": "stress-group",
      "services": [
        {
          "name": "stress",
          "image": "progrium/stress:latest",
          "run_arguments": [
            "--verbose",
            "--cpu", "2",
            "--hdd", "1",
            "--vm", "2",
            "--backoff", "10000000"
          ],
          "specs": {
            "replicas": 1
          },
          "labels": {
            "app": "stress"
          }
        }
      ]
    }
  ]
}
```

This is also valid whenever you need to pass arguments to images in the platform, it's not only valid for the external Docker images. 

## Adding & deploying the app to the system

Once this is done, the only thing left to do is adding the application to the system and deploying an instance of it. These steps are the same for every application, so our suggestion is to check out our [Application deployment](appdeployment_wclusters.md) tutorial to see how to do it.

