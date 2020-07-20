# Descriptor Creation Course

## Session 3: Parameters

The application we're going to be working with in this session is the Metric Exposer ([metric-exposer.json](desc101-metric-exposer.json)). Please download the file and work on it to complete the exercise below.

------

Some services need some environment variables to work. When this is the case, what we need to do is:

1. Declare them in the `environment_variables` section of the service.
2. Define them later in the descriptor as parameters.

In the case of Metric Exposer, we need the following information:

```json
"services": [
  {
    "name": "metricexposer",
    "image": "nalej/metrics-exposer:v1.0.0",
    "specs": {
      "replicas": 1
    },
    "labels": {
      "app": "communications"
    },
    "environment_variables": {
      "RW_URL": "",
      "RW_USERNAME": "",
      "RW_PASSWORD":  "",
      "SCRAPE_METRICS_PATH": "/metrics",
      "SCRAPE_TARGET_HOST":  "",
      "SCRAPE_CA_FILE":  "",
      "SCRAPE_CERT_FILE":  "",
      "SCRAPE_KEY_FILE":  ""
    }
  }
]
```

These variables depend on the service that you're defining and will most certainly change every time.

Once we have declared them in the body of the `services` section, we need to define them. This is done in a new section called (you guessed it) `parameters`, and each parameter follows this structure:

```json
  "parameters": [
    {
      "name": "Remote write URL",
      "description": "Target URL for the remote write configuration",
      "path": "groups.0.services.0.environment_variables.RW_URL",
      "type": 4,
      "category": 0
    },
```

This structure is thoroughly explained [in the documentation](applications/app_descriptors/#parameters). We will talk again about two of the components, for the sake of clarity.

The **path** indicates where in the descriptor the parameter is declared. This appears as :

 `group.`+number of service group

+`.services.`+number of service inside the service group

+`.`+section where the parameter is declared

+`.`+name of the parameter. 

The **type**, on the other hand, indicates what kind of content the parameter has. It can be one of the following:

0. boolean
1. integer
2. float
3. enum
4. string
5. password



## Exercise

Knowing all this, your task for this session is to complete the Metric Exposer descriptor ([metric-exposer.json](desc101-metric-exposer.json)) with the rest of the parameters.