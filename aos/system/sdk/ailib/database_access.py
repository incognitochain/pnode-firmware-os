import os
import json
import mysql.connector
import pytz
from dateutil import parser
from mysql.connector import errorcode
from hashlib import md5
from firebase_util import FirebaseUtil

config = {
    'user': os.environ.get('AI_TEAM_SQL_USER', 'admindev'),
    'password': os.environ.get('AI_TEAM_SQL_PASSWORD', 'admin123'),
    'host': os.environ.get('AI_TEAM_SQL_HOST', '35.203.177.3'),
    'database': os.environ.get('AI_TEAM_SQL_DB_NAME', 'robotbase'),
}


class Singleton(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance


class DatabaseAccess:
    def __init__(self):
        self._connect()
        return

    def _connect(self):
        try:
            self.connection = mysql.connector.connect(**config)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                raise Exception("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                raise Exception("Database does not exist")
            else:
                raise Exception(err)

    def _get_cursor(self):
        try:
            self.connection.ping()
        except:
            self._connect()
        return self.connection.cursor()

    def get_rows(self, query):
        cursor = self._get_cursor()
        cursor.execute(query)
        rows = [dict((cursor.description[i][0], value) for i, value in enumerate(row)) for row in cursor.fetchall()]
        self.connection.commit()
        cursor.close()
        return rows

    def get_rows_without_desc(self, query):
        cursor = self._get_cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        self.connection.commit()
        cursor.close()
        return rows

    def add_rows(self, query, params):
        cursor = self._get_cursor()
        cursor.execute(query, params)
        self.connection.commit()
        cursor.close()
        return True

    def add_data_logging(self, user_id=None, app_id=None, jdoc=None):
        jdoc = json.dumps(jdoc)
        sql = ''' INSERT INTO data_logging (user_id, app_id, jdoc) VALUES (%s, %s, %s)'''
        return self.add_rows(sql, (user_id, app_id, jdoc))

    def get_data_logging(self, event=None, app_id=None, user_id=None, date_from=None):
        sql_extend = ''
        if app_id:
            sql_extend += ' AND app_id = %s ' % app_id
        if user_id:
            sql_extend += ' AND user_id = %s ' % user_id
        if event:
            sql_extend += ' AND event = "%s" ' % event
        if date_from:
            sql_extend += ' AND DATE(date) >= "%s" ' % date_from

        if sql_extend:
            sql = 'select *, NULL as updated, NULL as jdoc from data_logging WHERE TRUE AND product_id IS NOT NULL %s' % sql_extend
        else:
            sql = 'select *, NULL as updated, NULL as jdoc from data_logging WHERE product_id IS NOT NULL'
        return self.get_rows(sql)

    def get_product_info(self, product_id=None, user_id=None, user_email=None):
        # Get user_id
        if user_email:
            user = self.get_rows('SELECT * FROM users WHERE email = "%s"' % user_email)
            if not user:
                return []
            user_id = user[0]['id']

        sql = 'SELECT *, NULL AS data FROM product_id WHERE TRUE %s'
        sql_extend = ''
        if product_id:
            sql_extend += ' AND product_id = "%s"' % product_id
        if user_id:
            sql_extend += ' AND user_id = "%s"' % user_id
        return self.get_rows(sql % sql_extend)

    def get_user_info(self, user_id=None):
        if user_id:
            sql = 'SELECT *, NULL AS password FROM users WHERE id = %s' % user_id
        else:
            sql = 'SELECT *, NULL AS password FROM users'
        return self.get_rows(sql)

    def get_event_from_date(self, event=None, user_id=None, date_from=None):
        sql_extend = ''
        if event:
            sql_extend += ' AND event = "%s" ' % event
        if user_id:
            sql_extend += ' AND user_id = "%s" ' % user_id
        if date_from:
            sql_extend += ' AND FROM_UNIXTIME(`time`/1000) >= "%s" ' % date_from

        if sql_extend:
            sql = 'select *, NULL as updated, NULL as jdoc from data_logging WHERE TRUE %s' % sql_extend
        else:
            sql = 'select *, NULL as updated, NULL as jdoc from data_logging'
        return self.get_rows(sql)

    def get_list_task_by_product_id(self, product_id=None, is_suggested=None):
        temp = ''
        if is_suggested:
            if is_suggested == 'true':
                temp = 'AND gr_value.is_suggested = 1'
            else:
                temp = 'AND gr_value.is_suggested = 0'
        sql = '''
        SELECT task.id as task_id,
        `action`.`name` as `action`,
        devapps.`name` as app,
        gr_value.id as group_variable_value_id,
        task_value.id as variable_value_id, task_value.`value` as variable_value_value,
        task_value.endpoint_value as variable_value_endpoint,
        variable.`name` as variable_value_name
        FROM product_id p
          LEFT JOIN user_apps ua ON p.id = ua.product_id
          LEFT JOIN devapps ON ua.devapp_id = devapps.id
          LEFT JOIN task_user_app task_ua ON ua.id = task_ua.user_app_id
          LEFT JOIN task ON task_ua.task_id = task.id
          LEFT JOIN group_task_variable_value gr_value ON gr_value.task_id = task.id
          LEFT JOIN task_variable_value task_value ON gr_value.id = task_value.group_task_variable_value_id
          LEFT JOIN action ON task.action_id = action.id
          LEFT JOIN variable ON action.id = variable.action_id
        WHERE task.id IS NOT NULL AND p.product_id = '{product_id}' {sql_extend}
        AND variable.action_id IS NULL
        UNION
        SELECT task.id as task_id,
        action.name as `action`,
        devapps.name as app,
        gr_value.id as group_variable_value_id,
        task_value.id as variable_value_id, task_value.`value` as variable_value_value,
        task_value.endpoint_value as variable_value_endpoint,
        variable.`name` as variable_value_name
        FROM product_id p
          LEFT JOIN user_apps ua ON p.id = ua.product_id
          LEFT JOIN devapps ON ua.devapp_id = devapps.id
          LEFT JOIN task_user_app task_ua ON ua.id = task_ua.user_app_id
          LEFT JOIN task ON task_ua.task_id = task.id
          INNER JOIN group_task_variable_value gr_value ON gr_value.task_id = task.id
          LEFT JOIN task_variable_value task_value ON gr_value.id = task_value.group_task_variable_value_id
          LEFT JOIN variable ON task_value.variable_id = variable.id
          LEFT JOIN action ON variable.action_id = action.id
        WHERE p.product_id = '{product_id}' {sql_extend} ;
        '''.format(product_id=product_id, sql_extend=temp)
        return self.get_rows(sql)

    def get_last_updated_task_by_product_id(self, product_id=None):
        sql = '''
            SELECT task.id as task_id, task.updated_at
            FROM product_id p
              LEFT JOIN user_apps ua ON p.id = ua.product_id
              LEFT JOIN devapps ON ua.devapp_id = devapps.id
              LEFT JOIN task_user_app task_ua ON ua.id = task_ua.user_app_id
              LEFT JOIN task ON task_ua.task_id = task.id
              LEFT JOIN group_task_variable_value gr_value ON gr_value.task_id = task.id
              LEFT JOIN task_variable_value task_value ON gr_value.id = task_value.group_task_variable_value_id
              LEFT JOIN action ON task.action_id = action.id
              LEFT JOIN variable ON action.id = variable.action_id
            WHERE task.id IS NOT NULL AND p.product_id = '{product_id}'
            AND variable.action_id IS NULL
            UNION
            SELECT task.id as task_id, task.updated_at
            FROM product_id p
              LEFT JOIN user_apps ua ON p.id = ua.product_id
              LEFT JOIN devapps ON ua.devapp_id = devapps.id
              LEFT JOIN task_user_app task_ua ON ua.id = task_ua.user_app_id
              LEFT JOIN task ON task_ua.task_id = task.id
              INNER JOIN group_task_variable_value gr_value ON gr_value.task_id = task.id
              LEFT JOIN task_variable_value task_value ON gr_value.id = task_value.group_task_variable_value_id
              LEFT JOIN variable ON task_value.variable_id = variable.id
              LEFT JOIN action ON variable.action_id = action.id
            WHERE p.product_id = '{product_id}'
            ORDER BY updated_at DESC LIMIT 1;
            '''.format(product_id=product_id)
        return self.get_rows(sql)

    def get_list_user_product_active(self, ):
        sql = '''
            SELECT * FROM product_id p
            LEFT JOIN users u ON p.user_id = u.id
            WHERE p.is_checkin = 1
        '''
        return self.get_rows(sql)

    def get_channel_firebase(self, product_id):
        sql = '''
        SELECT users.id FROM users
        LEFT JOIN product_id ON users.id = product_id.user_id
        WHERE product_id = '%s';
        ''' % product_id
        res = self.get_rows(sql)
        if not res:
            raise Exception("Product id not found")
        res = res[0]
        m = md5()
        m.update(str(res['id']) + "_" + 'autonomous123')
        user_hash = m.hexdigest()

        # Thu tao firebase
        try:
            FirebaseUtil.create_username_password(product_id + '@autonomous.ai', user_hash)
        except Exception as err:
            pass

        # firebase_id = FirebaseUtil.get_firebase_id(product_id, user_hash)
        # source = "%s/%s" % (firebase_id, product_id)
        return product_id + '@autonomous.ai', user_hash

    def get_source_firebase(self, product_id):
        sql = '''
        SELECT users.id FROM users
        LEFT JOIN product_id ON users.id = product_id.user_id
        WHERE product_id = '%s';
        ''' % product_id
        res = self.get_rows(sql)
        if not res:
            raise Exception("Product id not found")
        res = res[0]
        m = md5()
        m.update(str(res['id']) + "_" + 'autonomous123')
        user_hash = m.hexdigest()

        # Thu tao firebase
        try:
            FirebaseUtil.create_username_password(product_id + '@autonomous.ai', user_hash)
        except Exception as err:
            pass

        firebase_id = FirebaseUtil.get_firebase_id(product_id, user_hash)
        return "%s/%s" % (firebase_id, product_id)

    def notify_product(self, product_id, data=None):
        if data is None:
            with open('send_notify.json') as f:
                data = json.load(f)
        username, password = self.get_channel_firebase(product_id)
        FirebaseUtil.auth(username=username, password=password, platform=None,
                          product_id=product_id, params=data)

    def get_list_user_has_log(self, date_from=None):
        sql = '''
            SELECT DISTINCT users.* FROM data_logging
            LEFT JOIN users ON data_logging.user_id = users.id
            WHERE FROM_UNIXTIME(`time`/1000) >= '%s'
        ''' % date_from
        return self.get_rows(sql)

    def get_list_user_active(self, user_active_days=14):

        product_id_query = '''
            SELECT
                *
            FROM
                product_id
            WHERE
                is_checkin = 1
                    AND address_lat <> 0
                    AND address_long <> 0
            UNION ALL SELECT
                *
            FROM
                product_id
            WHERE
                id IN (SELECT
                        id
                    FROM
                        (SELECT
                            MAX(id) AS id, SUM(is_checkin) AS x
                        FROM
                            product_id
                        WHERE address_lat <> 0
                                AND address_long <> 0
                        GROUP BY user_id
                        HAVING x = 0) a)
        '''
        sql = '''
            SELECT
                a.id AS user_id,
                b.id AS pid,
                b.product_id,
                b.address,
                b.address_lat,
                b.address_long,
                b.timezone,
                c.time,
                b.is_checkin
            FROM
                users a
                    INNER JOIN
                (%(product_id_query)s) b ON a.id = b.user_id
                    INNER JOIN
                (SELECT
                    *
                FROM
                    data_logging
                WHERE
                    id IN (SELECT
                            MAX(id)
                        FROM
                            data_logging
                        GROUP BY user_id)) c ON a.id = c.user_id
            WHERE
                time IS NOT NULL
                    AND FROM_UNIXTIME(time / 1000) >= (NOW() - INTERVAL %(user_active_days)d DAY)
            GROUP BY a.id
        ''' % {
            "product_id_query": product_id_query,
            "user_active_days": user_active_days
        }

        return self.get_rows(sql)

    def get_delivery_logs_of_active_users(self, user_active_days=14, log_from_microseconds=60 * 60 * 24 * 1000000):
        active_users = self.get_list_user_active(user_active_days=user_active_days)
        sql = '''
            SELECT
                *
            FROM
                data_logging
            WHERE
                FROM_UNIXTIME(time / 1000) >= (NOW() - INTERVAL %d MICROSECOND)
                    AND JSON_EXTRACT(jdoc, '$.app') = 'delivery'
                    AND user_id IN (%s)
        ''' % (log_from_microseconds, ",".join([str(row['user_id']) for row in active_users]))
        return self.get_rows(sql)

    def __parse_item_schedule_time(self, schedules):
        item_schedules = []
        for schedule in schedules:
            for time in schedule.get("times"):
                time["from"] = parser.parse(time["from"]).isoformat()
                time["to"] = parser.parse(time["to"]).isoformat()
                item_schedules.append(time)
        return item_schedules

    def __parse_merchant_schedule_time(self, schedule):
        item_schedules = []
        for day, time in schedule.get("delivery").iteritems():
            if time["times_open"]:
                timex = {
                    "from": parser.parse(time["times_open"][0]["start"]).isoformat(),
                    "to": parser.parse(time["times_open"][0]["end"]).isoformat(),
                    "day": day.title()
                }
                item_schedules.append(timex)
        return item_schedules

    def __convert_item_time_to_user_time(self, times, timezone):
        for i, schedule in enumerate(times):
            times[i]["from"] = parser.parse(times[i]["from"]).astimezone(tz=pytz.timezone(timezone)).isoformat()
            times[i]["to"] = parser.parse(times[i]["to"]).astimezone(tz=pytz.timezone(timezone)).isoformat()
        return times

    def get_history_delivery_items_of_active_users(self, user_active_days=14, is_suggested=False):
        active_users = self.get_list_user_active(user_active_days=user_active_days)
        user_ids = [str(user["user_id"]) for user in active_users]
        product_id_query = '''
            SELECT
                product_id
            FROM
                product_id
            WHERE
                is_checkin = 1 AND user_id IN (%(user_ids)s)
                    AND address_lat <> 0
                    AND address_long <> 0
            UNION ALL SELECT
                product_id
            FROM
                product_id
            WHERE
                id IN (SELECT
                        id
                    FROM
                        (SELECT
                            MAX(id) AS id, SUM(is_checkin) AS x
                        FROM
                            product_id
                        WHERE
                            user_id IN (%(user_ids)s) AND address_lat <> 0
                                AND address_long <> 0
                        GROUP BY user_id
                        HAVING x = 0) a)
        ''' % {"user_ids": ",".join(user_ids)}

        product_ids = [row["product_id"] for row in self.get_rows(product_id_query)]

        temp = ''
        if is_suggested is not None:
            if is_suggested:
                temp = 'AND gr_value.is_suggested = 1'
            else:
                temp = 'AND gr_value.is_suggested = 0'

        sql = '''
        SELECT task.id as task_id,
        `action`.`name` as `action`,
        devapps.`name` as app,
        gr_value.id as group_variable_value_id,
        task_value.id as variable_value_id, task_value.`value` as variable_value_value,
        task_value.endpoint_value as variable_value_endpoint,
        variable.`name` as variable_value_name,
        p.id AS pid,
        p.user_id AS user_id,
        p.address AS address,
        p.address_lat AS address_lat,
        p.address_long AS address_long,
        p.timezone AS timezone,
        p.product_id as product_id,
        gr_value.is_suggested as is_suggested
        FROM product_id p
          LEFT JOIN user_apps ua ON p.id = ua.product_id
          LEFT JOIN devapps ON ua.devapp_id = devapps.id
          LEFT JOIN task_user_app task_ua ON ua.id = task_ua.user_app_id
          LEFT JOIN task ON task_ua.task_id = task.id
          LEFT JOIN group_task_variable_value gr_value ON gr_value.task_id = task.id
          LEFT JOIN task_variable_value task_value ON gr_value.id = task_value.group_task_variable_value_id
          LEFT JOIN action ON task.action_id = action.id
          LEFT JOIN variable ON action.id = variable.action_id
        WHERE task.id IS NOT NULL AND devapps.name = 'delivery' AND p.product_id IN ('{product_id}') {sql_extend}
        AND variable.action_id IS NULL
        UNION
        SELECT task.id as task_id,
        action.name as `action`,
        devapps.name as app,
        gr_value.id as group_variable_value_id,
        task_value.id as variable_value_id, task_value.`value` as variable_value_value,
        task_value.endpoint_value as variable_value_endpoint,
        variable.`name` as variable_value_name,
        p.id AS pid,
        p.user_id AS user_id,
        p.address AS address,
        p.address_lat AS address_lat,
        p.address_long AS address_long,
        p.timezone AS timezone,
        p.product_id as product_id,
        gr_value.is_suggested as is_suggested
        FROM product_id p
          LEFT JOIN user_apps ua ON p.id = ua.product_id
          LEFT JOIN devapps ON ua.devapp_id = devapps.id
          LEFT JOIN task_user_app task_ua ON ua.id = task_ua.user_app_id
          LEFT JOIN task ON task_ua.task_id = task.id
          INNER JOIN group_task_variable_value gr_value ON gr_value.task_id = task.id
          LEFT JOIN task_variable_value task_value ON gr_value.id = task_value.group_task_variable_value_id
          LEFT JOIN variable ON task_value.variable_id = variable.id
          LEFT JOIN action ON variable.action_id = action.id
        WHERE devapps.name = 'delivery' AND p.product_id IN ('{product_id}') {sql_extend} ;
        '''.format(product_id="','".join(product_ids), sql_extend=temp)

        rows = self.get_rows(sql)

        history_data = {}

        for row in rows:
            user_id = row["user_id"]
            address = row["address"]
            latitude = row["address_lat"]
            longitude = row["address_long"]
            timezone = row["timezone"]
            pid = row["pid"]
            product_id = row["product_id"]
            variable_value_endpoint = json.loads(str(row["variable_value_endpoint"]))
            variable_id = row["group_variable_value_id"]
            item = variable_value_endpoint.get("item")
            restaurant = variable_value_endpoint.get("restaurant")
            item_id = item.get("value")
            item_name = item.get("display")
            item_description = item.get("description")
            item_price = item.get("price", 0)
            restaurant_id = restaurant.get("value")
            restaurant_rating = restaurant.get("rating", 0)
            is_suggested = row["is_suggested"]

            item_data = {
                "merchant_id": restaurant_id,
                "merchant_rating": restaurant_rating,
                "item_id": item_id,
                "name": item_name,
                "description": item_description,
                "price": item_price,
                "var_id": variable_id,
                "is_suggested": is_suggested
            }

            if str(user_id) in history_data:
                history_data[str(user_id)]["items"].append(item_data)
            else:
                history_data[str(user_id)] = {
                    "user": {
                        "address": address,
                        "address_lat": latitude,
                        "address_long": longitude,
                        "pid": pid,
                        "product_id": product_id,
                        "timezone": timezone,
                        "uid": user_id
                    },
                    "items": [item_data]
                }

        return history_data.values()


# print DatabaseAccess().get_event_from_date(user_id=1005)
# print DatabaseAccess().get_list_task_by_product_id(product_id='465272e0-48d9-4e26-86cf-9f010c72785c', is_suggested='true')
# print DatabaseAccess().get_event_from_date(date_from='2016/08/01')
# print (DatabaseAccess().get_list_task_by_product_id(product_id='a5f18dae-8aa8-46ec-8e07-8306ea12b0d8'))
# print json.dumps(DatabaseAccess().get_history_delivery_items_of_active_users(user_active_days=7))
# print json.dumps(DatabaseAccess().get_list_user_active(user_active_days=1))
# print json.dumps([x.get("id") for x in
#     DatabaseAccess().get_delivery_logs_of_active_users(user_active_days=1, log_from_microseconds=60 * 15 * 1000000)])
# DatabaseAccess().get_channel_firebase('a8bf77e1-8c83-4c31-a405-8b5d4d367f47')
# print DatabaseAccess().get_list_user_has_log('2017/08/01')
# print DatabaseAccess().get_last_updated_task_by_product_id('a8bf77e1-8c83-4c31-a405-8b5d4d367f47')
# print DatabaseAccess().get_history_delivery_items_of_active_users()
