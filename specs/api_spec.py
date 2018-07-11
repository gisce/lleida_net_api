# -*- coding: utf-8 -*-
from __future__ import (absolute_import)
import vcr
import io

import logging
logging.basicConfig(level=logging.DEBUG)

from lleida_net.click_sign import CS_API

fixtures_path = 'specs/fixtures/click_sign/'

spec_VCR = vcr.VCR(
    record_mode='all',
    cassette_library_dir=fixtures_path
)

config = {
    'user': 'the_key',
    'password': 'the_secret',
    'environment': 'prod'
}

scope = {
    "get_config": {
        "url": "/get_config"
    }
}

expected = {
}

with description('A new CS API'):
    with before.each:
        with spec_VCR.use_cassette('init.yaml'):
            self.config = config
            self.expected = expected
            self.api = CS_API(**config)

    with context('initialization'):
        with it('must be performed as expected'):
            with spec_VCR.use_cassette('init.yaml'):
                assert type(self.api.user) == str, "User format is not the expected (str)"
                assert self.api.user == self.config['user'], "User is not the expected one"

                assert type(self.api.password) == str, "Password format is not the expected (str)"
                assert self.api.password == self.config['password'], "Password is not the expected one"

                assert type(self.api.environment) == str, "Password format is not the expected (str)"
                assert self.api.environment == self.config['environment'], "Password is not the expected one"
