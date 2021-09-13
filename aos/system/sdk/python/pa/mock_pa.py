from pa import PA, NOTIFY_TYPE, \
  NOTIFY_ACTION_TMPL_SET_TASKS, \
  NOTIFY_ACTION_TMPL_REMOVE_TASK, \
  NOTIFY_ACTION_TMPL_UPDATE_TASK, \
  NOTIFY_ACTION_TMPL_ADD_TASK, \
  NOTIFY_ACTION_TMPL_CLEAR_TASKS

class MockPA:
  @staticmethod
  def set_tasks(app, action, data, source=""):
    """Set tasks"""
    data = PA.format_data(data)
    return PA.build_sensor_json(
        NOTIFY_ACTION_TMPL_SET_TASKS, app, action, data, None, source
    )
  #end

  @staticmethod
  def add_task(app, action, data, prepend = False, source=""):
    """Add task(s)"""
    data = PA.format_data(data)
    opts = None
    if prepend == True:
      opts = {}
      opts['prepend'] = True
    return PA.build_sensor_json(
        NOTIFY_ACTION_TMPL_ADD_TASK, app, action, data, opts, source
    )
  #end

  @staticmethod
  def update_task(app, action, data, source=""):
    """Update task(s)"""
    data = PA.format_data(data)
    return PA.build_sensor_json(
        NOTIFY_ACTION_TMPL_UPDATE_TASK, app, action, data, None, source
    )
  #end

  @staticmethod
  def remove_task(app, action, data, source=""):
    """Update task"""
    data = PA.format_data(data)
    return PA.build_sensor_json(
        NOTIFY_ACTION_TMPL_REMOVE_TASK, app, action, data, None, source
    )
  #end

  @staticmethod
  def clear_tasks(app, action = None, source=""):
    """Update task"""
    return PA.build_sensor_json(
        NOTIFY_ACTION_TMPL_CLEAR_TASKS, app, action, None, None, source
    )
  #end