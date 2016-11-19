

class DistributionState(object):
    def __init__(self, workflow_id):
        self.workflow_id = workflow_id
        self.is_final_state = None

    def work(self, event, context):
        raise NotImplemented("Method must be overridden in concrete class.")

    def complete(self, success, context):
        raise NotImplemented("Method must be overridden in concrete class.")

    def next_state(self, context, newState):
        context.set_state(newState)


class CreatedState(DistributionState):
    def __init__(self, workflow_id):
        super(CreatedState, self).__init__(workflow_id)
        self.is_final_state = False
        print "Created initial state machine. workflow id {0}".format(self.workflow_id)

    def work(self, event, context):
        print "\tProcessing initial state. workflow id {0}".format(self.workflow_id)
        self.next_state(context, SyndicationState)
        return True


class SyndicationState(DistributionState):
    def __init__(self, workflow_id):
        super(SyndicationState, self).__init__(workflow_id)
        print 'Entered SyndicationState for workflow {0}'.format(self.workflow_id)
        self.is_final_state = False

    def work(self, event, context):
        print '\tRunning Syndication! for workflow {0}'.format(self.workflow_id)
        self.next_state(context, EncodeState)
        return True


class EncodeState(DistributionState):
    def __init__(self, workflow_id):
        super(EncodeState, self).__init__(workflow_id)
        self.is_final_state = False
        print 'Entered EncodeState for workflow {0}'.format(self.workflow_id)

    def work(self, event, context):
        print '\tRunning Encode! for workflow {0}'.format(self.workflow_id)
        self.next_state(context, CopyState)
        return True


class CopyState(DistributionState):
    def __init__(self, workflow_id):
        super(CopyState, self).__init__(workflow_id)
        self.is_final_state = False
        print 'Entered CopyState for workflow {0}'.format(self.workflow_id)

    def work(self, event, context):
        print '\tRunning Copy! for workflow {0}'.format(context.workflow_id)
        self.next_state(context, CompletedState)
        return True


class SuspendState(DistributionState):
    def __init__(self, workflow_id):
        super(SuspendState, self).__init__(workflow_id)
        self.is_final_state = True
        print 'Entered SuspendState for workflow {0}'.format(self.workflow_id)

    def work(self, event, context):
        print "\tCan't really work in suspend state. Workflow {0}".format(self.workflow_id)

    def reset(self, context):
        print "Resetting state from Suspended."
        self.next_state(context, CreatedState)


class CompletedState(DistributionState):
    def __init__(self, workflow_id):
        super(CompletedState, self).__init__(workflow_id)
        self.is_final_state = True
        print "Entered Completed State! Workflow %s".format(self.workflow_id)

    def work(self, event, context):
        print "Nothing to do, we're already completed. Workflow %s".format(self.workflow_id)

    def complete(self, success, context):
        print "Already in final state. No-op."
