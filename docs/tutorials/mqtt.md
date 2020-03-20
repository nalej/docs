# MQTT, and what we use it for

## What is MQTT?

An open industry standard (developed by OASIS), specifying a light weight publish-subscribe messaging protocol. It is perfect for large-scale Internet of Things applications and high performance mobile messaging, so it is just what we need for our system.

## What is VerneMQ?

VerneMQ is a MQTT publish/subscribe message broker which implements the OASIS industry standard MQTT protocol.

It is a well-known and respected telco-grade production software with soft real-time properties, and fulfills all our current and expected future requirements around licensing, support, performance, stability, security, extensibility and functionality.

MQTT is a protocol, and VerneMQ is the broker that deals with it. So, from now on, when we talk about MQTT (and an MQTT server, and so on), we will be talking about both of them together.

## How do we use them?

We are using a custom plugin for authentication. Its main functionality is to use [JWT tokens](https://jwt.io/) to authenticate and authorize MQTT clients that register, publish and subscribe to the broker.

Let's see a little example of an application that uses MQTT to connect a device with an application.

![App instance diagram](../img/mqtt_example_appinstance_diagram.png)

This is a simple example that has a thermometer functionality. It has a device that measures the temperature, and it sends the data to our application, which then displays it in a user-friendly manner. This example is thoroughly explained [in another tutorial](endtoendtutorial.md), and in case you want to try it yourself you only need a Raspberry Pi with a temperature sensor and a tinkering mood.

So, the application flow is as follows:

![Application flow](../img/endtoend_app_flow.png)

The device sends the temperature to the MQTT server, and there is a little Elastic service (MQTTBeat) listening on that queue so it receives every message. It then receives the data and sends it to Elastic, which then processes it and sends the result to Kibana to be displayed.

### So, where and how should we install it?

As we can see above, we need to install it at least in two places, which are the server and the device, so they can message each other. The server, in our case, will be installed in the Nalej platform (as well as the rest of the services needed to process and display the information), and the device, as explained [here](installingsdkindevice.md), must support Python and have the SDK installed.

- The server will be a Docker image of the VerneMQ broker, configured with the credentials that will be provided by the manager of the image.
- The device will have the `paho-mqtt` library, which implements versions 3.1 and 3.1.1 of the MQTT protocol.

## How can I prove that it works?

Once you have installed your system, you may want to try it out piece by piece so you know everything is working correctly. Even if you have a separate device (as in the example) that sends MQTT messages to your application, it is recommended to install what you need in a terminal, if only for checking that everything is working correctly. To do that, you will need an MQTT client, something that can subscribe to the topics you're interested in as well as send messages to the system. Entering Mosquitto.

### MosQuiTTo

MosQuiTTo  is an open source (EPL/EDL licensed) message broker that implements the MQTT protocol versions 5.0, 3.1.1 and 3.1. The Mosquitto project also provides a C library for implementing MQTT clients, and the very popular `mosquitto_pub` and `mosquitto_sub` command line MQTT clients. These two clients are what we are going to use. 

To install Mosquitto through Homebrew, you just have to execute:

```bash
brew install mosquitto
```

When Homebrew ends the installation, it shows some instructions to start the MQTT server. We don't really need those, since we already have an MQTT server running in our applicaton. The only thing we need is the two clients for the MQTT we do have.

The first thing we need is to open two terminals, and execute in one of them the client that publishes the messages and reserve the other one for the client that listens to what is published in a certain topic. 

#### Publishing a message

```bash
mosquitto_pub 
	-h 192.168.1.184 
	-m "test message"
	-t test/terminal
	-u mqtt_user
	-P mqtt_password
	-d
```

This is the main command we will need to publish any message, and it's composed by:

- `-h`, which indicates the MQTT host IP.
- `-m`, which is the payload of the message.
- `-t`, which is the topic the message will be published to.
- `-u` and `-P`, which are the MQTT server user and password, respectively.
- `-d`, which enables the debugging messages to appear, so we know what is happening.

The **MQTT host IP** is the endpoint that appears in the service information section of the deployed instance in the web interface. You can also obtain this IP through the CLI.

The **payload** of the message is the extra information we want to include. It is recommended that it has a known format, since usually the services receiving this information must process it, but it is not mandatory.

The **topic** must be known, since this is the message queue where the message will be delivered, and where the services will subscribe to read the messages. In this example, as we only want to try the system out, the only requirement we have is to have the same topic here and in the listener client.

The **user** and **password** must be known by the MQTT server. In our case, these can be specified in our application descriptor, when detailing the MQTT server part.

The **debug** feature can be very useful while in the testing phase of the development.

#### Listening to a topic

Before publishing a message, let's set up a listener, so we can make sure the server is doing what it's supposed to. The listener will be subscribed to the topic where the publisher is sending the messages.

```bash
mosquitto sub
	-h 192.168.1.184 
	-t test/#
	-v
	-d
```

This will show the messages arriving to the queue where the client is listening.

- `-h` is, again, the MQTT host IP.
- `-t` is the topic (or topics) the listener is subscribed to. In this case, the `#` at the end of the topic means that the listener is subscribed to all the topics starting with `test/`.
- `-v` is the `verbose` flag. This shows the topic the message was sent to beside the message. 
- `-d` is, again, the `debug` flag. Here, it is used to show the message flags, like the QoS or the retain flag.

Once we have these two clients running, whenever we send a message to a topic the listener is subscribed to, we should see how it is sent, and how the listener sees it.