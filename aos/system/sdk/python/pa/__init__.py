"""personal assistant sdk"""
from __future__ import print_function
import os
from os.path import dirname, abspath
import sys

# Add system path prefix
CUR_DIR = dirname(abspath(__file__))
PARENT_DIR = dirname(CUR_DIR)
sys.path.insert(0, PARENT_DIR)
sys.path.insert(0, dirname(PARENT_DIR))

#
from send import send_json

#
NOTIFY_TYPE = "personal_assistant"
#
NOTIFY_ACTION_TMPL_SET_TASKS = "tmpl_set_tasks"
NOTIFY_ACTION_TMPL_REMOVE_TASK = "tmpl_remove_task"
NOTIFY_ACTION_TMPL_UPDATE_TASK = "tmpl_update_task"
NOTIFY_ACTION_TMPL_ADD_TASK = "tmpl_add_task"
NOTIFY_ACTION_TMPL_CLEAR_TASKS = "tmpl_clear_tasks"

class PA(object):
  """Helper class, send data for PA"""

  @classmethod
  def get_source(cls, source):
    """Get source"""
    # if source:
    #    source = DatabaseAccess().get_channel_firebase(source)
    return source
  #end

  @classmethod
  def format_data(cls, data, opts=None):
    """Format data"""
    if opts is None:
      opts = {}
    _type = type(data)
    data = [data] if not (_type is list) else data

    return data
  #end

  @classmethod
  def build_sensor_json(cls, notify_action, app, action, data, opts, source=""):
    """Build sensor json data"""
    # Format input
    source = cls.get_source(source)

    datalv1 = {
      "app": app,
      "action": action,
      "data": data,
    }

    if opts != None:
      datalv1["opts"] = opts

    datalv0 = {
      "action": notify_action,
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
  def set_tasks(cls, app, action, data, source=""):
    """Set tasks"""
    data = cls.format_data(data)
    json = cls.build_sensor_json(
      NOTIFY_ACTION_TMPL_SET_TASKS, app, action, data, None, source
    )
    print('set_tasks: ', json)
    send_json(json)
  #end

  @classmethod
  def add_task(cls, app, action, data, prepend = False, source=""):
    """Add task(s)"""
    data = cls.format_data(data)
    opts = {}
    opts['prepend'] = prepend
    json = cls.build_sensor_json(
      NOTIFY_ACTION_TMPL_ADD_TASK, app, action, data, opts, source
    )
    print('add_task: ', json)
    send_json(json)
  #end

  @classmethod
  def update_task(cls, app, action, data, source=""):
    """Update task(s)"""
    data = cls.format_data(data)
    json = cls.build_sensor_json(
      NOTIFY_ACTION_TMPL_UPDATE_TASK, app, action, data, None, source
    )
    print('update_task: ', json)
    send_json(json)
  #end

  @classmethod
  def remove_task(cls, app, action, data, source=""):
    """Update task"""
    data = cls.format_data(data)
    json = cls.build_sensor_json(
      NOTIFY_ACTION_TMPL_REMOVE_TASK, app, action, data, None, source
    )
    print('remove_task: ', json)
    send_json(json)
  #end

  @classmethod
  def clear_tasks(cls, app, action = None, source=""):
    """Update task"""
    json = cls.build_sensor_json(
      NOTIFY_ACTION_TMPL_CLEAR_TASKS, app, action, None, None, source
    )
    print('clear_tasks: ', json)
    send_json(json)
  #end

  def __init__(self, _from):
    super(PA, self).__init__()
  #end
