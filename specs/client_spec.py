# -*- coding: utf-8 -*-
from __future__ import (absolute_import)
import vcr
import logging
from expects import expect, raise_error

logging.basicConfig(level=logging.DEBUG)

from lleida_net.click_sign import Client, NotValidSignatureSchemaException

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
                    data = {
                        "config_id": 12345,
                        "contract_id": "ContractID",
                        "level": [
                            {
                                "level_order": 0,
                                "signatories": [
                                    {
                                        "phone": "+34666666666",
                                        "email": "signatory1@mail.com",
                                        "name": "Name1",
                                        "surname": "Surname1"
                                    },
                                ]
                            },
                        ],
                        "file": [
                            {
                                "filename": "contract.pdf",
                                "content": "{{base64_file_content}}",
                                "file_group": "contract_files"
                            }
                        ]
                    }

                    response = self.client.signature.start(data)

            with it('must handle incorrect signature definitions'):
                with spec_VCR.use_cassette('signature_start.yaml'):

                    def incorrect_signature_start ():
                        data = {
                            "config_id": 12345,
                            "contract_id": "ContractID",
                            "file": [
                                {
                                    "filename": "contract.pdf",
                                    "content": "{{base64_file_content}}",
                                    "file_group": "contract_files"
                                }
                            ]
                        }

                        response = self.client.signature.start(data)

                    expect(incorrect_signature_start).to(raise_error(NotValidSignatureSchemaException))
