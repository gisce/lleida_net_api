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

class NotFoundSignatureException(ClientException):
    """signatory_id requested not exists"""
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
        # print (response_object)
        if response_object.errors:
            raise NotValidAPIResponseSchemaException(response_object.errors)

        validation_object = response_schema().load(response_object.data.result)
        # print (validation_object)
        if validation_object.errors:
            raise NotValidSchemaException(response_schema, validation_object.errors)

        return validation_object.data


class Configuration(ClientResource):

    def get_config_list(self):
        """
        Return the result of the Config List request if no errors appears
        """
        try:
            return self.response(self.api.post(resource="get_config_list"), response_schema=schema.GetConfigListSchema)
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
            return self.response(self.api.post(resource="get_config", json=config), response_schema=schema.ConfigDetailSchema)
        except Exception as e:
            raise NotValidConfigurationSchemaException(str(e))

    def set_config(self, data):
        """
        Set new config
        """
        assert isinstance(data, dict), "Data must be a dict"

        config = {
            'config': data,
        }

        # Validate passed data
        data_schema = schema.ConfigDetailSchema().load(config)
        print (data_schema)
        if not data_schema.errors:
            try:
                # return self.response(self.api.post(resource="get_config", json=config), response_schema=schema.ConfigDetailSchema)
                return self.api.post(resource="set_config", json=config)
            except Exception as e:
                raise NotValidConfigurationSchemaException(str(e))
        return False


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

    @property
    def list(self):
        try:
            return self.api.post(resource="get_signature_list", json={ "start_date": 1517443200})
        except Exception as e:
            raise NotValidSignatureSchemaException(str(e))

    def status(self, signatory_id):
        """
        It tries to reach the status of an already started signature.

        If not, raises an exception
        """
        assert isinstance(signatory_id, int), "signatory_id must be an integer"

        try:
            response = self.api.post(resource="get_signatory_details", json={"signatory_id": signatory_id})
            validated_response = schema.StatusSignatureSchema().load(response)

        except Exception as e:
            raise NotValidSignatureSchemaException(str(e))


        if not validated_response.errors and validated_response.data.result.signatory_details:
            return validated_response.data.result.signatory_details

        raise NotFoundSignatureException()

    def get_document_stamp(self, data):
        """
        It tries to reach the signatory stamp of an already signed signature.
        If not, raises an exception
        """
        assert isinstance(data, dict), "Data must be a dict"
        data['file_group'] = "SIGNATORY_STAMP"

        try:
            signatory_data = schema.SignatoryStampSchema().dump(data).data
            response = self.api.post(
                resource="get_document", json=signatory_data)
            validated_response = schema.GetDocumentSchema().load(response)

        except Exception as e:
            raise NotValidSignatureSchemaException(str(e))

        if not validated_response.errors and validated_response.data.result.document:
            return validated_response.data.result.document

        raise NotFoundSignatureException()

    def get_document_evidence(self, data):
        """
        It tries to reach the signatory evidence of an already signed signature.
        If not, raises an exception
        """
        assert isinstance(data, dict), "Data must be a dict"
        data['file_group'] = "SIGNATORY_EVIDENCE"

        try:
            signatory_data = schema.SignatoryStampSchema().dump(data).data
            response = self.api.post(
                resource="get_document", json=signatory_data)
            validated_response = schema.GetDocumentSchema().load(response)

        except Exception as e:
            raise NotValidSignatureSchemaException(str(e))

        if not validated_response.errors and validated_response.data.result.document:
            return validated_response.data.result.document

        raise NotFoundSignatureException()


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
