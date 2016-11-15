import unittest
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from DistributionStateMachine import StateMachine, Context

class TestStateContext(unittest.TestCase):

    def test_context_initial_state(self):
        context = Context.Context('wkfl123')
        self.assertTrue(isinstance(context._current, StateMachine.CreatedState))

    def test_context_runall(self):
        context = Context.Context("wkfl_321")
        context.run_until_final_state()
        self.assertTrue( isinstance(context._current, StateMachine.CompletedState))

    def test_context_iteration(self):
        context = Context.Context("wkfl_789")
        context.set_state(StateMachine.SyndicationState)
        self.assertTrue(isinstance(context._current, StateMachine.SyndicationState))

        context.work(None)
        self.assertTrue(isinstance(context._current, StateMachine.EncodeState))
