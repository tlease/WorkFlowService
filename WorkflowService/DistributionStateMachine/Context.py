import StateMachine

class Context(object):
    """
    Client facing class wrapping state machine.
    Work() and Complete() methods are passed along to the current state

    """
    def __init__(self, workflow_id=None):
        self.workflow_id = workflow_id
        self._current = StateMachine.CreatedState()
        print "Created state context. Workflow ID %s" % workflow_id
        self._current.work(None, self)  # no worker will ever work on initial state, so immediately transition it.

    def set_state(self, new_state):
        self._current = new_state()

    def get_state(self):
        return self._current

    def work(self, event):
        self._current.work(event, self)

    def run_until_final_state(self):
        while not self._current.is_final_state:
            res = self._current.work(None, self)
