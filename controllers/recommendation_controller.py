from flask import Blueprint, request

from services.recommendation_service import RecommendationService
from utils.camel_case_utils import CamelCaseUtils

recommendation_bp = Blueprint('recommendation', __name__)

recommendation_service = RecommendationService()

convert_to_camel_case_dict = lambda event: CamelCaseUtils.to_camel_case_dict(event)

@recommendation_bp.get('/')
def get_recommentations():
  raw_user_id = request.args['userId']
  raw_skip = request.args['skip']
  raw_limit = request.args['limit']

  if raw_user_id.isnumeric and raw_skip.isnumeric() and raw_limit.isnumeric():
    user_id = int(raw_user_id)
    skip = int(raw_skip)
    limit = int(raw_limit)

    paginated_events = recommendation_service.get_recommended_events_by_user(user_id, skip, limit)
    
    events = list(map(convert_to_camel_case_dict, paginated_events.items))

    return {
      'items': events,
      'totalPagesCount': paginated_events.total_pages_count,
      'totalItemsCount': paginated_events.total_items_count,
    }
