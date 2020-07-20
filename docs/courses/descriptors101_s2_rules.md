# Session 2: Rules and connections

The application we're going to be working with in this session is the Pinger ([pinger.json](desc101-pinger.json)). Please download the file and work on it to complete the exercise below.

------

Some of the services that we will deploy in the Nalej platform will probably need connections to work. These connections must be regulated so that there is no unintended communication with the services, and this regulation takes place in the `rules` section of the descriptor.

Each rule has at least the following components:

- **name**: a human-readable name that ideally explains what the rule is about.
- **target_service_group_name**: the name of the service group this rule applies to.
- **target_service_name**: the name of the service this rule applies to.
- **target_port**: port of the target service that will be used for the connection.
- **access**: the kind of connection that this rule regulates.

Depending on the value in the **access** parameter, the rule will need other specific fields or not. You can find all the possibilities [in the "Rules" section of the documentation on application descriptors](applications/app_descriptors/#rules), but in this tutorial we will focus on the use case of the Pinger service.

The Pinger service will need an outbound socket to send pings, and an inbound socket to receive the response to said pings. So, first you need to create the sockets, and then you need the rules to control the connections through them.

```json
  "inbound_net_interfaces": [
    {"name": "in"}
  ],
```

Shown above is the declaration of a new socket. The section starts with `inbound_net_interface` or `outbound_net_interface`, depending on the type of socket, and then you assign a name inside. In the case of an outbound socket, you also need to clarify if it's required.

After you declare the new socket, it's time to create the rule associated with it.

```json
  "rules": [
    {
      "name": "Ping inwards",
      "target_service_group_name": "ping-group",
      "target_service_name": "ping",
      "target_port": 666,
      "access": 4,
      "inbound_net_interface": "in"
    },
```

In this case, the **access** value is **4**, which indicates an inbound connection. As there might be several inbound sockets in the same descriptor, you need to specify which one is the one used in this rule, thus linking the socket with the service that will use it

## Exercise

The exercise for this session is to complete the Pinger descriptor ([pinger.json](desc101-pinger.json)) with the information needed for an outbound socket.

