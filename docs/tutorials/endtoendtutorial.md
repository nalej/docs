# How to use a Raspberry Pi as a device in your Nalej app

I know you have been fascinated with Nalej's possibilities from the get-go, and more so since you learned that you could use that Raspberry Pi you've been waiting for an excuse to buy. If you needed a sign to move it from the wishlist to the shopping cart, this is it: in this easy and comprehensive tutorial, we're going to show you how to install, configure and use a device in a Nalej application.

## The Scenario

We are going to build a fancy thermometer. For this, we will use a brand new Raspberry Pi with a temperature sensor \(the DHT22 sensor, specifically\), and we will have a web interface to see what it measures. We will deploy an instance of Kibana with ElasticSearch, and the device will collect the data that Kibana is going to manage.

That device would be our Raspberry Pi, so we will install Nalej SDK in it, and activate and configure the SDK so that it connects with Nalej automatically.

Then we will create the application descriptor that will allow our application to deploy. This descriptor will have some parameters we will be able to configure, like the name of the device group our device belongs to. Once this is done, we will be able to include the app in the system and deploy it.

## The Device

You receive your brand new Raspberry Pi with your DHT-22 sensor \([which you have physically connected to it like so](https://www.instructables.com/id/Raspberry-Pi-Tutorial-How-to-Use-the-DHT-22/)\), and have a microSD, and now you want to start configuring it as a Nalej device as soon as possible. Great! So, what do you need?

### Creating a device group

First, you need to get everything ready for your device, and that means that you need to create a new device group for your device to belong to.

You can [add a new device group in the system](../../devices/devices-1#adding-a-device-group) following the instructions in the documentation, or you can also use an already existent device group if you wish. Then, the information you need for registering your device in the system can be obtained following [this other tutorial](../../devices/devices-1#getting-device-related-information).

> DISCLAIMER: by now, the information needed to register a device is only available through the Public API CLI. So, although the tutorials show how to add or manage device groups through the Web Interface too, we recommend doing it through the Public API CLI, so the gathering of information is more straightforward.

### Getting ready for the SDK

Now your device needs an operating system. The only requirement for it to run the SDK is that it has a Python interpreter. For Raspberry Pi, there are many options available and ready to download, but we recommend **Raspbian**, which you can download [from the official Raspberry Pi site](https://www.raspberrypi.org/downloads/) and easily install in your microSD.

Let's suppose you install Raspbian and the installation went uneventfully. In order to be able to use the Nalej Python SDK, you need **Python 3.7** and **PIP 3** \(version 18.1 or higher\). You also need the following libraries:

* requests
* pathlib
* paho-mqtt

For this particular example, the DHT library is also needed, and you can download and install it with the following commands:

```bash
git clone https://github.com/adafruit/Adafruit_Python_DHT.git
cd Adafruit_Python_DHT
sudo apt-get update
sudo apt-get install build-essential python-dev
sudo python setup.py install
```

After that you have to reboot your Pi system to get the Adafruit driver, and then you can start installing Nalej SDK. For that, you just need to follow [this simple step-by-step tutorial](installingsdkindevice.md), and your device will be all set.

## The Application

Now that the device is configured, we need to take care of the application side. And the first thing to do regarding the application is its descriptor.

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

* As we said, we need **Kibana** to display the data sent by the device.
* We also said we would use Kibana with **ElasticSearch**, so we also need that.
* Having devices implies some kind of communication between the device and the server. For that, we will use **MQTT**, with a global instance \(the broker\) in the server and a local instance \(a client\) in each device.
* Lastly, we need something that can deliver the MQTT messages to Elastic easily. This will be solved by a **Beat**, an MQTTBeat specifically.

So we will need only one service group, the `core`, which will have Kibana, ElasticSearch, the Beat and an instance of MQTT. The `groups` part of the descriptor, then, would look like this:

```javascript
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
              "content": <content_in_base64>,
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
        "replicas": 1,
        "deployment_selectors": {
          "cloud": "azure"
        }
      }
    }
  ],
```

We can see the two service groups we need to declare and the services in each one. There are some configuration variables we will talk about in another tutorial, but by now it's enough to know that you will have to ask for them to your Nalej administrator.

All these services need some rules to communicate.

* Kibana must be accessible publicly, so we can display the recollected data, but the others should not be. 
* Kibana must have access to Elastic, to get the information, and Beats should have access to Elastic too, to leave information. 
* MQTT should allow access to Beats to its core instance \(so Beats can collect the messages from the message queue and pass them on to ElasticSearch\). 
* Lastly, the devices should have access to the gateway instance of MQTT, to be able to send messages.

Such a complex net of relationships would look like this in the descriptor file:

```javascript
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
      "name": "Allow mqttbeats to access mqtt",
      "target_service_group_name": "core",
      "target_service_name": "mqtt",
      "target_port": 1883,
      "access": 1,
      "auth_service_group_name": "core",
      "auth_services": [
        "mqttbeats"
      ]
    },
    {
      "name": "allow access to mqtt from device groups",
      "target_service_group_name": "core",
      "target_service_name": "mqtt",
      "target_port": 1883,
      "access": 3,
      "device_group_names": [
        "raspberry"
      ]
    }
  ],
```

The last thing we need to do is specify the list of parameters that we will configure when we deploy the application. Which, in our case, consists only of one parameter: the device group name.

As you can see, the device group name written in the last rule is `raspberry`. This will be the default name for the device group, but we need to be able to specify another one if we want to. So, let's include the parameter section:

```javascript
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

* a simple `description`.
* a `path`: this tells us where to find the variable in the descriptor. The variable must exist beforehand so we can substitute its value with a new one. In this case, this variable is in the fifth rule \(starting from 0\), and has the name `DEVICE_GROUP_NAME`.
* a `type`, to be chosen between boolean \(0\), integer \(1\), double \(2\), enum \(3\), string \(4\) or password \(5\). In this case, it's a `string`.
* a `category`, which is an indication of this parameter being needed for a basic configuration \(0\) or an advanced one \(1\).
* a flag telling us if the parameter is `required` or optional. In this case, it's optional.

And that's it! You have finished your application descriptor and can now deploy an instance of your application in Nalej. If you have trouble with this part, there is a step-by-step tutorial [here](appdeployment_wclusters.md), and you can find more information [here](../applications/applications-1.md) if you have further questions.

## Sending telemetry data

Now, you have a registered device AND an application to use it with. How do we connect the device to the application we want to use? Well, we use **labels**.

Our application descriptor starts with something like this:

```javascript
{
   "name": "Thermometer application",
   "labels": {
       "app": "thermometer-app"
   },
   "rules": [
   {
       ...
    ...
```

The `app` parameter inside the `labels` part of the descriptor is what we need to connect to a specific app in the system.

Then, the next step is creating a data object that knows how to interact with that application. We are using the MQTT protocol, which is the only protocol the platform supports by now, so we need a NalejMqttData object in our Python file. For that object we need two parameters:

* the **topic** of the MQTT messages.
* the **function** \(as a parameter\) that will return the data to be sent to the application.

Finally, we need to send the telemetry data to the application using the **publish** method, which creates a new thread that sends telemetry data every 5 seconds, and will continue to do so until the **disconnect** method is executed.

This part of the program would look like this:

```python
from nalej.core.client import NalejClient
from nalej.messaging.mqtt.mqtt_model import NalejMqttData

# ...
# Device created
# Device registered & connected
# ...

topic = 'sensor/' + client.config.deviceId + '/temperature'
labels = {'app':'example-app'}
dataObject = NalejMqttData(topic, get_random_temp_payload)
client.publish(labels, dataObject)
```

## Disconnecting device

The publish method will be sending data in a new thread until the program disconnects. The **disconnect** method stops the communication with all the connected applications and the platform \(the log out must be processed from the platform side\), and it looks like this:

```python
from nalej.core.client import NalejClient

# ...
# Once the device has been connected and has sent all the needed data
# ...

client.disconnect()
```

So, that would be it! With this, you would have the whole system up and running. Have fun!

## Complete example files

Here you have the files you need for this example. Please read them carefully, because it's probable that you will need to modify them with your own information.

### Application descriptor

```javascript
{
  "name": "Sample thermometer application with 5 elements",
  "labels": {
    "app": "thermometer-app"
  },
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
      "name": "Allow mqttbeats to access mqtt",
      "target_service_group_name": "core",
      "target_service_name": "mqtt",
      "target_port": 1883,
      "access": 1,
      "auth_service_group_name": "core",
      "auth_services": [
        "mqttbeats"
      ]
    },
    {
      "name": "allow access to mqtt from device groups",
      "target_service_group_name": "core",
      "target_service_name": "mqtt",
      "target_port": 1883,
      "access": 3,
      "device_group_names": [
        "raspberry"
      ]
    }
  ],
  "groups": [
    {
      "name": "core",
      "services": [
        {
          "name": "kibana",
          "image": "docker.elastic.co/kibana/kibana:6.4.2",
          "specs": {
            "replicas": 1
          },
          "exposed_ports": [
            {
              "name": "kibanaport",
              "internal_port": 5601,
              "exposed_port": 5601,
              "endpoints": [
                {
                  "type": 2,
                  "path": "/"
                }
              ]
            }
          ],
          "environment_variables": {
            "ELASTICSEARCH_URL": "http://NALEJ_SERV_ELASTIC:9200"
          },
          "labels": {
            "app": "kibana"
          }
        },
        {
          "name": "elastic",
          "image": "docker.elastic.co/elasticsearch/elasticsearch:6.4.2",
          "specs": {
            "replicas": 1
          },
          "storage": [
            {
              "mount_path": "/usr/share/elasticsearch/data"
            }
          ],
          "exposed_ports": [
            {
              "name": "elasticport",
              "internal_port": 9200,
              "exposed_port": 9200
            }
          ],
          "environment_variables": {
            "ES_JAVA_OPTS": "-Xms512m -Xmx512m",
            "bootstrap.memory_lock": "true",
            "cluster.name": "elastic-cluster",
            "discovery.type": "single-node"
          },
          "labels": {
            "app": "elastic"
          }
        },
        {
          "name": "mqttbeats",
          "image": <docker_image_path>,
          "specs": {
            "replicas": 1
          },
          "configs": [
            {
              "content": <content_in_base64>,
              "mount_path": "/config/mqttbeats.yml"
            }
          ],
          "labels": {
            "app": "mqttbeats"
          }
        },
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
        "replicas": 1,
        "deployment_selectors": {
          "cloud": "azure"
        }
      }
    }
  ]
}
```

### Python file

This file gets the humidity and temperature values from the DHT22 sensor \(you have an easy installation tutorial for this sensor [here](https://www.instructables.com/id/Raspberry-Pi-Tutorial-How-to-Use-the-DHT-22/)\).

```python
import Adafruit_DHT # library to access the sensors
import logging
import time

from nalej.configuration.config_manager import NalejConfig
from nalej.core.client import NalejClient
from nalej.messaging.mqtt.mqtt_model import NalejMqttData

# Getting humidity and temperature values from the sensor.
def get_dht22_temp():
    humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 4)
    return "{0:.2f}".format(temperature)

# Formatting the values with the format we want
# to read in the application.
def get_dht22_temp_payload():
    payload = '{"value":' + str(get_dht22_temp()) + '}'
    return payload

# For logging purpuses
logging.basicConfig(level=logging.DEBUG)

# Creating the client (in this case, from a configuration
# file)
client = NalejClient.fromConfigFile()

# Loop that tries to connect with the platform
# (and manages the errors the connection may cause) 
connected = False
while not connected:
   try:
       client.connect()
       connected = True
   except:
       logging.error('Login failed. Trying again in 2 seconds.')
       time.sleep(2)

# Creating the object to be sent to the platform and 
# publishing the data every 5 seconds in another thread.
topic = 'sensor/' + client.config.deviceId + '/temperature'
labels = {'app':'thermometer-app'}
dataObject = NalejMqttData(topic, get_dht22_temp_payload)
client.publish(labels, dataObject)

# Waiting loop for this thread... until 
# - the program receives a keyboard interruption, which will
#   disconnect the client, or
# - an error happens, which will be logged.
try:
   while True:
       time.sleep(10)
except KeyboardInterrupt:
   logging.debug('Disconnecting virtual device')
   client.disconnect()
except Exception as error:
   logging.error('Virtual device: ' + str(error.args[0]))
```

### Config file

If you want to use this config file as it is used in the Python program above, remember to substitute the information here with your specific configuration info, and to save this file as _.nalej\_config_ in the _home_ folder of the current user.

Also, remember that you will need several parameters that will change depending on your organization and application, like the **organizationID**, the **deviceGroupID** and the **deviceGroupApiKey**.

```javascript
{
    "nalejPlatformDomain": "demo.nalej.tech",
    "organizationId": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "deviceGroupName": "test_group",
    "deviceGroupId": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "deviceGroupApiKey": "xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
    "deviceId": "deviceTemp001"
}
```

