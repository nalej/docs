# Persistent storage

Much like the problems with [defining ingress and routing traffic](https://www.weave.works/blog/kubernetes-faq-how-can-i-route-traffic-for-kubernetes-on-bare-metal) for bare metal, you can’t rely on the services that are available from the major cloud providers to provide persistent storage volumes for your stateful applications. On-disk files in a Kubernetes container are ephemeral, which presents some problems for non-trivial applications when running in containers. When a container crashes, `kubelet` will restart it, but the files will be lost - the container starts with a clean state.

Because of this, you need to make the data available after a pod recovers, and that can be done moving the data outside the pod so that it can exist independently. In Kubernetes, data is kept in a volume that allows the state of a service to persist across multiple pods.

## Options

### emptyDir

Kubernetes exposes multiple kinds of volumes, the most basic of which is the empty volume `emptyDir`. With this type of volume, the node stores its data to an `emptyDir` that runs from either RAM or from persistent storage like an SSD drive. This type of storage obviously runs right on the node and means that it only persists if the node is running. If the node goes down, the contents of the `emptyDir` are erased.

An `emptyDir` volume is first created when a pod is assigned to a node, and exists as long as that Pod is running on that node. When a Pod is removed from a node for any reason, the data in the `emptyDir` is deleted forever.

Note that a container crashing does NOT remove a pod from a node, so the data in an `emptyDir` volume is safe across container crashes.

### hostPath

In case the directory should not start out empty, `hostPath` can be used instead. The main difference with `emptyDir` is that the host path is mounted directly on the Pod. This means if the Pod goes down, its data will still be preserved.

## Persistent Volumes for the Nalej Platform

Due to the limitation that `hostPath` requires a mount path, the option for those kubernetes deployments/statefulsets requiring persistent volumes will be to **use `emptyDir` in case of on-premise installation**. As highlighted above, the `emptyDir` volume just lives as long as the Pod is not removed from the cluster. This drawback will be mitigated as soon as a solution for persistent storage is in place.

### Impacted Kubernetes Deployments / Statefulsets

- ``conductor.deployment.yaml``
- ``network-manager.deployment.yaml``
- ``elastic.deployment.yaml``
- ``vpnserver.deployment.yaml``
- ``dns-server.statefulset.yaml``
- ``nalej-bus.bookie.statefulset.yaml``
- ``nalej-bus-zookeeper.statefulset.yaml``
- ``scylla-statefulset.yaml``

The current method to update the YAML is using the following script. It does not need parameter inputs, and it needs to be stored in the assets folder. 

**`claim_to_emtpydirs.py`**

```yaml
#!/usr/bin/env python3

import yaml
import sys

def convert_claims_to_empty_dirs_statefulset(yaml_dict):
    try:
        spec = yaml_dict["spec"]
        template_spec = spec["template"]["spec"]
        volumes = template_spec.get("volumes", [])
        volume_claims = spec.pop("volumeClaimTemplates", [])

        for claim in volume_claims:
            claim_name = claim["metadata"]["name"]
            volumes.append({"name": claim_name, "emptyDir": {}})
                
        template_spec["volumes"] = volumes
        spec["template"]["spec"] = template_spec
        yaml_dict["spec"] = spec
    except KeyError:
        pass
    finally:
        return yaml_dict

def convert_claims_to_empty_dirs_deployment(yaml_dict):
    try:
        spec = yaml_dict["spec"]
        template_spec = spec["template"]["spec"]
        volumes = template_spec.get("volumes", [])

        for volume in volumes:
            if "persistentVolumeClaim" in volume:
                volume.pop("persistentVolumeClaim")
                emptyDir= {"emptyDir": {}}
                volume ["emptyDir"] = {}

    except KeyError:
        pass
    finally:
        return yaml_dict


def main():

    list_of_yaml=["conductor.deployment.yaml", "network-manager.deployment.yaml", "elastic.deployment.yaml", "vpnserver.deployment.yaml", "dns-server.statefulset.yaml", "nalej-bus.bookie.statefulset.yaml", "nalej-bus-zookeeper.statefulset.yaml", "scylla-statefulset.yaml"]

    for yaml_path in list_of_yaml:

        yaml_dict = {}
        with open(yaml_path, "r") as yaml_file: 
            yaml_dict = yaml.load(yaml_file)

        if "statefulset" in yaml_path:   
            converted_yaml = convert_claims_to_empty_dirs_statefulset(yaml_dict)
        elif "deployment" in yaml_path:
            converted_yaml = convert_claims_to_empty_dirs_deployment(yaml_dict)

        with open(yaml_path, "w") as yaml_file:
            yaml_contents = yaml.dump(converted_yaml, default_flow_style=False)
            yaml_file.write(yaml_contents) 


if __name__ == "__main__":
    main()

```



