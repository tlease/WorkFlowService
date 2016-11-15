import unittest
import os
import sys

sys.path.insert(0, os.path.abspath('..'))

from dist_state_machine import state_machine, context

class TestStateContext(unittest.TestCase):

    def test_context_initial_state(self):
        _context = context.Context('wkfl123')
        self.assertTrue(isinstance(_context._current, state_machine.EncodeState))

    def test_context_runall(self):
        _context = context.Context("wkfl_321")
        _context.run_until_final_state()
        self.assertTrue( isinstance(_context._current, state_machine.CompletedState))

    def test_context_iteration(self):
        _context = context.Context("wkfl_789")
        _context.set_state(state_machine.SyndicationState)
        self.assertTrue(isinstance(_context._current, state_machine.SyndicationState))

        _context.work(None)
        self.assertTrue(isinstance(_context._current, state_machine.EncodeState))
