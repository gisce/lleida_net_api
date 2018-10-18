# -*- coding: utf-8 -*-
from __future__ import (absolute_import)
import vcr
from expects import expect, raise_error

from lleida_net.click_sign import serializers

import logging
logging.basicConfig(level=logging.CRITICAL)


fixtures_path = 'specs/fixtures/callback/'

spec_VCR = vcr.VCR(
    record_mode='new',
    cassette_library_dir=fixtures_path
)

with description('A new Callback'):

        with it('must work as expected'):
            with spec_VCR.use_cassette('callback.yaml'):
                callback = {
                    'data': {
                        "signature_id": "1111000000",
                        "signatory_id": "1111000002",
                        "contract_id": "Contract101",
                        "status": "evidence_generated",
                        "status_date": "1522111485"
                    }
                }

                validate = serializers.CallbackSchema().load(callback['data'])
                assert not validate.errors, "There must be no errors while validating API response: {}".format(validate.errors)

        with it('must handle incorrect schema'):
            with spec_VCR.use_cassette('callback.yaml'):

                def incorrect_schema():
                    callback = {
                        'data': {
                            "signature_id": "not_an_integer",
                            "signatory_id": "not_an_integer",
                            "contract_id": "Contract101",
                            "status": "inexistent status",
                            "status_date": "1522111485"
                        }
                    }
                    validate = serializers.CallbackSchema().load(callback['data'])
                    assert not validate.errors, "There must be no errors while validating API response: {}".format(validate.errors)
                    assert len(validate.error) == 3, "both sign* ids and status must be incorrect (3 errors vs '{}')".format(len(validate.error))

                expect(incorrect_schema).to(raise_error(AssertionError))
