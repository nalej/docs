# Structure of an application descriptor

The system supports specifying the application structure in the form of an application descriptor. An application descriptor is an entity that contains all the information required to launch a complex application composed of different services. The overall structure of an application descriptor is as follows:

```javascript
{   
    "name": "Sample application",   
    "labels": {
        ...   
    },
    "rules": [
        ...   
    ],
    "groups": [
        {
		...
            "services": [
                ...
            ]
    	}
    ] 
 }
```

An application descriptor contains a **name** and a **descriptor** to describe the purpose of the application to the users that will deploy them. It also contains a set of **labels** that will be used in the future to facilitate queries, and two main sections: **rules** and **service groups**. The *rules* define how the different services are connected among themselves, and the *service groups* contain the list of services that need to be deployed in order for the application to work properly, bundled in groups.

## Rules

The rule entity determines the connectivity of a service with the others. To specify a service:

```javascript
{
  "rule_id": <rule_id>,       
  "name": "this is what this rule does",       
  "target_service_group_name": <service_group_name>,       
  "target_service_name": <service_name>,
  "target_port": <port>,       
  "access": 2     
},    
```

Where:

* **rule\_id** is the rule identifier.

* **name** is the user friendly name of the rule.

* **target\_service\_group\_name** contains the name of the group where the service to be accessed can be found.

* **target\_service\_name** contains the name of the service to be accessed.

* **target\_port** contains the port that is affected by the current rule.

* **access** contains the type of access allowed. 

  * Use **1** to signal that the service is accessible by other app services. The correct way to specify the services would be:

    ```json
    "access": 1
    "auth_service_group": {
        "name": <service_group_name>,
    	"auth_services": [
            <service_name_1>,
        	<service_name_2>,
        	...
        ]    
    }
    ```

  * Use **2** to signal that the service is publicly available.

  * Use **3** to signal that the service is available only for some devices.

    ```json
    "access": 3
    "device_groups": [
        <device_name_1>,
        <device_name_2>,
        ....
    ]
    ```

Example:

```json
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
```



## ServiceGroups

A service group is a collection of services that can be replicated together. The structure of a service group is as follows:

```json
  "groups": [
    {
      "name": "g1",
      "services": [
        ...       
      ],
      "specs": {
        "num_replicas": 1
      }
    }
  ]
```

Where:

- **name** is the name we give to the service group.
- **services** is the collection of services the group contains.
- **specs** defines the specifications for the group. The different parameters here are 
  - **num\_replicas**, which is the number of replicas of this group that are going to be deployed, and 
  - **multicluster_replica**, which is a boolean that states whether or not the replicas will be deployed in the same cluster.

### Services

A service defines a component of the application. The elements that describe a service are:

```javascript
{              
    "name": <service_name>,           
    "image": <docker image>,       
    "specs": {         
        "replicas": <num_replicas>       
    },
    "configs": [
        {
          "config_file_id": <config_file_id>,
          "content": <config_file_content>,
          "mount_path": <config_file_path>
        }
      ],
    "storage": [         
        {           
            "mount_path": <path_to_be_mounted>         
        }       
    ],
    "exposed_ports": [         
        {           
            "name": <port_name>,           
            "internal_port": <port_number>,           
            "exposed_port": <port_number>         
        }       
    ],       
    "environment_variables": {         
        "<env_name>": <env_value>       
    },       
    "labels": {         
        "app": <app_name>       
    }     
 },
```

Where:

* **service\_name** is the name of the service.
* **image** is the name of the docker image.
* **specs** defines the specifications for the service. In it, **replicas** is the number of replicas of this service to be deployed.
* **configs** defines the configuration files that the service may need. In it, 
  * **config\_file\_id** is the identifier of each specific configuration file, 
  * **content** is the content the configuration file should have, and
  * **mount\_file** is the path where the file should be in the cluster, so the system can create it and fill it with what is in the **content** parameter.
* **storage** defines the storage required by the image. It is an optional field.
* **exposed\_ports** defines the ports that are exposed by the container.
* **environment\_variables** specifies the environment variables required by the containers.
* **labels** define the labels of the service. Notice that the app label is mandatory.

Example:

```javascript
{         
    "name": "simple-mysql",       
    "description": "A MySQL instance",       
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
```



## Using private images

In order to access private images, the user should provide the credentials for downloading them. To use them, add the following options to the service descriptor:

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

* **username** is the username to log into the remote repository.
* **password** is the password to log into the remote repository.
* **email** is the email of the user. Depending on the type of remote repository, use the email of the user required to log into the system.
* **docker\_repository** contains the HTTPS url of the remote repository

### Passing arguments to the images

To pass arguments to the docker images, use the **run\_arguments** attribute as in the following example:

```javascript
{       
    "name": "Sample service with image accepting run arguments",       
    "image": "run-test:v0.1.0",       
    "run_arguments" : ["arg1", "arg2", ..., "argN"] 
        ...     
 },
```

## Attaching storage to services

To attach storage to a given service, use the following construct:

```javascript
{           
    "name": "Sample service",       
    "image": "run-test:v0.1.0",       
    "storage": [         
        {           
            "size": 104857600,           
            "mount_path": "/tmp",           
            "type": 1         
        }       
    ],
 ... 
 }
```

Where **type** will define the type of storage to create, being:

- **0**: ephemeral storage.
- **1**: persistent storage.



## Example

As an example, the following descriptor contains an application composed of mysql and wordpress.

```javascript
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
            "WORDPRESS_DB_HOST": "NALEJ_SERV_SIMPLE-MYSQL:3306",
            "WORDPRESS_DB_PASSWORD": "root"
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

