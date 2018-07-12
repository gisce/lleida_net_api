# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, post_load
from munch import Munch

class Objectify(Munch):
    pass

class ResponseSchema(Schema):
    """
    Base response format
    See https://api.clickandsign.eu/dtd/clickandsign/v1/es/index.html#format
    """
    code = fields.Integer(required=True)
    status = fields.Str(required=True)
    request = fields.Str(required=True)
    request_id = fields.Int()

    @post_load
    def create_model(self, data):
        return Objectify(**data)


class BytesIO_field(fields.Field):
    def _serialize(self, value, attr, obj):
        if value is None:
            return ''
        return value



"""
API response
"""

class APIResponseSchema(Schema):
    """
    API Response schema
    """
    code = fields.Integer(required=True)
    error = fields.Boolean(required=True)
    result = fields.Dict(required=True)
    message = fields.Str(required=False)

    @post_load
    def create_model(self, data):
        return Objectify(**data)



"""
Signature
"""

class SignatorieSchema(Schema):
    phone = fields.Str()
    email = fields.Str()
    url_redirect = fields.Str()
    # Other user labels

    @post_load
    def create_model(self, data):
        return Objectify(**data)


class LevelSchema(Schema):
    level_order = fields.Integer(required=True)
    required_signatories_to_complete_level = fields.Integer()
    signatories = fields.Nested(SignatorieSchema, many=True, required=True)

    @post_load
    def create_model(self, data):
        return Objectify(**data)


class FileSchema(Schema):
    filename = fields.Str(required=True)
    content = fields.Str() # TODO must be base64 urlencoded RFC-4648
    file_group = fields.Str(required=True)
    sign_on_landing = fields.Str()

    @post_load
    def create_model(self, data):
        return Objectify(**data)


class SignatureSchema(Schema):
    config_id = fields.Integer(required=True)
    contract_id = fields.Str(required=True)
    level = fields.Nested(LevelSchema, many=True, required=True)
    file = fields.Nested(FileSchema, many=True)

    @post_load
    def create_model(self, data):
        return Objectify(**data)


class StartSignatureSchema(ResponseSchema):
    signature = fields.Nested(SignatureSchema, many=False, required=True)

    @post_load
    def create_model(self, data):
        return Objectify(**data)



"""
Configuration
"""

class ConfigSchema(Schema):
    config_id = fields.Integer(required=True)
    name = fields.Str(required=True)
    status = fields.Str(required=True)

    @post_load
    def create_model(self, data):
        return Objectify(**data)


class GetConfigListSchema(ResponseSchema):
    config = fields.Nested(SignatureSchema, many=True, required=True)

    @post_load
    def create_model(self, data):
        return Objectify(**data)
