import zmq

data = {'action': 'send_wifi_info',
        "wpa": "Autonomous",
        "ssid": "Autonomous",
        "user_hash": "b6a85f3a485dac01e59e086f5f9ec773",
        "time_zone": "Asia/Ho_Chi_Minh",
        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBodW9uZ2RlMjAwQGdtYWlsLmNvbSIsImV4cCI6MTUyMjgyOTYxOCwiaWQiOjc5Mjc2fQ.VKIiwuKETp9W9SHFRoh1K91nHGAgImoY22kEhM6RdhM",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InBodW9uZ2RlMjAwQGdtYWlsLmNvbSIsImV4cCI6MTUyMjgyOTYxOCwiaWQiOjc5Mjc2fQ.VKIiwuKETp9W9SHFRoh1K91nHGAgImoY22kEhM6RdhM",
        "address": "ho chi minh viet nam",
        "address_lat": 0.325235345,
        "address_long": 0.2423432,
        "birth": "2016-12-31",
        "city": "",
        "code": "7b9f13",
        "country": "",
        "created_at": "Mon, 05 Mar 2018 14:50:50 GMT",
        "credit": 0,
        "email": "phuongde200@gmail.com",
        "fullname": "Phuong de",
        "gender": "Male",
        "id": 661,
        "user_id": 661,
        "last_update_task": "Mon, 05 Mar 2018 14:50:50 GMT",
        "phone": "",
        "source": "phuong test",
        "verify_code": "phuong test XXX",
        "product_name": "phuong test",
        "platform": "SMART_WALL"
        }

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5004")
socket.send_json(data)
message = socket.recv()

print message