
# WorkFlow Service

This project contains several components that, when working together
will manage arbitrary workflows.

## Workflows
A "Workflow" is a state machines defined in code, and concrete 
instances will be created and serialized and persisted by the service.

Clients of the service can retrieve an instance by an identifier, and operate on that workflow as needed by the client.

## Workers
Workers do work. The command pattern will be used to pass along parameters 
to workers, and workers will be instantiated by the workflow service 
when appropriate.

## Events
Workers create event streams as they work, and some of these events may need to be forwarded on to the workflow service to change state.
