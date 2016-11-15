
class Event(object):
    """
    DTO for json events back from workers to pass to state machines.
    """
    type = ""
    id = ""
    payload = ""