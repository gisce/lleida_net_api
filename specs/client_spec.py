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
            self.expected = expected
            self.client = CS_API(**config)

    with context('initialization'):
        with it('must be performed as expected'):
            with spec_VCR.use_cassette('init.yaml'):
                assert self.client
