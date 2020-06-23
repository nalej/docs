# Installing Nalej SDK in a device

## Getting ready

For this tutorial's purposes, we're going to assume that you already have a device group declared in your application, and an actual device you want to transform into a Nalej device. We're also assuming that this device has a running operating system with a Python interpreter.

In order to be able to use the Nalej Python SDK, your device needs **Python 3.7** and **PIP 3** \(version 18.1 or higher\). It also needs the following libraries:

* requests \(which allows you to send HTTP/1.1 requests in the easiest way possible\).
* pathlib \(which takes care of formatting path strings in the most appropriate format\).
* paho-mqtt \(which implements versions 3.1 and 3.1.1 of the MQTT protocol\).

## Installing the SDK

Now, to install the SDK you first need to download the source code from the GitHub repository \([here](https://github.com/nalej/nalej-iot-device-sdk-python>)\). After doing that, once in the SDK folder, there are two ways of installing the SDK, which are:

```text
python3 setup.py install
```

Or:

```text
pip3 install -e .
```

## Device registration and platform log-in

We have already installed the SDK, and now it's time to register our device and get it in the system. For this, we will need to write a very short Python program with some configuration information and commands.

To register the device, we need the following information:

* the Nalej **platform domain**. This parameter is the platform domain where we log in as users. If the login address is `login.example.nalej.com`, the platform domain would be `example.nalej.com`.
* the **organization\_id**. This parameter can be obtained through the CLI with the command `./public-api-cli org info`, or through the web interface.
* the **device\_group\_name**. This parameter can be already defined or, if it's the first device of its group, we can choose a name now and include it later in the descriptor when we deploy the application.
* the **device\_group\_id**. This parameter can be obtained through the CLI with the command `./public-api-cli devicegroup list`, where all the device group IDs in the system will appear.
* the **device\_group\_api\_key**.This parameter can be obtained through the CLI with the command `./public-api-cli devicegroup list`, or through the web interface.
* the **device\_id**. This parameter is chosen by the user.

The device will be a client of the platform. In the SDK this is modeled as a NalejClient object. This object needs the configuration information stored somewhere so it can register the device, and this "somewhere" is a NalejConfig object.

We can create a NalejClient object that can be instantiated and register our device following one of these two ways: we can create a NalejConfig object, or we can create a JSON file with the information and then obtain it from there. Let's see the two options:

#### Creating a NalejConfig object

To do this, our Python file would look like this:

```python
from nalej.configuration.config_manager import NalejConfig
from nalej.core.client import NalejClient

# we include the configuraton information that we have
# gathered previously (mainly by asking the Nalej admin).
nalejPlatformDomain='demo.nalej.tech'
organizationId='xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
deviceGroupName='test_group'
deviceGroupId='xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
deviceGroupApiKey='xxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
deviceId='deviceTemp001'

# we then create the NalejConfig object with all this
# information
config = NalejConfig(nalejPlatformDomain, organizationId, deviceGroupName, deviceGroupId, deviceGroupApiKey, deviceId)

# finally, we instantiate the NalejClient object with the
# configuration as a parameter
client = NalejClient(config)
```

#### Using a local configuration file

The SDK contemplates the possibility that, instead of each parameter, the Nalej administrator gives you a configuration file. The file will look like this:

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

In this case, the method to create the object will be a bit different, and you will need to include the configuration file path. If this method doesn't have a path, it will look for a file called _.nalej\_config_ in the _home_ folder of the current user.

So, assuming the file is called _.nalej\_config_ and it's located in the _home_ folder of the current user, your Python file will look like this:

```python
from nalej.core.client import NalejClient

# config in /Users/username/.nalej_config
client = NalejClient.fromConfigFile()

# config somewhere else
# client = NalejClient.fromConfigFile(/path/to/config/file)
```

### Registering process

After getting a NalejClient object, to register the device and log in the platform, we need to add the following to our Python program:

```python
client.connect()
```

What happens when the device tries to connect to the platform with this command?

First, it checks if it's already registered in the platform.

If it's not registered, it tries to register. When the registration ends successfully, there's a file \(the **device API key**\) that gets stored in a local file. The path of this file is defined in a parameter of the NalejConfig object called **deviceApiKeyPath**, but if it's not, it will be stored in a file called _deviceID.key_ in the _home_ folder of the current user.

If/when the device is registered, the SDK tries to log it in the platform. For this, it needs the **device API key** and the **organization ID**.

If the login is successful, the platform will return a valid JWT token, and now the device can interact with the platform using that token.

