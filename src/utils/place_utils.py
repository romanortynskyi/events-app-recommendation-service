from io import StringIO
from typing import Dict
import pandas as pd

from utils.csv_utils import CsvUtils
from models.place import Place

class PlaceUtils:
  @staticmethod
  def from_dict(dict: Dict) -> Place:
    return Place(
      id = dict['id'],
      created_at = dict['createdAt'],
      updated_at = dict['updatedAt'],
    )
  
  @staticmethod
  def from_csv_to_data_frame(places_csv: str):
    csv_file = StringIO(places_csv)
    data_frame = pd.read_csv(csv_file)

    return data_frame

  @staticmethod
  def to_csv(event):
    return CsvUtils.to_csv(event, Place.attributes)
