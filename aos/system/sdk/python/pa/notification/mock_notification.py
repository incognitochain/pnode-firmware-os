"""personal assistant sdk"""
from __future__ import print_function

#
from pa.notification import Notification, NOTIFY_ACTION, REMOVE_ACTION

class MockNotification:
  """Helper class, send data for PA"""

  @staticmethod
  def notify(app, tmpl, source=""):
    """Notify"""
    json = Notification.build_sensor_json(NOTIFY_ACTION, app, tmpl, source)
    return json
  #end

  @staticmethod
  def remove(app, id, source=""):
    """Remove"""
    ids = [id] if not id is list else id
    json = Notification.build_sensor_json(REMOVE_ACTION, app, ids, source)
    return json
  #end
