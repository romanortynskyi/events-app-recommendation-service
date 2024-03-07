import csv
from io import StringIO
from typing import Dict

from models.category import Category

class CategoryUtils:
  @staticmethod
  def from_dict(dict: Dict) -> Category:
    return Category(
      id = dict['id'],
      name = dict['name'],
      events_count = dict['eventsCount'],
      created_at = dict['createdAt'],
      updated_at = dict['updatedAt'],
    )
  
  @staticmethod
  def to_csv(category):
    attributes = Category.attributes
    values = [getattr(category, attr) for attr in attributes]

    csv_buffer = StringIO()

    csv_writer = csv.writer(csv_buffer, quoting=csv.QUOTE_NONNUMERIC)
    csv_writer.writerow(values)

    csv_line = csv_buffer.getvalue().strip()
    
    csv_buffer.close()

    return csv_line  

