# How to turn a Raspberry Pi (or any device) into a device in your Nalej app

I know you have been fascinated with Nalej's possibilities from the get-go, and more so since you learned that you could use that Raspberry Pi you've been waiting for an excuse to buy. If you needed a sign to move it from the wishlist to the shopping cart, this is it: in this easy tutorial we're going to show you how to install, configure and use a device in a Nalej application.

## The Scenario

We want to deploy an instance of Kibana with ElasticSearch, and we want a device to collect the data that Kibana is going to manage. That device would be a brand new Raspberry Pi, so we will install Nalej SDK in it, and activate and configure the SDK so that it connects with Nalej automatically. 

Then we will create the application descriptor that will allow our application to deploy. This descriptor will have some parameters we will be able to configure, like the name of the device group our device belongs to. Once this is done, we will be able to include the app in the system and deploy it. 

## The Device

> <https://github.com/nalej/nalej-iot-device-sdk-python/blob/master/README.md>
>
> para el device necesitamos:
>
> - instalar el sdk
> - 

## The Application

Now that it's configured, we need to take care of the application side. And the first thing to do regarding the application is its descriptor.

### Application Descriptor

The general structure of a descriptor is, as you know, as follows:

```bash
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
  ],
  "parameters":[
   ...
  ],
}
```

We will start thinking about the services we need for our application.

- As we said, we need **Kibana** to display the data sent by the device.

- We also said we would use Kibana with **ElasticSearch**, so we also need that.

- Having devices implies some kind of communication between the device and the server. For that we will use **MQTT**, with a global instance (the broker) in the server and a local instance (a client) in each device.

- Lastly, we need something that can deliver the MQTT messages to Elastic easily. This will be solved by a **Beat**. 

  

So, as we said, we would need two service groups, the `core` (which will have Kibana, ElasticSearch, the Beat and the core instance of MQTT) and the `gateway` (which will have the local instance of MQTT). The `groups` part of the descriptor, then, would look like this:

```json
 "groups": [
    {
      "name": "core",
      "services": [
        {
          "name": "kibana",
          "description": "Kibana",
          "image": <image_path>,
          "specs": {
            "replicas": 1
          },
          "exposed_ports": [
            {
              "name": "public",
              "internal_port": xxxx,
              "exposed_port": xxxx,
              "endpoints": [
                {
                  "type": 2,
                  "path": "/"
                }
              ]
            }
          ],
          "environment_variables": {
            "ELASTICSEARCH_URL": <url:port>
          },
          "deploy_after": [
            "elastic"
          ]
        },
        {
          "name": "elastic",
          "description": "Elastic",
          "image": <image_path>,
          "storage": [
            {
              "size": 104857600,
              "mount_path": <mount_path>
            }
          ],
          "specs": {
            "replicas": 1
          },
          "exposed_ports": [
            {
              "name": "elasticport",
              "internal_port": xxxx,
              "exposed_port": xxxx
            }
          ],
          "environment_variables": {
            "cluster.name": "elastic-cluster",
            "bootstrap.memory_lock": "true",
            "ES_JAVA_OPTS": "-Xms512m -Xmx512m",
            "discovery.type": "single-node"
          }
        },
        {
		  "name": "mqttbeat",
          "description": "MQTT Beat",
          "image": <mqtt_beat_image_path>,
          "specs": {
            "replicas": 1
          },
          "configs": [
            {
              "content": "content",
              "mount_path": "/conf/mqttbeat.yml"
            }
          ],
          "labels": {
            "app": "mqttbeat"
          },
          "run_arguments": [
            "--path.config=/conf/"
          ]  
        },            
        {
          "name": "coremqtt",
          "description": "VerneMQ MQTT message broker",
          "image": <image_path>,
          "credentials": {
            "username": <username>,
            "password": <password>,
            "email": <email>,
            "docker_repository": <repository>
          },
          "specs": {
            "replicas": 1
          },
          "exposed_ports": [
            {
              "name": "mqtt-port",
              "internal_port": xxxx,
              "exposed_port": xxxx
            }
          ],
          "environment_variables": {
            "NALEJ_TRUSTED_USER": <trusted_user>,
            "NALEJ_TRUSTED_PASSWORD": <trusted_pword>
          }
        }
      ],
      "specs": {
        "replicas": 1,
        "deployment_selectors": {
          "cloud": "azure"
        }
      }
    },
    {
      "name": "gateway",
      "services": [
        {
          "name": "mqtt",
          "description": "VerneMQ MQTT message broker",
          "image": <image_path>,
          "credentials": {
            "username": <username>,
            "password": <password>,
            "email": <email>,
            "docker_repository": <repository>
          },
          "specs": {
            "replicas": 1
          },
          "exposed_ports": [
            {
              "name": "mqtt-port",
              "internal_port": xxxx,
              "exposed_port": xxxx
            }
          ],
          "environment_variables": {
            "NALEJ_TRUSTED_USER": <trusted_user>,
            "NALEJ_TRUSTED_PASSWORD": <trusted_pword>
          }
        }
      ],
      "specs": {
        "multi_cluster_replica": true
      }
    }
  ],
```

