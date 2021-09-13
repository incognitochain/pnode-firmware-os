"""personal assistant sdk"""
from __future__ import print_function

#
from send import send_json

#
NOTIFY_TYPE = "personal_assistant"
NOTIFY_ACTION = "loader"

class Loader(object):
  """Helper class, send data for PA"""

  @classmethod
  def get_source(cls, source):
    """Get source"""
    return source
  #end

  @classmethod
  def build_sensor_json(cls, action, app, status, source=""):
    """Build sensor json data"""
    # Format input
    source = cls.get_source(source)

    datalv0 = {
      "action": action,
      "data": {
        "status": status
      },
      "from": app
    }

    sensor = {
      "source": source,
      "type": NOTIFY_TYPE,
      "data": datalv0,
      "protocal": ""
    }

    return sensor
  #end

  @classmethod
  def show(cls, app, source=""):
    """Notify"""
    json = cls.build_sensor_json(NOTIFY_ACTION, app, 1, source)
    send_json(json)
  #end

  @classmethod
  def hide(cls, app, source=""):
    json = cls.build_sensor_json(NOTIFY_ACTION, app, 0, source)
    send_json(json)
  #end

  def __init__(self):
    super(Loader, self).__init__()
  #end
