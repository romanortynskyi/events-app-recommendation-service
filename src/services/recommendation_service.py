import math

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense

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

    places_csv = upload_service.read_text_file(DatasetFileKeyEnum.PLACES.value)
    places_df = PlaceUtils.from_csv_to_data_frame(places_csv)

    merged_data = pd.merge(
      events_df,
      places_df,
      left_on = 'placeId',
      right_on = 'id',
    )

    merged_data['ticketsSoldPercentage'] = (merged_data['soldTicketsCount'] / merged_data['totalTicketsCount']) * 100

    X = merged_data[['placeId', 'ticketsSoldPercentage']]
    y = merged_data['soldTicketsCount']

    X = pd.get_dummies(X, columns=['placeId'])

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
    )

    scaler = StandardScaler()
    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    model = Sequential()
    model.add(Dense(64, input_dim = X_train.shape[1], activation = 'relu'))
    model.add(Dense(32, activation = 'relu'))
    model.add(Dense(1))

    model.compile(optimizer = 'adam', loss = 'mean_squared_error')

    model.fit(
      X_train,
      y_train,
      epochs = 100,
      batch_size = 32,
      validation_split = 0.2,
      verbose = 0,
    )

    predictions = model.predict(X)

    merged_data['predictedSales'] = predictions

    predicted_sales_by_place = merged_data.groupby('placeId')['predictedSales'].sum().reset_index()

    predicted_sales = pd.merge(
        predicted_sales_by_place,
        places_df,
        left_on = 'placeId',
        right_on = 'id',
    )

    total_predicted_sales = predicted_sales['predictedSales'].sum()

    predicted_sales['predictedSalesPercentage'] = (predicted_sales['predictedSales'] / total_predicted_sales) * 100
    
    place_dicts = predicted_sales.to_dict('records')
    place_dicts = list(map(lambda place: {
      'id': place['id'],
      'predictedSalesPercentage': 0 if place['predictedSalesPercentage'] < 0 or place['predictedSalesPercentage'] > 100 else round(place['predictedSalesPercentage'], 2),
    }, place_dicts))

    sorted_place_dicts = sorted(
      place_dicts,
      key = lambda place: place['predictedSalesPercentage'],
      reverse = True,
    )

    paginated_items = PaginationUtils.paginate_list(sorted_place_dicts, skip, limit)
    total_items_count = len(sorted_place_dicts)
    total_pages_count = math.ceil(total_items_count / limit)

    return Paginated(
      items = paginated_items,
      total_pages_count = total_pages_count,
      total_items_count = total_items_count,
    )
