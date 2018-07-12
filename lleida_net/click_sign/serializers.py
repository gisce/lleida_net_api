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



class SMSSchema(Schema):
    registered = fields.Str()
    type = fields.Str()
    reminder_lapse = fields.Str()
    sender = fields.Str()
    recipient = fields.Str()
    text = fields.Str()


class SignatureOnSignSchema(Schema):
    handwritten = fields.Str()
    otp = fields.Str()
    otp_length = fields.Int()
    otp_max_retries = fields.Int()
    otp_sending = fields.Str()


class LandingSchema(Schema):
    landing_template = fields.Str()
    signature_type = fields.Str()
    signature_on_sign_required_elements = fields.Nested(SignatureOnSignSchema)


class EmailSchema(Schema):
    registered = fields.Str()
    type = fields.Str()
    reminder_lapse = fields.Str()
    from_name = fields.Str()
    to = fields.Str()
    cc = fields.Str()
    bcc = fields.Str()
    subject = fields.Str()
    body_template = fields.Str()
    body_free_text = fields.Str()
    attachment_file_group = fields.List(fields.Str())


class ConfigInfoSchema(Schema):
    name = fields.Str()
    expire_lapse = fields.Integer()
    auto_cancel = fields.Str()
    default_sms_sender = fields.Str()
    default_email_from_name = fields.Str()
    registered_company_name = fields.Str()
    registered_company_vat_number = fields.Str()
    registered_langs = fields.Str()
    lang = fields.Str()
    signatory_cb_url_ = fields.Str()
    signature_cb_url = fields.Str()
    color_background = fields.Str()
    color_text = fields.Str()
    color_button_background = fields.Str()
    color_button_text = fields.Str()
    logo = fields.Int()
    status = fields.Str()
    signatory_fields = fields.List(fields.Str())
    sms = fields.Nested(SMSSchema, many=True)
    email = fields.Nested(EmailSchema, many=True)
    landing = fields.Nested(LandingSchema, many=False)

    @post_load
    def create_model(self, data):
        return Objectify(**data)


class ConfigDetailSchema(Schema):
    config_id = fields.Integer(required=True)
    config = fields.Nested(ConfigInfoSchema)

    @post_load
    def create_model(self, data):
        return Objectify(**data)


class ConfigSchema(Schema):
    config_id = fields.Integer(required=True)
    name = fields.Str(required=True)
    status = fields.Str(required=True)

    @post_load
    def create_model(self, data):
        return Objectify(**data)


class GetConfigListSchema(ResponseSchema):
    config = fields.Nested(ConfigSchema, many=True, required=True)

    @post_load
    def create_model(self, data):
        return Objectify(**data)


class GetConfigListSchema(ResponseSchema):
    config = fields.Nested(ConfigSchema, many=True, required=True)

    @post_load
    def create_model(self, data):
        return Objectify(**data)
