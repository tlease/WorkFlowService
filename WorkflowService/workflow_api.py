
import json
from collections import namedtuple

from flask import Flask
from flask import request
from flask_restful import Api, Resource, fields, marshal

import workflow

app = Flask(__name__)
api = Api(app)
wf_manager = workflow.WorkflowManager()


class WorkflowAPI(Resource):
    def get(self, id):
        wf = wf_manager.get_workflow(id)
        if not wf:
            return {"code": 404, "message": "Workflow not found"}, 404

        return marshal(wf, workflow_fields)

    def put(self, id):
        pass

    def post(self):
        id = request["id"]
        type = request["type"] or "DistributionStateMachine"
        wf = wf_manager.get_or_create_workflow(type, id)

        return marshal(wf, workflow_fields), 201

    def delete(self, id):
        pass


class WorkflowListAPI(Resource):
    def get(self):
        wfs = wf_manager.get_all()

        if not wfs:
            return {"code": 404, "message": "Workflow not found"}, 404

        return {"tasks": [marshal(wf, workflow_fields) for wf in wfs]}

    def post(self):
        json_obj = request.get_json()
        #obj = json.loads(json_obj)

        wf_manager.add(**json_obj)

workflow_fields = {
    'id':  fields.String,
    'completed': fields.Boolean,
    'active': fields.Boolean,
    'self': fields.Url('workflows')
}


def receive_event(self, json_event):
    """Some json that can be cast as event.Event type"""
    event_obj = read_event(json_event)
    wf = self.get_workflow(event_obj.id)
    wf.receive_event(event_obj)

def read_event(json_event):
    """
    Casts the json DTO as an object Event with named properties.
    It's expected that the json contains id, type, and a payload of values useful to the
    state machine for the current state / event type

    {
      "type": "SyndicationComplete",
      "id": "12345",
      "payload": {
        "syndicated_products": 100,
        "failed_products": 5,
        "dfm_path": "\\server\shared\folder\dfm.xml",
        "encode_products": true
      }
    }

    """
    j = json.loads(json_event,
                   object_hook= lambda d: namedtuple('Event', d.keys())(*d.values()))
    return j


api.add_resource(WorkflowAPI, '/workflows/<string:id>', endpoint='workflows')
api.add_resource(WorkflowListAPI, '/workflows')


if __name__ == '__main__':
    app.run(debug=True)