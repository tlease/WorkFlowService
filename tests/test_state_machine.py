import unittest
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from DistributionStateMachine import StateMachine, Context

class TestStateContext(unittest.TestCase):

    def setUp(self):
        self.context = Context.Context('wkfl123')

    def test_context_initial_state(self):
        self.assertTrue(isinstance(self.context._current, StateMachine.CreatedState))

    def test_context_runall(self):
        self.context.run_remaining_states()
        self.assertTrue( isinstance(self.context._current, StateMachine.CompletedState))