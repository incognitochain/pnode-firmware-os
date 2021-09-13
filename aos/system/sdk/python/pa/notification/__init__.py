"""personal assistant sdk"""
from __future__ import print_function

#
from send import send_json

#
NOTIFY_TYPE = "personal_assistant"
NOTIFY_ACTION = "notification"
REMOVE_ACTION = "notification_remove"

class Notification(object):
  """Helper class, send data for PA"""

  @classmethod
  def get_source(cls, source):
    """Get source"""
    return source
  #end

  @classmethod
  def build_sensor_json(cls, action, app, tmpl, source=""):
    """Build sensor json data"""
    # Format input
    source = cls.get_source(source)

    datalv1 = {
      "status": 1,
      "message": "",
      "data": tmpl,
    }

    datalv0 = {
      "action": action,
      "data": datalv1,
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
  def notify(cls, app, tmpl, source=""):
    """Notify"""
    json = cls.build_sensor_json(NOTIFY_ACTION, app, tmpl, source)
    send_json(json)
  #end

  @classmethod
  def remove(cls, app, id, source=""):
    """Notify"""
    ids = [id] if not id is list else id
    json = cls.build_sensor_json(REMOVE_ACTION, app, ids, source)
    send_json(json)
  #end

  def __init__(self):
    super(Notification, self).__init__()
  #end
