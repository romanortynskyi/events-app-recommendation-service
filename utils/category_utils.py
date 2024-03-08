import csv
from io import StringIO
from typing import Dict

from models.category import Category
from utils.csv_utils import CsvUtils

class CategoryUtils:
  @staticmethod
  def from_dict(dict: Dict) -> Category:
    return Category(
      id = dict['id'],
      events_count = dict['eventsCount'],
      created_at = dict['createdAt'],
      updated_at = dict['updatedAt'],
    )
  
  @staticmethod
  def to_csv(category):
    return CsvUtils.to_csv(category, Category.attributes)
