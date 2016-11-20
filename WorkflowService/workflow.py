
import os
import pickle
import uuid
import json
from collections import namedtuple

from dist_state_machine import context

WORKFLOW_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'workflows')

class WorkflowManager(object):
    """
    Creates and manages state machines. Receives events and forwards them
    to the correct state machine.
    """

    def __init__(self):
        self.workflows = {}  # has to hold workflow instances in mem
        self.get_or_create_workflow(id='abc')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for wf_id in self.workflows:
            wf = self.workflows[wf]
            wf.dump()

    def get_all(self):
        return sorted(self.workflows.values(), key=lambda x: x.id)

    def add(self, **kwargs):
        wf = Workflow('DistributionStateMachine', **kwargs)
        self.workflows[wf.id] = wf

    def get_workflow(self, id):
        """
        First check in mem, if not there check disk
        """
        wf = self.workflows.get(id, None)
        if not wf:
            wf = load_workflow(id)
            if wf:
                self.workflows[id] = wf
        return wf

    def get_or_create_workflow(self, type='DistributionStateMachine', id=None):
        wf = self.get_workflow(id)
        if not wf:
            wf = Workflow(type, id)


        if not self.workflows.get(id):
            self.workflows[id] = wf
        return wf


class Workflow(object):
    """
    instance of a workflow. Has an ID, maitains a reference to a StateMachine context.
    """
    def __init__(self, state_machine_type, id=None, priority=10, **kwargs):
        self.id = id or generate_id()
        context = get_state_machine(state_machine_type)
        self._state_context = context(id)
        self._file_name = os.path.join(WORKFLOW_FOLDER, "{0}.pickle".format(self.id))
        self.__dict__.update(kwargs)  # sets k/v attrs in class for each arbitrary kwarg

    def dump(self):
        dump_workflow(self, self._file_name)

    def receive_event(self, event):
        """
        Forward the event to the state machine context.
        """
        print 'Workflow {0} recv event {1}'.format(self.id, event)
        self._state_context.work(event)


def workflow_filename(id):
    return os.path.join(WORKFLOW_FOLDER, '{0}.pickle'.format(id))


def dump_workflow(obj, id):
    if not os.path.exists(WORKFLOW_FOLDER):
        os.mkdir(WORKFLOW_FOLDER)
    pickle.dump(obj, open(workflow_filename(id), 'wb'))


def load_workflow(id):
    filename = workflow_filename(id)
    wf = None
    if os.path.exists(filename):
        wf = pickle.load(open(filename, 'rb'))
    return wf


def get_state_machine(type):
    return {
        "DistributionStateMachine": context.Context
    }[type]


def generate_id():
    return "{}".format(uuid.uuid1())
