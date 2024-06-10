from flask import Blueprint, jsonify, request

from services.place_service import PlaceService
from utils.camel_case_utils import CamelCaseUtils
from utils.place_utils import PlaceUtils

place_bp = Blueprint('place', __name__)

place_service = PlaceService()

@place_bp.post('/')
def add_place():
  place = PlaceUtils.from_dict(request.json)

  created_place = CamelCaseUtils.to_camel_case_dict(place_service.add_place(place))

  response = jsonify(created_place)
  response.status_code = 201

  return response