We can see the two service groups we need to declare, and the services in each one. There are some configuration variables we will talk about in another tutorial, but by now it's enough to know that you will have to ask for them to your Nalej administrator.

All these services need some rules to communicate. 

- Kibana must be accesible publicly, so we can display the recollected data, but the others should not be. 
- Kibana must have access to Elastic, to get the information, and Beats should have access to Elastic too, to leave information. 
- MQTT should allow access to Beats to its core instance (so Beats can collect the messages from the message queue and pass them on to ElasticSearch). 
- Lastly, the devices should have access to the gateway instance of MQTT, to be able to send messages.

How can you describe such a complex net of relationships? It would look like this:

```json
 "rules": [
    {
      "name": "Allow public access to kibana",
      "target_service_group_name": "core",
      "target_service_name": "kibana",
      "target_port": 5601,
      "access": 2
    },
    {
      "name": "Allow kibana access to elastic",
      "target_service_group_name": "core",
      "target_service_name": "elastic",
      "target_port": 9200,
      "access": 1,
      "auth_service_group_name": "core",
      "auth_services": [
        "kibana"
      ]
    },
    {
      "name": "Allow mqttbeats access to elastic",
      "target_service_group_name": "core",
      "target_service_name": "elastic",
      "target_port": 9200,
      "access": 1,
      "auth_service_group_name": "core",
      "auth_services": [
        "mqttbeats"
      ]
    },
    {
      "name": "Allow mqttbeats to access core mqtt",
      "target_service_group_name": "core",
      "target_service_name": "coremqtt",
      "target_port": 1883,
      "access": 1,
      "auth_service_group_name": "core",
      "auth_services": [
        "mqttbeats"
      ]
    },
    {
      "name": "allow access to mqtt from device groups",
      "target_service_group_name": "gateway",
      "target_service_name": "mqtt",
      "target_port": 1883,
      "access": 3,
      "device_group_names": [
        "raspberry"
      ]
    }
  ],
```

The last thing we need to do is specify the list of parameters that we will configure when whe deploy the application. Which, in our case, consists only of one parameter: the device group name.

As you can see, the device group name written in the last rule is `raspberry`. This will be the default name for the device group, but we need to be able to specify another one if we want to. So, let's include the parameter section:

```json
"parameters": [
    {
        "name":"deviceGroupName",
        "description": "device group name",
  		"path":"rules.4.DEVICE_GROUP_NAME",
        "type": 4,
        "category":0,
        "required": false
    },
]
```

Here we have a typical declaration for a parameter. In this case, the parameter called `deviceGroupName` has:

- a simple `description`.
- a `path`: this tells us where to find the variable in the descriptor, since the variable must exist beforehand so we can substitute its value with a new one. In this case, this variable is in the fifth rule (starting from 0), and has the name `DEVICE_GROUP_NAME`.
- a `type`, to be chosen between boolean (0), integer (1), double (2), enum (3), string (4) or password (5). In this case, it's a `string`.
- a `category`, which is an indicative of this parameter being needed for a basic configuration (0) or an advanced one (1).
- a flag telling us if the parameter is `required` or optional. In this case, it's optional.

And that's it! You have finished your application descriptor, and can now deploy an instance of your application in Nalej. How to do that, you ask? There is a step-by-step tutorial [here](appdeployment_wclusters.md), and you can find more information [here](../applications/applications-1.md) if you have further questions.