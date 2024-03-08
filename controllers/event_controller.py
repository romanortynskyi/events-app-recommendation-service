import json
from flask import Blueprint, jsonify, request

from services.event_service import EventService
from utils.camel_case_utils import CamelCaseUtils
from utils.event_utils import EventUtils

event_bp = Blueprint('event', __name__)

event_service = EventService()

convert_to_camel_case_dict = lambda event: CamelCaseUtils.to_camel_case_dict(event)

@event_bp.post('/')
def add_event():
  event = EventUtils.from_dict(request.json)

  created_event = CamelCaseUtils.to_camel_case_dict(event_service.add_event(event))

  response = jsonify(created_event)
  response.status_code = 201

  return response
