import math
from models.event import Event

from models.paginated import Paginated

from utils.event_utils import EventUtils
from utils.pagination_utils import PaginationUtils
from utils.user_utils import UserUtils

class RecommendationService:
  def get_recommended_events_by_user(self, id: int, skip: int, limit: int) -> Paginated[Event] :
    users_csv_file = open('users.csv', 'r')
    users_csv = users_csv_file.read()
    users_csv_file.close()

    events_csv_file = open('events.csv', 'r')
    events_csv = events_csv_file.read()
    events_csv_file.close()

    users = UserUtils.parse_csv_users(users_csv)

    condition = lambda user: user.id == id
    user = next((user for user in users if condition(user)), None)

    events_data = EventUtils.from_csv_to_data_frame(events_csv)

    filtered_data = events_data[events_data['categories'].apply(lambda x: any(category_id in x for category_id in user.categories))]

    if filtered_data.empty:
      return []
    
    filtered_events = map(lambda event_dict: EventUtils.from_dict(event_dict), filtered_data.to_dict(orient='records'))
    sorted_events = sorted(filtered_events, key=lambda event: event.start_date)
    events = PaginationUtils.paginate_list(sorted_events, skip, limit)

    total_items_count = len(sorted_events)

    total_pages_count = math.ceil(total_items_count / limit)

    return Paginated(
      items = events,
      total_pages_count = total_pages_count,
      total_items_count = total_items_count,
    )
