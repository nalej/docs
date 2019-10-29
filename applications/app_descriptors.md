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

An application descriptor contains a **name**, a set of **labels** that will be used in the future to facilitate queries, and two main sections: **rules** and **service groups**. The _rules_ define how the different services are connected among themselves, and each _service group_ contains a set of services that need to be deployed in order for the application to work properly.

## Rules

The rule entity determines the connectivity of a service with the others. To specify a service:

```javascript
{     
  "name": "this is what this rule does",       
  "target_service_group_name": <service_group_name>,       
  "target_service_name": <service_name>,
  "target_port": <port>,       
  "access": 2     
},
```

Where:

* **name** is the user friendly name of the rule.
* **target\_service\_group\_name** contains the name of the group where the service to be accessed can be found.
* **target\_service\_name** contains the name of the service to be accessed.
* **target\_port** contains the port that is affected by the current rule.
* **access** contains the type of access allowed.
  * Use **1** to signal that the service is accessible by other app services. The correct way to specify the services would be:

    ```javascript
    "access": 1,
    "auth_service_group_name": <serv_group_name>,
        "auth_services": [
            <service_name_1>,
            <service_name_2>,
            ...
        ]    
    }
    ```

  * Use **2** to signal that the service is publicly available.
  * Use **3** to signal that the service is available only for some devices.

    ```javascript
    "access": 3,
    "device_group_names": [
        <device_group_name_1>,
        <device_group_name_2>,
        ...
    ]
    ```

  * Use **4** to indicate a rule that describes an inbound plug for connections between applications. This will mean that the "target service" will receive connections through this rule. When using this rule, the target port must be exposed on the target service description and the following field must be added to the rule definition:

    * **inbound\_net\_interface**: The name of the inbound net interface that will be linked to this rule

    ```javascript
    "access": 4,
    "inbound_net_interface": <inbound_iface_name>
    ```

  * Use **5** to indicate a rule that describes an outbound plug for connections between applications. This will mean that the "target service" will be able to connect to other applications through this rule using the predefined variable `NALEJ_OUTBOUND_[interface_name]` . When using this rule, the target port must be exposed on the target service description and the following field must be added to the rule definition:

    * **outbound\_net\_interface**: The name of the outbound net interface that will be linked to this rule

    ```javascript
    "access": 5,
    "outbound_net_interface": <outbound_iface_name>
    ```

Example:

```javascript
  "rules": [
    {
      "name": "allow access to wordpress",
      "target_service_group_name": "g1",
      "target_service_name": "2",
      "target_port": 80,
      "access": 2
    }
  ],
```

## Network interfaces

If you want to have communication between your applications, you will need to declare "plugs" to wire them up. You can see the network interfaces as those plugs. Each inbound or outbound interface will be linked to a Service through a Rule. This will allow the services inside the application to connect to other services that live in different applications. On deployment time or with an already installed appliance, the user will be able to connect one outbound interface to an inbound interface to open a secure TCP/IP channel between the services.

On a descriptor, the user can define interfaces with the following properties:

* **inbound\_net\_interfaces**: An array of inbound interfaces. Each of them are described just by its **name**. Must be unique between inbound/outbound/ interfaces.

  ```javascript
  "inbound_net_interfaces": [
      {"name": "WORDPRESS_IN"}
  ]
  ```

* **outbound\_net\_interfaces**: An array of outbound interfaces. Each of them are described with the following properties:

  * **name**: The name of the outbound interface. Must be unique between inbound/outbound/ interfaces.
  * **required**: Boolean flag that indicates if the outbound connection is required by the application. This means that the outbound must be connected on deployment time and the connection cannot be safely removed \(the user can force it through a parameter\). Default value is false.

  ```javascript
  "outbound_net_interfaces": [
      {"name": "MYSQL", "required": true},
      {"name": "EXTERNAL_LOGGER"}
  ]
  ```

## Service groups

A service group is a collection of services that can be replicated together. Usually, a service group specifies highly coupled applications, like Wordpress and MySQL. A service group is defined by a **group name**, a list of **services** and **deployment specifications**.

The structure of a service group is as follows:

```javascript
  "groups": [
    {
      "name": <group_name>,
      "services": [
        ...       
      ],
      "specs": {
        "multi_cluster_replica": <true|false>,
        "replicas": <num_replicas>,
        "deployment_selectors": {
          "<label_name>": "<label_value>",
        }
      }
    },
    ...
  ]
```

Where:

* **name** is the name we give to the service group. It must be unique in the context of the application.
* **services** is the collection of services the group contains. There must be at least one service defined in the group.
* **specs** defines the deployment specifications for the group. The different parameters here are:
  * **multicluster\_replica**, which is a boolean that states whether  the replicas will be deployed in the same cluster \(=_false_\), or on the contrary they will be deployed into any available cluster \(=_true_\). By default it is set to _false_.
  * **num\_replicas**, which is the number of replicas of this group that are going to be deployed. These replicas will appear as different instances in the system. By default it is set to 1.
  * **deployment\_selectors**, which is a collection of labels and values that is checked against the available clusters. Only those clusters with all the labels and values indicated by the deployment\_selectors are considered to be candidates.

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
          "config_file_name": <config_file_name>,
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
* **specs** defines the specifications for the service. In it, 
  * **replicas** is the number of replicas of this service to be deployed. These replicas will be part of the same instance in the system \(unlike the replicas at service group level, which will be seen as different instances\).
* **configs** defines the configuration files that the service may need. In it, 
  * **config\_file\_id** is the identifier of each specific configuration file, 
  * **content** is the content the configuration file should have, and
  * **mount\_file** is the path where the file should be in the cluster, so the system can create it and fill it with what is in the **content** parameter.
* **storage** defines the storage required by the image. It is an optional field.
* **exposed\_ports** defines the ports that are exposed by the container.
* **environment\_variables** specifies the environment variables required by the containers.
* **labels** define the labels of the service. The **app** label is mandatory.

Example:

```javascript
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
        "MYSQL_ROOT_PASSWORD": <mysql_pword>      
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

* **username** and **password** are the credentials to log into the remote repository.
* **email** is the email of the user. Depending on the type of remote repository, use the email of the user required to log into the system.
* **docker\_repository** contains the HTTPS url of the remote repository.

### Passing arguments to the images

To pass arguments to the docker images, use the **run\_arguments** attribute as in the following example:

```javascript
{       
    "name": "Sample image accepting run arguments",       
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

Where **size** is the size of the storage we want to attach \(in bytes\), and the **type** will define the type of storage to create, being:

* **0**: ephemeral storage.
* **1**: persistent storage.

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

