import math

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

from enums.dataset_file_key_enum import DatasetFileKeyEnum
from utils.place_utils import PlaceUtils
from utils.event_category_utils import EventCategoryUtils
from services.upload_service import UploadService
from models.event import Event
from models.paginated import Paginated
from utils.event_utils import EventUtils
from utils.pagination_utils import PaginationUtils
from utils.user_utils import UserUtils

upload_service = UploadService()

class RecommendationService:
  def get_recommended_events_by_user(self, id: int, skip: int, limit: int) -> Paginated[Event]:
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

  def get_recommended_places(self, skip: int, limit: int) -> Paginated[int]:
    events_csv = upload_service.read_text_file(DatasetFileKeyEnum.EVENTS.value)

    events_df = EventUtils.from_csv_to_data_frame(events_csv)

    event_categories_csv = upload_service.read_text_file(DatasetFileKeyEnum.EVENT_CATEGORIES.value)
    event_categories_df = EventCategoryUtils.from_csv_to_data_frame(event_categories_csv)

    category_ids_grouped = event_categories_df.groupby('eventId')['categoryId'].apply(list).reset_index()

    events_df = events_df.merge(
      category_ids_grouped,
      how = 'left',
      left_on = 'id',
      right_on = 'eventId',
    )

    events_df.drop('eventId', axis=1, inplace=True)
    events_df.rename(columns = { 'categoryId': 'categoryIds' }, inplace = True)

    places_csv = upload_service.read_text_file(DatasetFileKeyEnum.PLACES.value)
    places_df = PlaceUtils.from_csv_to_data_frame(places_csv)

    merged_df = pd.merge(events_df, places_df, left_on='placeId', right_on='id', how='left')

    merged_df['percentageSold'] = merged_df['soldTicketsCount'] / merged_df['totalTicketsCount']
    
    X = merged_df[['totalTicketsCount', 'percentageSold']]
    y = merged_df['soldTicketsCount'] * 100

    X_train, X_test, y_train, y_test = train_test_split(
      X,
      y,
      test_size = 0.2,
      random_state = 42,
    )

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    places_with_predictions = pd.concat([places_df, pd.Series(predictions, name='predictedSales')], axis=1)

    sorted_places = places_with_predictions.sort_values(by='predictedSales', ascending=False)

    place_ids = []

    for index, place in sorted_places.iterrows():
      place_ids.append(place['id'])

    paginated_place_ids = PaginationUtils.paginate_list(place_ids, skip, limit)
    total_items_count = len(sorted_places)
    total_pages_count = math.ceil(total_items_count / limit)

    return Paginated(
      items = paginated_place_ids,
      total_pages_count = total_pages_count,
      total_items_count = total_items_count,
    )
