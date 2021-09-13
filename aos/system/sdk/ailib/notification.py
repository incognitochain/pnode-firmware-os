from database_access import DatabaseAccess
from pyfcm import FCMNotification

API_KEY_FIRE_BASE = "AAAA2siPpWk:APA91bGCMqRr5J24qmlyyAA8ks1XCzgdwK8_Pj-qav9QCgFTqsGcJR4X7n-XjVQOvlzPFLRJ7RFGI1WQwjzSKLq-Y9s6SbZSzIDnVvk_PURaGXw8vcvOeR2ShIOe4dBJ9rLxz-lT6ylzJd3czKbA_zxglpPf0QZBiA"


class Notification:
    def __init__(self):
        self.db = DatabaseAccess()
        self.push_service = FCMNotification(api_key=API_KEY_FIRE_BASE)

    def send_notify(self, product_id=None, message_title=None, message_body=None, data_message=None):
        if not product_id:
            raise Exception('Param `product_id` is required')

        if not message_body:
            raise Exception('Param `message_body` is required')

        res = self.db.get_rows_without_desc(
            '''
                SELECT DISTINCT gcm.gcm_code FROM gcm
                LEFT JOIN users u
                  ON gcm.user_id = u.id
                LEFT JOIN product_id p
                  ON u.id = p.user_id
                WHERE p.product_id = '%s' AND gcm_code IS NOT NULL
            ''' % product_id)

        if not res:
            raise Exception('GCM code not found to push notification')

        registration_ids = [i[0] for i in res]
        result = self.push_service.notify_multiple_devices(registration_ids=registration_ids,
                                                          message_title=message_title, message_body=message_body,
                                                          data_message=data_message)
        return result


# print Notification.send_notify('8cb46f07-7d8b-472e-8ff9-39c35c7087fe', 'message_title', 'message_body', {'meta': {'aaa': 'aaa'}})
