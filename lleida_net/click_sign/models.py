# -*- coding: utf-8 -*-
from marshmallow import Schema, fields, post_load
from munch import Munch

## Base response Models and Schemas
class CS_Response(Munch):
    pass

class ResponseSchema(Schema):
    """
    Base response format
    See https://api.clickandsign.eu/dtd/clickandsign/v1/es/index.html#format
    """
    code = fields.Integer()
    status = fields.Str()
    request = fields.Str()
    request_id = fields.Str()
    result = fields.Dict()

    @post_load
    def create_model(self, data):
        return CS_Response(**data)
