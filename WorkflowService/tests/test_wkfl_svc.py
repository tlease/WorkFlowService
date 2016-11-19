import unittest
import sys
import os
import json
import shutil

from collections import namedtuple

sys.path.insert(0, os.path.abspath(".."))

import workflow_svc
from dist_state_machine.context import Context
from dist_state_machine import state_machine


class TestWorkflow(unittest.TestCase):

    def setUp(self):
        self.wkfl = workflow_svc.Workflow("DistributionStateMachine", "abc123")

    def test_id(self):
        self.assertEqual(self.wkfl.id, "abc123")

    def test_events_transition(self):
        event = namedtuple('Event', ['type', 'success', 'payload'])
        event('SyndicationCompleted', True, None)
        self.wkfl.receive_event(event)
        self.assertTrue(isinstance(
            self.wkfl._state_context._current, state_machine.EncodeState))

        event = namedtuple('Event', ['type', 'success', 'payload'])
        event('EncodeCompleted', True, None)
        self.wkfl.receive_event(event)
        self.assertTrue(isinstance(
            self.wkfl._state_context._current, state_machine.CopyState))


        event = namedtuple('Event', ['type', 'success', 'payload'])
        event('CopyCompleted', True, None)
        self.wkfl.receive_event(event)
        self.assertTrue(isinstance(
            self.wkfl._state_context._current, state_machine.CompletedState))


class TestStaticFuncs(unittest.TestCase):

    def setup(self):
        try:
            shutil.rmtree('./workflows')
            os.mkdir('./workflows')
        except:
            print "error setting up test state, continuing..."
            print sys.exc_info()

    # def tearDown(self):
    #     try:
    #         shutil.rmtree('./workflows')
    #     except:
    #         print "error in teardown of TestStaticFuncs. continuing..."
    #         print sys.exc_info()

    def test_get_state_machine(self):
        wkfl = workflow_svc.get_state_machine("DistributionStateMachine")
        self.assertEqual(type(wkfl), type(Context))

    def test_get_state_machine_neg(self):

        self.assertRaises(KeyError, workflow_svc.get_state_machine, ("not valid type",))

    def test_read_event(self):
        j = r"""{
            "key1": "val1",
            "subobj": {
                "subobjkey1": "subobjval1"
            },
            "key2": [
                {"arr1k": "arr1v"},
                {"arr2k": "arr2v"}
            ],
            "key3": 50
        }"""
        event = workflow_svc.read_event(j)
        self.assertEqual(event.key1, "val1")
        self.assertEqual(event.subobj.subobjkey1, "subobjval1")
        self.assertEqual(event.key3, 50)
        self.assertEqual(event.key2[0].arr1k, "arr1v")

    def test_dump_workflow(self):
        id = 'abc123'
        wf = workflow_svc.Workflow("DistributionStateMachine", id)
        workflow_svc.dump_workflow(wf, id)
        self.assertTrue(os.path.exists('workflows\\{0}.pickle'.format(id)))
        wf2 = workflow_svc.load_workflow(id)
        self.assertEqual(wf.id, wf2.id)