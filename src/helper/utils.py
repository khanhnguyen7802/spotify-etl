from datetime import datetime

def unix_to_datetime(unix_timestamp):
  """
  Convert a Unix timestamp to a datetime object.

  :param unix_timestamp: The Unix timestamp to convert.
  :return: A datetime string in the format "dd-mm-yyyy hh:mm:ss".
  """
  dt = datetime.fromtimestamp(unix_timestamp)
  return dt.strftime("%d-%m-%Y %H:%M:%S")

def beautify_datetime(str_dt):
  """
  Convert string datetime (e.g., 2025-11-08T19:40:57.229Z) to readable format.

  :param str_dt: The original datetime string from Spotify API.
  :return: A datetime string in the format "dd-mm-yyyy hh:mm:ss".
  """
  dt = datetime.fromisoformat(str_dt.replace("Z", "+00:00"))
  return dt.strftime("%d-%m-%Y %H:%M:%S")


if __name__ == '__main__':
  test1 = unix_to_datetime(1762614940.61236)
  print(type(unix_to_datetime(1762614940.61236)))
  print((test1))
  

  test2 = beautify_datetime("2025-11-08T19:40:57.229Z")
  print(test2)