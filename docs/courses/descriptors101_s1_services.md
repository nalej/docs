# Session 1: Services

The application we're going to be working with in this session is the WordPress + MySQL ([wp_mysql.json](https://github.com/nalej/docs/blob/master/docs/courses/desc101-files/desc101-wordpress-mysql.json){target=_blank}). Please download the file and work on it to complete the exercise below.

------

This is the first session in the descriptor creation workshop. In this session, we will describe the parts of a descriptor and define our first service. For more information on this topic, please refer to the main [documentation about descriptors](applications/app_descriptors/).

### Structure of an application descriptor

An application descriptor contains the following sections:

- **Application Info**: This is the beginning of the file, with the name, description, and labels of the application. The fields are mostly human-readable and are useful for identifying the application in the system.
- **Rules**: This section manages the communication of the services in the application. More of this in Session 2. 
- **Groups**: The application consists of one or more *service groups*, which contain services. The groups are created depending on the number of service instances to be deployed, for example.
- **Services**: The services that compose the application.

The use case in this session is an application consisting of a WordPress instance and a MySQL database associated to it. The Application info section of this descriptor looks like this:

```json
{
  "name": "Simple wordpress",
  "description": "Wordpress with a mySQL database",
  "labels": {
    "app": "simple-wordpress-mysql"
  }
```

The most important thing to consider here is the **labels** field, because it's what will identify the application in the platform.

The Rules section is next. In this use case, we will need two rules: one to give public access to the WordPress service, and another to allow communication between WordPress and MySQL.

```json
  "rules": [
    {
      "name": "allow public access to wordpress",
      "target_service_group_name": "group1",
      "target_service_name": "simplewordpress",
      "target_port": 80,
      "access": 2
    },
    {
      "name": "allow wordpress access to mysql",
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
```

In the first rule, the `target_service` is the WordPress service, since we want to have access to it from a browser. Then, the `access` field has the value `2`, since that's how we indicate that the access is public.

In the second rule, however, the `target_service` is the MySQL service. This rule describes the communication between services, and so we need to detail which services can communicate with the `target_service` (in this case, the WordPress service).

The Service Group section is next. We only need one group to gather the two services, and then we start defining each service. 

```json
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
 					///...
        }
      ]
    }
  ]
```

The group only needs a name so we can identify it easily from other parts of the descriptor (in this example, `group1`).

The service, on the other hand, can have a lot more attributes. Not all of them are mandatory, it depends on the specific service that we're describing.

- **`name`**: the name of the service.
- **`description`**: a human-readable description of the service.
- **`image`**: the Docker image of the service.
- **`storage`**: the storage required by the image, and the path where it will be mounted.
- **`exposed_ports`**: the ports exposed by the container. This is a list, and each element contains a port name, the exposed port, the internal port it corresponds to, and the endpoints needed. In this case, the type of the endpoint is `2`, meaning it's accessible for the public, and the path is `/`, so, the main access to the WordPress (not a subpage).
- **`environment_variables`**: the environment variables needed for the image to run properly. In this case, the value of one of this variables (`NALEJ_SERV_MYSQL:3306`) is predefined by the system. 
- **`deploy_after`**: sometimes a service needs some other service to be deployed first. The WordPress service uses a predefined environment variable that contains info about the MySQL service (its address in the platform). This variable needs to be filled before deploying the service, so the WordPress service needs to be deployed after the MySQL service.
- **`labels`**: as we said before, these labels allow us to identify the application in the system.

There are more attributes that can be used in the definition of a service. If you want to know more, please read the [Service Groups](../applications/app_descriptors/#service-groups) and the [Services](../applications/app_descriptors/#services) sections of the documentation.

## Exercise

The exercise for this session is to complete the [wp_mysql.json](https://github.com/nalej/docs/blob/master/docs/courses/desc101-files/desc101-wordpress-mysql.json){target=_blank} file with the definition of the MySQL service, which must contain the following:

- **Image:** mysql:5.6
- **Storage** size: 104857600, mounted at /tmp
- **Internal and exposed ports:** 3306 (name: 'mysqlport')
- **Environment variables**: MYSQL_ROOT_PASSWORD = root
- Add labels “**app**” and “**component**”