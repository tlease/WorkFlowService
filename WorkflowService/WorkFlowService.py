
import os
import pickle
import uuid
import json
from collections import namedtuple

import DistributionStateMachine.Context


class WorkflowService(object):
    """
    Creates and manages state machines. Receives events and forwards them
    to the correct state machine.
    """

    def __init__(self):
        self.workflows = {}  # has to hold workflow instances in mem

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for wf_id in self.workflows:
            wf = self.workflows[wf]
            wf.dump()

    def get_workflow(self, id):
        wf = self.workflows.get(id, None)
        if not wf:
            wf = load_workflow(id)
            if wf:
                self.workflows[id] = wf
        return wf

    def get_or_create_workflow(self, type='DistributionStateMachine', id=None):
        wf = self.get_workflow(id)
        if not wf:
            wf = WorkFlow(type, id)
        return wf

    def receive_event(self, json_event):
        """Some json that can be cast as event.Event type"""
        event_obj = read_event(json_event)
        wf = self.get_workflow(event_obj.id)
        wf.receive_event(event_obj)


class WorkFlow(object):
    """
    instance of a workflow. Has an ID, maitains a reference to a StateMachine context.
    """
    def __init__(self, state_machine_type, id=None, priority=10):
        self.id = id or generate_id()
        context = get_state_machine(state_machine_type)
        self._state_context = context(id)
        self._file_name = "workflows\\{0}.pickle".format(self.id)

    def dump(self):
        dump_workflow(self, self._file_name)


    def receive_event(self, event):
        """
        Forward the event to the state machine context.
        """
        print 'Workflow {0} recv event {1}'.format(self.id, event)
        self._state_context.work(event)


def read_event(json_event):
    """
    Casts the json DTP as an object Event with named properties.
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


def workflow_filename(id):
    return 'workflows\\{0}.pickle'.format(id)


def dump_workflow(obj, id):
    if not os.path.exists('workflows'):
        os.makedir('workflows')
    pickle.dump(obj, open(workflow_filename(id), 'wb'))


def load_workflow(id):
    filename = workflow_filename(id)
    if not os.path.exists(filename):
        raise Exception("File {0} not found".format(filename))
    wf = pickle.load(filename)
    return wf


def get_state_machine(type):
    return {
        "DistributionStateMachine": DistributionStateMachine.Context
    }.get(type, None)


def generate_id():
    return "{}".format(uuid.uuid1())
