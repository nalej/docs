# The Application Diagram, explained



![Application instance main screen](../.gitbook/assets/app_instance_view.png)

The Application Diagram, in the Application Instance screen, can be daunting. Fear not, dear user, for we are here to shed some light on your doubts about it and make you an expert. Let's begin.

![I mean, who can blame you. This is scary.](../.gitbook/assets/thingsboard_diagram.png)

## Service instances

Let's begin with the service instances. Each instance has a different color depending on its status:

- Dark blue means it's *RUNNING*.
- Turquoise means it's *IN TRANSITION* (which can mean it's queued, or scheduled, or deploying...).
- Red means it has an *ERROR*.

In some cases you can find service instances that can be repeated. Remember the replicas we can specify in the [application descriptor](app_descriptors.md)? This is how those replicas are represented visually. 

As we know, we can ask for replicas of a single service or of an entire service group. Both are represented separately, since each replica is a service instance, and each instance can be running or have errors independently. Each instance, also, depending on the service group it belongs to, can have different rules and permissions. But let's get to that later.

![Text description of the application instance](../.gitbook/assets/app_instance_service_table.png)

You can (in fact, we encourage you to) use the rest of the information in the screen to decipher what we are seeing. Over the diagram, on the upper right corner of its section in the screen, there are two icons, so we can toggle between the diagram view and the text view. The text view describes every service that can be seen in the diagram with extra information (like how many replicas it has, its endpoints, its status, and more info like tags, credentials or the ID of the cluster it is deployed in).

![Text description of the application instance](../.gitbook/assets/app_instance_service_info.png)

## Rules

![Rules of the Sentiment application instance](../.gitbook/assets/app_instance_diagram_rules.png)

Do you see the little arrows pointing from one service to another? They represent the rules that apply to the services, and the relationships created between them because of that.

![Beginner-mode diagram](../.gitbook/assets/app_instance_diagram.png)

In the case of the Sentiment app, we can see that in the "sentiment" group, the "elastic" service is the target of some rules, each regarding different ports. There are four rules in total, which allow the services access to "elastic" in different ports. In the diagram, as you can see, we only see that these two services ("kibana" and "nifi") are allowed to access "elastic".

