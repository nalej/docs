# How to deploy a Docker Compose app in Nalej

You have Nalej as your system, but there are some apps that you have in Docker Compose and don't know how to deploy in Nalej. No worries! It's easier than it seems.

> primero describir la app. Tendremos que decir una app de ejemplo
>
> Segundo añadir la parte que se refiere a la imagen (using private images en la documentación). Sería guay que hubiera que pasarle argumentos a la imagen.
>
> Tercero desplegar la app.
>
> Cuarto comprobar que la app se ha desplegado.

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
        "num_replicas": 1
      }
    }
  ]
}
```

