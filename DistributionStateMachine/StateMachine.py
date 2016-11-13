

class DistributionState(object):

    def __init__(self):
        self.is_final_state = None

    def work(self, workflow_id):
        raise NotImplemented("Method must be overridden in concrete class.")

    def complete(self, success, context):
        raise NotImplemented("Method must be overridden in concrete class.")

    def next_state(self, context, newState):
        context.set_state(newState)


class CreatedState(DistributionState):

    def __init__(self):
        super(CreatedState, self).__init__()
        self.is_final_state = False

    def work(self, workflow_id):
        print "Created initial state machine, workflow id %s" % workflow_id
        return True

    def complete(self, success, context):
        if success:
            self.next_state(context, SyndicationState)
        else:
            self.next_state(context, SuspendState)


class SyndicationState(DistributionState):

    def __init__(self):
        super(SyndicationState, self).__init__()
        self.is_final_state = False

    def work(self, workflow_id):
        print 'Running Syndication! for workflow %s' % workflow_id
        return True

    def complete(self, success, context):
        if success:
            self.next_state(context, EncodeState)
        else:
            self.next_state(context, SuspendState)


class EncodeState(DistributionState):

    def __init__(self):
        super(EncodeState, self).__init__()
        self.is_final_state = False

    def work(self, workflow_id):
        print 'Running Encode! for workflow %s' % workflow_id
        return True

    def complete(self, success, context):
        if success:
            self.next_state(context, CompletedState)
        else:
            self.next_state(context, SuspendState)


class SuspendState(DistributionState):

    def __init__(self):
        super(SuspendState, self).__init__()
        self.is_final_state = True

    def work(self, workflow_id):
        print "Can't really work in suspend state. Workflow %s" % workflow_id

    def reset(self, context):
        print "Resetting state."
        self.next_state(context, CreatedState)

class CompletedState(DistributionState):

    def __init__(self):
        super(CompletedState, self).__init__()
        self.is_final_state = True

    def work(self, workflow_id):
        print "Completed State reached! Workflow %s" % workflow_id

    def complete(self, success, context):
        print "Already in final state. No-op."