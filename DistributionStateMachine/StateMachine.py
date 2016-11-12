

class DistributionState(object):

    def __int__(self, workflow_id=None):
        """
        :param context: Statte machine context
        :param workflow_id:
        :return:
        """
        self._workflow_id = workflow_id
        print self

    def __repr__(self):
        return "Base DistributionState: WorkflowID %s" % self._workflow_id

    def work(self):
        raise NotImplemented("Method must be overridden in concrete class.")

    def complete(self, success, context):
        raise NotImplemented("Method must be overridden in concrete class.")

    def next_state(self, context, newState):
        context.set_state(newState)


class CreatedState(DistributionState):

    def __init__(self, workflow_id=None):
        super(CreatedState, self).__init__(workflow_id)

    def work(self):
        print "Created initial state machine. Workflow %s" % self._workflow_id

    def complete(self, success, context):
        if success:
            self.next_state(context, SyndicationState)
        else:
            self.next_state(context, SuspendState)


class SyndicationState(DistributionState):

    def __init__(self, workflow_id=None):
        super(SyndicationState, self).__init__(workflow_id)

    def work(self):
        print 'Running Syndication! for workflow %s' % self._workflow_id
        return True

    def complete(self, success, context):
        if success:
            self.next_state(context, EncodeState)
        else:
            self.next_state(context, SuspendState)


class EncodeState(DistributionState):

    def __init__(self, workflow_id=None):
        super(EncodeState, self).__init__(workflow_id)

    def work(self):
        print 'Running Encode! for workflow %s' % self._workflow_id

        return True

    def complete(self, success, context):
        if success:
            self.next_state(context, CompletedState)
        else:
            self.next_state(context, SuspendState)


class SuspendState(DistributionState):

    def __init__(self, workflow_id=None):
        super(SuspendState, self).__init__(workflow_id)

    def work(self):
        print "Can't really work in suspend state. Workflow %s" % self._workflow_id

    def reset(self, context):
        print "Resetting state. workflow %s" % self._workflow_id
        self.next_state(context, CreatedState)

class CompletedState(DistributionState):

    def __init__(self, workflow_id=None):
        super(CompletedState, self).__init__(workflow_id)

    def work(self):
        print "Completed State reached! Workflow %s" % self._workflow_id

    def complete(self, success, context):
        print "Already in final state. No-op. Workflow %s" % self._workflow_id