class PaginationUtils:
  @staticmethod
  def paginate_list(input_list, skip, limit):
    result = input_list[skip:skip + limit]
    
    return result
