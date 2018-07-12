# -*- coding: utf-8 -*-

from .api import CS_API
from . import serializers as schema
import os

class ClientException(Exception):
    """Base ClientException exception"""
    pass

class NotValidSignatureSchemaException(ClientException):
    """Signature data is not valid"""
    pass


class Configuration(object):
    def __init__(self, api):
        self.api = api

    def get_config_list(self):
        try:
            response = self.api.post(resource="get_config_list")
            response_object = schema.APIResponseSchema().load(response)
            assert not response_object.errors
            return response_object
        except Exception as e:
            raise NotValidConfigurationSchemaException(str(e))


class Signature(object):
    def __init__(self, api):
        self.api = api

    def start(self, data):
        assert isinstance(data, dict), "Data must be a dict"

        # Validate data
        signature_schema = schema.SignatureSchema().load(data)

        if not signature_schema.errors:
            signature = schema.StartSignatureSchema().dump({"signature": data}).data
            # return signature
            return self.api.post(resource="start_signature", json=signature)
        else:
            raise NotValidSignatureSchemaException(signature.errors)



class Client(object):
    def __init__(self, user=None, password=None, environment=None):

        # Handle the user
        self.user = user
        if not user:
            self.user = os.getenv('CS_USER')
        assert self.user, "The user is needed to initialize the Lleida.net Click'n'Sign connection"

        # Handle the password
        self.password = password
        if not password:
            self.password = os.getenv('CS_PASSWORD')
        assert self.password, "The password is needed to initialize the Lleida.net Click'n'Sign connection"

        # Handle the env, by default prod
        self.environment = "prod"
        if environment:
            self.environment = environment

        self.API = CS_API(user=self.user, password=self.password, environment=self.environment)

        # Prepare API resources
        self.signature = Signature(self.API)
        self.configuration = Configuration(self.API)
