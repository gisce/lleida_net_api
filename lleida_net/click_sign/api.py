# -*- coding: utf-8 -*-

import logging
from io import BytesIO
import requests

click_sign_envs = {
    'prod': 'https://api.clickandsign.eu/cs/',
    # 'staging': None,
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

