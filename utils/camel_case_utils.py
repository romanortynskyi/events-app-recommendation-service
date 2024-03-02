from dataclasses import asdict


class CamelCaseUtils:
  @staticmethod
  def to_camel_case(snake_str):
    words = snake_str.split('_')

    return words[0] + ''.join(word.capitalize() for word in words[1:])

  @staticmethod
  def to_camel_case_dict(object):
    return { CamelCaseUtils.to_camel_case(key): value for key, value in asdict(object).items() }
