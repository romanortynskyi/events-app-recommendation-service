from flask import Blueprint, request

from services.category_service import CategoryService
from utils.camel_case_utils import CamelCaseUtils
from utils.category_utils import CategoryUtils

category_bp = Blueprint('category', __name__)

category_service = CategoryService()

convert_to_camel_case_dict = lambda event: CamelCaseUtils.to_camel_case_dict(event)

@category_bp.post('/')
def add_category():
  category = CategoryUtils.from_dict(request.json)

  return CamelCaseUtils.to_camel_case_dict(category_service.add_category(category))
