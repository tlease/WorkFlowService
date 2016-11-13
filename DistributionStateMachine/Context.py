import StateMachine

class Context(object):
    """
    Client facing class wrapping state machine.
    Work() and Complete() methods are passed along to the current state

    """
    def __init__(self, workflow_id=None):
        self._workflow_id = workflow_id
        self._current = StateMachine.CreatedState(self._workflow_id)

    def set_state(self, new_state):
        self._current = new_state(self._workflow_id)

    def work(self):
        self._current.work()

    def run_remaining_states(self):
        while not self._current.is_final_state:
            res = self._current.work()
            self._current.complete(res, self)

class Test(object):
    def __init__(self, arg=None):
        self.arg = arg