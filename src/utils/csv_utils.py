import csv
from io import StringIO


class CsvUtils:
  @staticmethod
  def to_csv(object, attributes):
    values = [getattr(object, attr) for attr in attributes]

    csv_buffer = StringIO()

    csv_writer = csv.writer(csv_buffer, quoting = csv.QUOTE_NONNUMERIC)
    csv_writer.writerow(values)

    csv_line = csv_buffer.getvalue().strip()
    
    csv_buffer.close()

    return csv_line