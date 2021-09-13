import unittest
from maya.sdk.ailib.notification import Notification
from maya.sdk.ailib.database_access import DatabaseAccess

# in local
# from ailib.database_access import DatabaseAccess
# from ailib.notification import Notification


class DatabaseAccessTest(unittest.TestCase):

    def setUp(self):
        self.db = DatabaseAccess()

    def test_get_all_data_logging(self):
        res = self.db.get_data_logging()
        self.assertNotEquals(len(res), 0)
        # Random event
        self.assertNotEquals(res[0]['event'], '')

    def test_get_data_logging_by_event_height(self):
        res = self.db.get_data_logging('height')
        self.assertNotEquals(len(res), 0)
        self.assertEquals(res[0]['event'], 'height')

    def test_get_data_from_date(self):
        res = self.db.get_data_logging(date_from='2030-01-22')
        self.assertEquals(len(res), 0)
        res = self.db.get_data_logging(date_from='2017-01-22')
        self.assertNotEquals(len(res), 0)


    def test_get_all_product(self):
        res = self.db.get_product_info()
        self.assertNotEquals(len(res), 0)

        # Random product
        self.assertNotEquals(res[0]['product_id'], '')

    def test_get_a_product_by_product_id(self):
        res = self.db.get_product_info('cc7fe4d7-2ea6-44c9-aaa5-d10ad99f1e83')
        self.assertEquals(len(res), 1)
        # Random product
        self.assertEquals(res[0]['product_id'], 'cc7fe4d7-2ea6-44c9-aaa5-d10ad99f1e83')

    def test_get_all_user(self):
        res = self.db.get_user_info()
        self.assertNotEquals(len(res), 0)

        # Random user
        self.assertNotEquals(res[0]['email'], '')

    def test_get_a_user_by_id(self):
        res = self.db.get_user_info(1)
        self.assertEquals(len(res), 1)
        self.assertEquals(res[0]['email'], 'glassyteam1@gmail.com')

    def tearDown(self):
        pass


class SendNotificationTest(unittest.TestCase):

    def setUp(self):
        pass

    def test_send_notification(self):
        value = Notification.send_notify("cc7fe4d7-2ea6-44c9-aaa5-d10ad99f1e83", "hello", "trongdth", {'metadata': {'aaa': 'aaa'}})
        self.assertNotEquals(value[0]['success'], 0)

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()
