# -*- coding: utf-8 -*-

from .api import CS_API
from . import serializers as schema
import os

class ClientException(Exception):
    """Base ClientException exception"""
    pass

class NotValidSchemaException(ClientException):
    """Signature data is not valid"""
    pass

class NotValidAPIResponseSchemaException(NotValidSchemaException):
    """Signature data is not valid"""
    pass

class NotValidSignatureSchemaException(NotValidSchemaException):
    """Signature data is not valid"""
    pass

class NotValidConfigurationSchemaException(NotValidSchemaException):
    """Configuration data is not valid"""
    pass


class ClientResource(object):
    def __init__(self, api):
        self.api = api

    def response(self, response, response_schema):
        """
        Validates and prepare the response depending on passed schema
        """
        # Validate base API Response schema
        response_object = schema.APIResponseSchema().load(response)
        print (response_object)
        if response_object.errors:
            raise NotValidAPIResponseSchemaException(response_object.errors)

        validation_object = response_schema().load(response_object.data.result)
        print (validation_object)
        if validation_object.errors:
            raise NotValidSchemaException(response_schema, validation_object.errors)

        return validation_object.data


class Configuration(ClientResource):
    
    def get_config_list(self):
        """
        Return the result of the Config List request if no errors appears
        """
        try:
            response = self.api.post(resource="get_config_list")
            response_object = schema.APIResponseSchema().load(response)
            assert not response_object.errors
            return response_object
        except Exception as e:
            raise NotValidConfigurationSchemaException(str(e))

    def get_config(self, config_id):
        """
        Return the detail of the requested config
        """
        assert type(config_id) == int, "Provided config_id is not correct '{}'".format(config_id)

        config = {
            'config_id': config_id,
        }

        try:
            response = self.api.post(resource="get_config", json=config)
            response_object = schema.APIResponseSchema().load(response)
            assert not response_object.errors
            return response_object
        except Exception as e:
            raise NotValidConfigurationSchemaException(str(e))



class Signature(ClientResource):

    def start(self, data):
        assert isinstance(data, dict), "Data must be a dict"

        # Validate data
        signature_schema = schema.SignatureSchema().load(data)

        if not signature_schema.errors:
            signature = schema.StartSignatureSchema().dump({"signature": data}).data
            # return signature
            return self.api.post(resource="start_signature", json=signature)
        else:
            raise NotValidSignatureSchemaException(signature_schema.errors)



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
