# How to create an application descriptor

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

* *rule\_id* is the rule identifier.
* *name* is the user friendly name of the rule
* *target\_service\_group\_name* contains the name of the group where the service to be accessed can be found.
* *target\_service\_name* contains the name of the service to be accessed.
* *target\_port* contains the port that is affected by the current rule.
* *access* contains the type of access allowed. Use 1 to signal that the service is accessible by other app services and 2 to signal that the service is publicly available.

> I have some doubts about the structure about the ACCESS parameters when the value is not 2, but 1 (for example). I don't know if there have been changes regarding this, or how to integrate authServiceGroupName and DeviceGroups in the rule structure.
>
> Also, is there a way to assign a rule to all the services in a group?

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

A service group is a collection of services that must be deployed following a given collocation policy.

> var CollocationPolicy_name = map[int32]string{
> 	0: "SAME_CLUSTER",
> 	1: "SEPARATE_CLUSTERS",
> }
>
> I would need an explanation about this, since I didn't see it in the example. I understand that 0 is the default value, so by default the services are deployed in the same cluster. Is this the only reason to put a service in a specific service group? The collocation policy?

### Services

A service defines a component of the application. The elements that describe a service are:

```javascript
{       
    "service_id": <service_identifier>,       
    "name": <service_name>,           
    "image": "<docker image>",       
    "specs": {         
        "replicas": <num_replicas>       
    },       
    "storage": [         
        {           
            "mount_path": "<path_to_be_mounted>"         
        }       
    ],
    "exposed_ports": [         
        {           
            "name": "<port_name>",           
            "internal_port": <port_number>,           
            "exposed_port": <port_number>         
        }       
    ],       
    "environment_variables": {         
        "<env_name>": "<env_value>"       
    },       
    "labels": {         
        "app": "<app_name>"       
    }     
 },
```

Where:

* *service\_identifier* is the identifier that will be used to refer to this service in the application descriptor.
* *service\_name* is the user friendly name of the service.
* *service\_description* is the user friendly description of the service.
* *image* is the name of the docker image.
* *num\_replicas* is the number of replicas to be deployed.
* *storage* defines the storage required by the image. It is an optional field.
* *exposed\_ports* defines the ports that are exposed by the container.
* *environment\_variables* specifies the environment variables required by the containers.
* *labels* define the labels of the service. Notice that the app label is mandatory.

Example:

```javascript
{       
    "service_id": "mysql",       
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
```



### Using private images

In order to access private images, the user should provide the credentials for downloading them. To use them, add the following options to the service descriptor:

```javascript
{       
    "service_id": "server",       
    "name": "performance-server",       
    "description": "Performance test server",       
    "image": "myrepo/myorg/performance-server:v0.2.0",      
    "credentials": {         
        "username": "username",         
        "password": "password",         
        "email": "email@email.com",         
        "docker_repository": "https://myrepo.url"       
    },        
 ...     
 },
```

Where:

* username is the username to log into the remote repository
* password is the password to log into the remote repository
* email is the email of the user. Depending on the type of remote repository, use the email of the user required to log into the system.
* docker\_repository contains the HTTPS url of the remote repository

### Passing arguments to the images

To pass arguments to the docker images, use the run\_arguments attribute as in the following example:

```javascript
{       
    "service_id": "myservice",       
    "name": "Sample service",       
    "description": "A sample image accepting run arguments", 
    "image": "run-test:v0.1.0",       
    "run_arguments" : ["arg1", "arg2", ..., "argN"] 
        ...     
 },
```

### Attaching storage to services

To attach storage to a given service, use the following construct:

```javascript
{       
    "service_id": "myservice",       
    "name": "Sample service",       
    "description": "A sample image accepting run arguments", 
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

To create ephemeral storage use type 0, type 1 will provide persistent storage.

## Example

As an example, the following descriptor contains an application composed of mysql and wordpress.

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
}{
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
        "WORDPRESS_DB_HOST": "NALEJ_SERV_1",
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

## Known limitations

* In this version, connectivity among services is not limited
* Ephemeral storage is used for user applications
* Labels must be set on each service.

