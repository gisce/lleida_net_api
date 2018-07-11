# -*- coding: utf-8 -*-

import logging
from io import BytesIO
import requests

click_sign_envs = {
    'prod': 'https://api.clickandsign.eu/cs/',
    # 'staging': None,
}

# API Status Codes
# See https://api.clickandsign.eu/dtd/clickandsign/v1/es/index.html#status
STATUS_CODES = {
    "200": "Success"
    "1400": "Method not allowed"
    "1401": "Invalid request"
    "1402": "Invalid content"
    "1403": "Invalid XML"
    "1404": "No data found"
    "1500": "Unknown error"
    "1501": "Timeout error"
    "1502": "Connection error"
    "1503": "Service unavailable"
    "1504": "Temporary error. Try again"
    "1505": "Already logged"
    "1506": "Not implemented yet"
    "1600": "Invalid user"
    "1601": "Insufficient credit"
    "1602": "Invalid credit"
    "1603": "Invalid id"
    "1605": "Invalid email"
    "1606": "Invalid number"
    "1700": "Invalid provider"
    "6000": "Incorrect encoding in received data"
    "6001": "Registered_langs field is not valid"
    "6002": "Lang not supported"
    "6003": "Malformed url. http:// or https:// required"
    "6009": "There are more free (not registered elements) defined that elements allowed"
    "6010": "The selected SMS type can't be registered"
    "6011": "Optional parameters in the selected SMS type are not allowed"
    "6012": "Define a recipient is only possible in Final SMS type"
    "6020": "Reminder_lapse is mandatory in Reminder SMS type"
    "6021": "Otp paramenter is mandatory in Otp SMS type"
    "6022": "At least Default_sender or Sender has to be defined"
    "6023": "Otp type is a Mandatory Registered SMS type"
    "6029": "Reminder type is the only SMS type that can be defined more than once"
    "6030": "The selected Email type can't be registered"
    "6031": "Optional parameters in the selected Email type are not allowed"
    "6032": "Define to option is only possible in Final Email type"
    "6033": "Start and Otp Email types are not allowed to define cc option"
    "6034": "Start and Otp Email types are not allowed to define bcc option"
    "6040": "Reminder_lapse is mandatory in Reminder Email type"
    "6041": "Subject field is mandatory and has to contain at least one character"
    "6042": "At least default_from_name or from_name has to be defined"
    "6043": "Otp type is a Mandatory Registered Email type"
    "6044": "File_group has to be selected in all the attachments"
    "6045": "The selected Email type doesn't allow the file_group selected in the attachment"
    "6049": "Reminder type is the only Email type that can be defined more than once"
    "6050": "Mapping signature_on_sign_required_elements can't be defined with the selected signature_type"
    "6060": "Contract_id, url and otp are reserved words in the signatories structure, so can't be defined as optional fields"
    "6061": "Some of the optional fields defined in the signatories structure don't exist in the SMS or Mail configuration"
    "6062": "File_group is mandatory"
    "6063": "The file_group selected is not valid"
    "6064": "Two or more files have the same filename with the same file_group"
    "6065": "Has to be, at least, one file with sign_on_landing"
    "6066": "Too much files"
    "6070": "Fulfil all required fields"
    "6071": "Invalid data range. Data range is to wide"
    "6099": "Invalid PDF file content"
}

class CS_API(object):

    def __init__(self, user=None, password=None, environment=None, **kwargs):
        logging.info("Initializing Lleida.net Click'n'Sign API")

        # Handle the user
        if not user:
            assert 'user' in kwargs
            user = kwargs['user']
        assert type(user) == str, "The user must be an string. Current type '{}'".format(type(user))
        self.user = user

        # Handle the password
        if not password:
            assert 'password' in kwargs
            password = kwargs['password']
        assert type(password) == str, "The user must be an string. Current type '{}'".format(type(password))
        self.password = password

        # Handle environment, default value "prod"
        self.environment = "prod"
        if not environment:
            if 'environment' in kwargs:
                assert type(kwargs['environment']) == str, "environment argument must be an string"
                assert kwargs['environment'] in click_sign_envs.keys(), "Provided environment '{}' not recognized in defined click_sign_envs {}".format(kwargs['environment'], str(FACE_ENVS.keys()))
                self.environment = kwargs['environment']

        self.url = click_sign_envs[self.environment]

        self.session = requests.Session()


    @property
    def credentials(self):
        """
        Return current credentials dict
        """
        return {
            'user': self.user,
            'password': self.password,
        }


    def method(self, method, resource, download=False, **kwargs):
        """
        Main method handler

        Fetch the requested URL with the requested action through the Session (with injected credentials) and return a JSON representeation of the response with the resultant code
        """
        url = self.url + resource

        # Prepare base request API params (user, password, request)
        # see https://api.clickandsign.eu/dtd/clickandsign/v1/es/index.html#overview

        kwargs['json'] = {
            **kwargs.get('json', {}),
            **self.credentials,
            'request': resource.upper(),
        }

        response = self.session.request(method=method, url=url, **kwargs)

        if download:
            return {
                'code': response.status_code,
                'result': BytesIO(response.content),
                'error': True if response.status_code >= 400 else False,
            }

        # Handle errors
        if response.status_code >= 400:
            return {
                'code': response.status_code,
                'error': True,
                'message': str(response),
            }
        else:
            return {
                'code': response.status_code,
                'result': response.json(),
                'error': False,
            }


    def get(self, resource, **kwargs):
        """
        GET method, it dispatch a session.get method consuming the desired resource
        """
        return self.method(method="GET", resource=resource, **kwargs)


    def post(self, resource, **kwargs):
        """
        POST method, it dispatch a session.get method consuming the desired resource
        """
        return self.method(method="POST", resource=resource, **kwargs)


    def download(self, resource, **kwargs):
        """
        DOWNLOAD method, it dispatch a session.get method consuming the desired resource in download mode
        """
        return self.method(method="GET", resource=resource, download=True, **kwargs)
