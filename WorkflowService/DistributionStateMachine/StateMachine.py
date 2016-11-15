

class DistributionState(object):
    def __init__(self):
        self.is_final_state = None

    def work(self, event, context):
        raise NotImplemented("Method must be overridden in concrete class.")

    def complete(self, success, context):
        raise NotImplemented("Method must be overridden in concrete class.")

    def next_state(self, context, newState):
        context.set_state(newState)


class CreatedState(DistributionState):
    def __init__(self):
        super(CreatedState, self).__init__()
        self.is_final_state = False

    def work(self, event, context):
        print "Created initial state machine, workflow id {0}".format(context.workflow_id)
        self.next_state(context, SyndicationState)
        return True


class SyndicationState(DistributionState):
    def __init__(self):
        super(SyndicationState, self).__init__()
        self.is_final_state = False

    def work(self, event, context):
        print 'Running Syndication! for workflow {0}'.format(context.workflow_id)
        self.next_state(context, EncodeState)
        return True


class EncodeState(DistributionState):
    def __init__(self):
        super(EncodeState, self).__init__()
        self.is_final_state = False

    def work(self, event, context):
        print 'Running Encode! for workflow {0}'.format(context.workflow_id)
        self.next_state(context, CopyState)
        return True


class CopyState(DistributionState):
    def __init__(self):
        super(CopyState, self).__init__()
        self.is_final_state = False

    def work(self, event, context):
        print 'Running Copy! for workflow {0}'.format(context.workflow_id)
        self.next_state(context, CompletedState)
        return True


class SuspendState(DistributionState):
    def __init__(self):
        super(SuspendState, self).__init__()
        self.is_final_state = True

    def work(self, event, context):
        print "Can't really work in suspend state. Workflow {0}".format(context.workflow_id)

    def reset(self, context):
        print "Resetting state."
        self.next_state(context, CreatedState)


class CompletedState(DistributionState):
    def __init__(self):
        super(CompletedState, self).__init__()
        self.is_final_state = True

    def work(self, event, context):
        print "Completed State reached! Workflow %s".format(context.workflow_id)

    def complete(self, success, context):
        print "Already in final state. No-op."
