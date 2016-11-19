import state_machine

class Context(object):
    """
    Client facing class wrapping state machine.
    Work() and Complete() methods are passed along to the current state

    """
    def __init__(self, workflow_id):
        self.workflow_id = workflow_id
        self._current = state_machine.CreatedState(self.workflow_id)
        self.work(None)  # no worker will ever work on initial state, so immediately transition it.

    def set_state(self, new_state):
        self._current = new_state(self.workflow_id)

    def get_state(self):
        return self._current

    def work(self, event):
        self._current.work(event, self)

    def run_until_final_state(self):
        while not self._current.is_final_state:
            res = self._current.work(None, self)

if __name__ == '__main__':
    c = Context('abc123')
    c.run_until_final_state()