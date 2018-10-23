# -*- coding: utf-8 -*-
from __future__ import (absolute_import)
import vcr
import logging
from expects import expect, raise_error
import os
import base64
from .config import config_id


try:
    from urllib.parse import quote_plus
except:
    from six.moves.urllib.parse import quote as quote_plus

logging.basicConfig(level=logging.CRITICAL)

from lleida_net.click_sign import Client, NotValidSignatureSchemaException, serializers as schema


ATTACHMENTS_PATH = os.path.dirname(os.path.realpath(__file__)) + "/attachments"
fixtures_path = 'specs/fixtures/client/'
spec_VCR = vcr.VCR(
    record_mode='new',
    cassette_library_dir=fixtures_path
)

config = {
    'user': 'user',
    'password': 'key',
    'environment': 'prod'
}

with description('A new CS client'):
    with before.each:
        with spec_VCR.use_cassette('init.yaml'):
            self.config = config
            self.client = Client(**config)

    with context('initialization'):
        with it('must be performed as expected'):
            with spec_VCR.use_cassette('init.yaml'):
                assert self.client

    with context('Signature'):
        with context('start'):
            with it('must work as expected'):
                with spec_VCR.use_cassette('signature_start.yaml'):
                    with open(ATTACHMENTS_PATH + "/dummy.pdf", "rb") as pdf:
                        encoded_pdf = quote_plus(base64.b64encode(pdf.read()))

                    data = {
                        "config_id": config_id,
                        "contract_id": "ContractID",
                        "level": [
                            {
                                "level_order": 0,
                                "signatories": [
                                    {
                                        "phone": "+34666666666",
                                        "email": "xtorello@gisce.net",
                                        "name": "Name1",
                                        "surname": "Surname1"
                                    },
                                ]
                            },
                        ],
                        "file": [
                            {
                                "filename": "contract.pdf",
                                "content": encoded_pdf,
                                "file_group": "contract_files"
                            }
                        ]
                    }

                    response = self.client.signature.start(data)
                    print (response)
                    assert not response.error

            with it('must handle incorrect signature definitions'):
                with spec_VCR.use_cassette('signature_start.yaml'):

                    def incorrect_signature_start():
                        data = {
                            "config_id": 12345,
                            "contract_id": "ContractID",
                            "file": [
                            ]
                        }
                        response = self.client.signature.start(data)

                    expect(incorrect_signature_start).to(raise_error(NotValidSignatureSchemaException))


            with it('must work as expected'):
                with spec_VCR.use_cassette('signature_status.yaml'):
                    response = self.client.signature.list
                    print (response)
                    # response = self.client.signature.status(signatory_id)
                    assert response


    with context('Configuration'):
            with it('must handle config lists'):
                with spec_VCR.use_cassette('configuration_list.yaml'):
                    response = self.client.configuration.get_config_list()
                    assert response and response.code == 200, "Get config list application status must be OK"

                    config = response.config
                    assert type(config) == list and len(config)>0, "Returning config must be a non-empty list"

                    for a_config in config:
                        validate_config = schema.ConfigSchema().load(a_config)
                        assert not validate_config.errors

            with it('must get config detail as expected'):
                with spec_VCR.use_cassette('configuration_list.yaml'):
                    response = self.client.configuration.get_config_list()
                    config = response.config
                    a_config = schema.ConfigSchema().load(config[0])
                    config_id = a_config.data.config_id
                    response = self.client.configuration.get_config(config_id)
