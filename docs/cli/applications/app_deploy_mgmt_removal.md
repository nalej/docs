# Deploy, manage and remove apps

This section will have all the documents related to app deployment, management and removal. You will also find what you need about application descriptors: what they are, how to create one, and how to use one in the system.

Now that we know how the clusters work, it's time to start deploying applications in the system. Let's see how to do this.

!!! note
    The CLI responses are shown in text format, which can be obtained adding `--output="text"` to the user options. If you need the responses in JSON format, you can get them by adding `--output="json"` at the end of your requests, or as a user option

## Application deployment

The process of deploying an application is as follows:

![This is the process to follow when deploying an instance of an application.](../../img/app_mgmt_deployment_diagram.png)

First you need to create an application descriptor. The documentation for doing so is [over here](app_descriptors.md), but by now let's just say that it should be a JSON file with more or less this aspect:

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
            "WORDPRESS_DB_HOST": <db_host>,
            "WORDPRESS_DB_PASSWORD": <db_password>
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

This is the descriptor of a WordPress server with an associated MySQL database. Yours should look similar, depending on the services you want to deploy.

### Adding the application to the system

Let's suppose you have the application descriptor already covered, and you want to deploy your application now. As stated before, the next step of the process is adding the application to the system. That will be done with the command:

```bash
./public-api-cli app desc add 
    /pathtodescriptor
```

It returns a table like this:

```bash
DESCRIPTOR                  ID          LABELS
SARA - simple application   <desc_id>   <label:value>

NAME                  IMAGE            LABELS
[Group] application   ===
simple-mysql          <serv1_img>      <l1:v1>,<l2:v2>
simple-wordpress      <serv2_img>      <l3:v3>,<l4:v4>
```

with an application **descriptor ID** inside, which we will need for deploying an instance of this application.

### Deploying the application

Now the application is ready to be deployed! We can do this with:

```bash
./public-api-cli app inst deploy 
    [descriptor_id]
    [name-app]
```

Here, as you may have noticed, is also the moment where we name the app with a human-readable name. When this command exits, it returns a JSON with an application **instance ID**, which is what we will use to work with the deployed instance.

The response to this command will look like this:

```javascript
REQUEST        ID          STATUS
<request_id>   <inst_id>   QUEUED
```

Which contains the **request\_id** for the request we just did, the **instance\_id** of the instance we are trying to deploy, and the current **status** of the instance, which in the moment after executing the command is **QUEUED** for deployment.

If there is a required parameter that you haven't provided, the response will look like this:

```bash
{
"level":"fatal",
"err":"[FailedPrecondition] Required outbound not filled",
"time":"2020-01-22T12:35:50+01:00",
"message":"cannot deploy application"
}
```

In this example, the instance required an outbound connection that wasn't filled, so the command returned with a fatal error.

##### Deploy with connections

If you designed your descriptor with outbound network interfaces, you will be able to connect any instance created with it on deployment time to other applications that were described with inbound network interfaces. Be aware that, if any outbound interface was described as required, to describe the connections to those interfaces on deployment time is mandatory.

Using the flag `--connections` you will be able to describe the connections to other applications. The connection is defined using the **outbound network interface name** that you want to connect, the **instance id** of the target application, and the **inbound network interface name** of that application to create a point to point connection. These fields must be concatenated using the comma `,` character. If you want to define more that one connection, concatenate the definitions using the sharp `#` character as separator.

```bash
./public-api-cli app inst deploy
    <desc_id>
    <inst_name>
    --connections <outbound_iface_name>,<target_inst_id>,<target_inbound_iface_name>#...
```

To know more about connections and networking, check the Application Networking tutorial [here](appnetworking.md).

## Application management

We can interact with the application in several ways, now that it's deployed. One of the actions we can take is getting its related info, which can be done with:

```bash
./public-api-cli app inst get 
    [instance_id]
```

This will return a table with some information related to the instance we are checking:

```bash
NAME                  REPLICAS           STATUS            
[Group] application   <num_replicas>    SERVICE_RUNNING   
<service_1>           <num_replicas>    SERVICE_RUNNING
<service_2>           <num_replicas>    SERVICE_RUNNING   

ENDPOINTS
"xxxx.xxxxx.appcluster.<yourcluster>.com"

simple-"xxxx.xxxxx.appcluster.<yourcluster>.com"
```

For example, a status like:

```javascript
STATUS
SERVICE_RUNNING
```

in the `[Group] application` row \(which is the info related to the whole instance\) will tell us that the application is running correctly, and

```javascript
ENDPOINTS
"xxxx.xxxxx.appcluster.<yourcluster>.com"
```

will tell us where the instance is deployed, so we can navigate to it and start working.

In case we don't have the ID of the instance we want to access, the command:

```bash
./public-api-cli app inst list
```

will return a list of the instances deployed in the platform.

## Getting logs from the instance

Once the application is running, it's generating logs and storing them in the system. To access these logs, we can use:

```bash
./public-api-cli log search 
    --instanceID=xxxx > appLogs.json
```

This will return a \(most likely\) very long response, with the following format:

```javascript
TIMESTAMP           MSG
<msg_timestamp>     <logged_info>
```

Where each **entry** has a **timestamp** and a **msg** with the logged info related to the instance, which is completely dependant on the application that generates the log. Typically, the logged info contains the **log\_level**, which can be useful to differentiate an informative log from an error one. Please check the log message format of the application you're consulting before diving in this file.

## Application removal

### Undeploying the instance

OK, so we finished working with this instance, and don't want it to be in the system anymore. In this case, we need to undeploy it. For this, we will need its instance ID.

```bash
./public-api-cli app inst undeploy 
    [instance_id]
```

That may be all the cleanup needed if this application is something we will use again in the system, since we can deploy it again tomorrow with the same application descriptor.

This, if executed successfully, will return an acknowledgment:

```javascript
RESULT
OK
```

### Deleting the app

This last step is optional, only needed if we want to delete a specific app from the system, and doesn't need to be done every time we undeploy an instance.

!!! note
    The system won't let you delete an application while it has deployed instances of it in the system, so first we need to undeploy all the instances first and then delete the application from the system.

What if we just don't want the application to be available again? In that case, we need to delete the application from the system, undoing the `add` we executed before. This needs the descriptor ID we got as a response when we added the application to the system.

```bash
./public-api-cli app desc delete      
    [descriptor_ID]
```

This, if executed successfully, will return an acknowledgment:

```javascript
RESULT
OK
```
