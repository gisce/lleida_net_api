# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, post_load
from munch import Munch

class CS_Response(Munch):
    pass


class ResponseSchema(Schema):
    """
    Base response format
    See https://api.clickandsign.eu/dtd/clickandsign/v1/es/index.html#format
    """
    code = fields.Integer(required=True)
    status = fields.Str(required=True)
    request = fields.Str(required=True)
    request_id = fields.Str()

    @post_load
    def create_model(self, data):
        return CS_Response(**data)


class BytesIO_field(fields.Field):
    def _serialize(self, value, attr, obj):
        if value is None:
            return ''
        return value


class SignatorieSchema(Schema):
    phone = fields.Str()
    email = fields.Str()
    url_redirect = fields.Str()
    # Other user labels


class LevelSchema(Schema):
    level_order = fields.Integer(required=True)
    required_signatories_to_complete_level = fields.Integer()
    signatories = fields.Nested(SignatorieSchema, many=True, required=True)


class FileSchema(Schema):
    filename = fields.Str(required=True)
    content = fields.Str() # TODO must be base64 urlencoded RFC-4648
    file_group = fields.Str(required=True)
    sign_on_landing = fields.Str()


class SignatureSchema(Schema):
    config_id = fields.Integer(required=True)
    contract_id = fields.Str(required=True)
    level = fields.Nested(LevelSchema, many=True, required=True)
    file = fields.Nested(FileSchema, many=True)


class StartSignatureSchema(ResponseSchema):
    signature = fields.Nested(SignatureSchema, many=False, required=True)
