
#TODO add flash app here

import json
from collections import namedtuple

def receive_event(self, json_event):
    """Some json that can be cast as event.Event type"""
    event_obj = read_event(json_event)
    wf = self.get_workflow(event_obj.id)
    wf.receive_event(event_obj)

def read_event(json_event):
    """
    Casts the json DTO as an object Event with named properties.
    It's expected that the json contains id, type, and a payload of values useful to the
    state machine for the current state / event type

    {
      "type": "SyndicationComplete",
      "id": "12345",
      "payload": {
        "syndicated_products": 100,
        "failed_products": 5,
        "dfm_path": "\\server\shared\folder\dfm.xml",
        "encode_products": true
      }
    }

    """
    j = json.loads(json_event,
                   object_hook= lambda d: namedtuple('Event', d.keys())(*d.values()))
    return j
