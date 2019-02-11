 The system supports specifying the application structure in the form of an application descriptor. An application descriptor is an entity that contains all the information required to launch a complex application composed of different services. The overall structure of an application descriptor is as follows:

```json
{   
	"name": "Sample application",   
    "description": "This is a basic descriptor of an application",   
    "labels": {
        ...   
    },
    "rules": [
        ...   
    ],
    "services": [
        ...   
    ] 
 }  
```



An application descriptor contains a name and a descriptor to describe the purpose of the application to the users that will deploy them. It also contains a set of labels that will be used in the future to facilitate queries, and two main sections: rules and services. The rules define how the different services are connected among themselves, the services contain the list of services that need to be deployed in order for the application to work properly. The full list of options can be easily accessed through:

## Rules

The rule entity determines the connectivity of a service with the others. To specify a service:

```json
`{       "rule_id": "<rule_id>",       "name": "description...",       "source_service_id": "<service_id>",       "source_port": <service_source_port>,       "access": 1,       "auth_services": [         "<service_id_that_wants_to_access_the_service>"       ]     },`
```

Where:

- rule_id is the identifier of the rule.
- name is the user friendly name of the rule
- source_service_id contains the identifier of the source service the rule targets.
- source_port contains the source port
- access contains the type of access allowed. Use 1 to signal that the service is accessible by other app services and 2 to signal that the service is publicly available.
- auth_services contains a list of service identifiers that access the service.

Example:

```json
`{       "rule_id": "002",       "name": "allow access to mysql",       "source_service_id": "mysql",       "source_port": 3306,       "access": 1,       "auth_services": [         "wordpress"       ]     },`
```



## Services

A service defines a component of the application. The elements that describe a service are:

```json
`{       "service_id": "<service_identifier>",       "name": "<service_name>",       "description": "<service description>",       "image": "<docker image>",       "specs": {         "replicas": <num_replicas>       },       "storage": [         {           "mount_path": "<path_to_be_mounted>"         }       ],       "exposed_ports": [         {           "name": "<port_name>",           "internal_port": <port_number>,           "exposed_port": <port_number>         }       ],       "environment_variables": {         "<env_name>": "<env_value>"       },       "labels": {         "app": "<app_name>"       }     },`
```

Where:

- service_identifier is the identifier that will be used to refer to this service in the application descriptor.
- service_name is the user friendly name of the service
- service_description is the user friendly description of the service
- image is the name of the docker image
- num_replicas is the number of replicas to be deployed
- storage defines the storage required by the image. It is an optional field.
- exposed ports defines the ports that are exposed by the container
- environment variables specifies the environment variables required by the containers
- labels define the labels of the service. Notice that the app label is mandatory.



Example:

```json
`{       "service_id": "mysql",       "name": "simple-mysql",       "description": "A MySQL instance",       "image": "mysql:5.6",       "specs": {         "replicas": 1       },       "storage": [         {           "mount_path": "/tmp"         }       ],       "exposed_ports": [         {           "name": "mysqlport",           "internal_port": 3306,           "exposed_port": 3306         }       ],       "environment_variables": {         "MYSQL_ROOT_PASSWORD": "root"       },       "labels": {         "app": "simple-mysql",         "component": "simple-app"       }     },`
```

### Using private images

In order to access private images the user should provide the credentials for downloading those. In order to use this images, add the following options to the service descriptor:

```json
`{       "service_id": "server",       "name": "performance-server",       "description": "Performance test server",       "image": "myrepo/myorg/performance-server:v0.2.0",       "credentials": {         "username": "username",         "password": "password",         "email": "email@email.com",         "docker_repository": "https://myrepo.url"       }, 		...     },`
```

Where:

- username is the username to log into the remote repository
- password is the password to log into the remote repository
- email is the email of the user. Depending on the type of remote repository, use the email of the user required to log into the system.
- docker_repository contains the HTTPS url of the remote repository

### Passing arguments to the images

To pass arguments to the docker images, use the run_arguments attribute as in the following example:

```json
`{       "service_id": "myservice",       "name": "Sample service",       "description": "A sample image accepting run arguments",       "image": "run-test:v0.1.0", 	  "run_arguments" : ["arg1", "arg2", ..., "argN"] 		...     },`
```



### Attaching storage to services

To attach storage to a given service, use the following construct:

```json
`{       "service_id": "myservice",       "name": "Sample service",       "description": "A sample image accepting run arguments",       "image": "run-test:v0.1.0",       "storage": [         {           "size": 104857600,           "mount_path": "/tmp",           "type": 1         }       ], ... }`
```

To create ephemeral storage use type 0, type 1 will provide persistent storage.



## Example

As an example, the following descriptor contains an application composed of mysql and wordpress.

```json
`{   "name": "Sample application",   "description": "This is a basic descriptor of an application",   "labels": {     "app": "simple-app"   },   "rules": [     {       "rule_id": "001",       "name": "allow access to wordpress",       "source_service_id": "2",       "source_port": 80,       "access": 2     }   ],   "services": [     {       "service_id": "1",       "name": "simple-mysql",       "description": "A MySQL instance",       "image": "mysql:5.6",       "specs": {         "replicas": 1       },       "storage": [         {           "mount_path": "/tmp"         }       ],       "exposed_ports": [         {           "name": "mysqlport",           "internal_port": 3306,           "exposed_port": 3306         }       ],       "environment_variables": {         "MYSQL_ROOT_PASSWORD": "root"       },       "labels": {         "app": "simple-mysql",         "component": "simple-app"       }     },     {       "service_id": "2",       "name": "simple-wordpress",       "description": "A Wordpress instance",       "image": "wordpress:5.0.0",       "specs": {         "replicas": 1       },       "storage": [         {           "mount_path": "/tmp"         }       ],       "exposed_ports": [         {           "name": "wordpressport",           "internal_port": 80,           "exposed_port": 80,           "endpoints": [             {               "type": 2,               "path": "/"             }           ]         }       ],       "environment_variables": {         "WORDPRESS_DB_HOST": "NALEJ_SERV_1",         "WORDPRESS_DB_PASSWORD": "root"       },       "labels": {         "app": "simple-wordpress",         "component": "simple-app"       }     }   ] }  `
```



## Known limitations

- In this version, connectivity among services is not limited
- Ephemeral storage is used for user applications
- Labels must be set on each service.





 