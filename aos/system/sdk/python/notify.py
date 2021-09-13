from send import send_json
product_pa_notify = ["PERSONAL_ASSISTANT","SMART_WALL"]
product_t2s = ["SMART_DESK","PERSONAL_ROBOT"]
class Notify:
    """
    To know how to notify.
    If product_type is in product_pa_notify list, we use "pa_notify", else use "t2s"
    """

    def __init__(self):
        self.notify_type = None
        self.data = {}
        
    def run(self, source, text, product_type):
        if (product_type in product_pa_notify):
            self.notify_type = "personal_assistant"
            self.data = {"data": text, "action": "notification"}
        if (product_type in product_t2s):
            self.notify_type = "t2s"
            self.data = {"text": text}
        if self.notify_type is not None:
            s = {"source": source, "type": self.notify_type, "data": self.data, "protocol": ""}
            print(s)
            send_json(s)

    def show_pa_notification (self, source, icon, title, notification_type, timeout, desc, buttons = []):
        sensor = self.build_sensor_pa_notification_json(source, icon, title, notification_type, timeout, desc, buttons)
        send_json(sensor)

    """
    Private methods
    """
    def build_sensor_pa_notification_json(self, source, icon, title, notification_type, timeout, desc, buttons = []):
        real_data = {
            "icon": icon,
            "title": title,
            "type": notification_type,
            "timeout": timeout,
            "desc": desc,
            "buttons": buttons
        }

        custom_data = {
            "action": "notification",
            "data": {
                "status": "1",
                "message": "",
                "data": real_data
            },
            "from": ""
        }
        
        sensor = {
            "source": source,
            "type": "personal_assistant",
            "data": custom_data,
            "protocal": ""
        }
        return sensor

"""
EXAMPLE FOR THE USAGE:

source = "gfUvnULP8DSroaWhQ2PvHRgcBMu2/6db3fff4-b8f7-4f83-9711-1f03d15c3828"
text = "abc"
product_type = "PERSONAL_ASSISTANT"
notify = Notify()
notify.run(source, text, product_type)
"""
