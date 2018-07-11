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


class Signature(object):
    def __init__(self, api):
        self.api = api

    def start(self, data):
        assert isinstance(data, dict), "Data must be a dict"

        # Validate data
        signature = schema.SignatureSchema().load(data)

        if not signature.errors:
            # Use a cleaned_data instead of passed one
            # It validates and just serializes the accompliant part of the schema
            clean_passed_data = schema.SignatureSchema().dump(data)
            return self.api.post(resource="start_signature", json=signature.data)
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
