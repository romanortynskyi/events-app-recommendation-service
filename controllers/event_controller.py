import json
from flask import Blueprint, request

from services.event_service import EventService
from utils.camel_case_utils import CamelCaseUtils
from utils.event_utils import EventUtils

event_bp = Blueprint('event', __name__)

event_service = EventService()

convert_to_camel_case_dict = lambda event: CamelCaseUtils.to_camel_case_dict(event)

@event_bp.post('/')
def add_event():
  event = EventUtils.from_dict(request.json)

  return CamelCaseUtils.to_camel_case_dict(event_service.add_event(event))
