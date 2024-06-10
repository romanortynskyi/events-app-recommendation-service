import json

from utils.camel_case_utils import CamelCaseUtils


class CamelCaseEncoder(json.JSONEncoder):
  def default(self, obj):
    if hasattr(obj, '__dict__'):
      return CamelCaseUtils.camel_case_dict(obj.__dict__)
    
    return super().default(obj)