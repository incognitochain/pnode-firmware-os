import os
import pyrebase

ACTIVE_LOCAL_CONFIG = os.getenv('ACTIVE_LOCAL_CONFIG', 'staging')


class FirebaseUtil:
    password = 'at9XafdcJ7TVHzGa'

    FIREBASE_CONFIG_staging = {
        "apiKey": "AIzaSyAtznPdWBuQFfx-kAuyKwUDNi_0L3JAYgs",
        "authDomain": "",
        "databaseURL": "https://test-rule.firebaseio.com/",
        "storageBucket": "",
        "serviceAccount": "",
        "userId": "w3a0rzxBTZQxvJZLK5rkKGTPhMh1",
        "productId": "8fed4642-2075-4b4d-a605-3478acd2b4dd"
    },

    FIREBASE_CONFIG_uat = {
      "apiKey": "AIzaSyC0owN7--MX4V9IsVdUFpo28NhQprhtClA",
      "authDomain": "",
      "databaseURL": "https://smardesk-3-staging-ute.firebaseio.com/",
      "storageBucket": "",
      "serviceAccount": "",
      "userId": "ltXAkRIUWedwtDRTQpLE6NhXilh1",
      "productId": "8fed4642-2075-4b4d-a605-3478acd2b4dd"
    },

    FIREBASE_CONFIG_production = {
        "apiKey": "AIzaSyBlkizgHz2N1HbOqmFPfxrEWIV51RPrGo8",
        "authDomain": "",
        "databaseURL": "https://aos-brain.firebaseio.com/",
        "storageBucket": "",
        "serviceAccount": "",
        "userId": "LddUIdQ20pSh4ToTZAvXI5s4WQ52",
        "productId": "8fed4642-2075-4b4d-a605-3478acd2b4dd"
    },

    FIREBASE_CONFIG = {
        'production': FIREBASE_CONFIG_production,
        'staging': FIREBASE_CONFIG_staging,
        'uat': FIREBASE_CONFIG_uat,
        'localhost': FIREBASE_CONFIG_staging,
    }

    @classmethod
    def create_username_password(cls, username=None, password=None):
        deployType = ACTIVE_LOCAL_CONFIG
        password = cls.password
        firebase = pyrebase.initialize_app(cls.FIREBASE_CONFIG[deployType][0])
        auth = firebase.auth()
        auth.create_user_with_email_and_password(username, password)

    @classmethod
    def auth(cls, username=None, password=None, platform=None, product_id=None, params=None):
        deployType = ACTIVE_LOCAL_CONFIG
        firebase = pyrebase.initialize_app(cls.FIREBASE_CONFIG[deployType][0])
        auth = firebase.auth()
        password = cls.password
        auth_data = auth.sign_in_with_email_and_password(username, password)
        print("Done sign_in_with_email_and_password")
        if auth_data and 'localId' in auth_data:
            firebase_id = auth_data['localId']
            firebase_token = auth_data['idToken']
            db = firebase.database()
            print("Done firebase.database()", firebase_id)
            params['source'] = '%s/%s_PHONE' % (firebase_id, product_id)
            db.child(firebase_id).child(product_id).push(params, firebase_token)

    @classmethod
    def get_firebase_id(cls, product_id, user_hash):
        deployType = ACTIVE_LOCAL_CONFIG
        user_hash = cls.password
        firebase = pyrebase.initialize_app(cls.FIREBASE_CONFIG[deployType][0])
        auth = firebase.auth()
        username = '%s@autonomous.ai' % product_id
        auth_data = auth.sign_in_with_email_and_password(username, user_hash)
        if auth_data and 'localId' in auth_data:
            return auth_data['localId']

    @classmethod
    def get_server_firebase_id(cls):
        deployType = ACTIVE_LOCAL_CONFIG
        firebase_config = cls.FIREBASE_CONFIG[deployType][0]
        print firebase_config
        return "%s/%s" % (firebase_config['userId'], firebase_config['productId'])
