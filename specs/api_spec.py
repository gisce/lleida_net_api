# -*- coding: utf-8 -*-
from __future__ import (absolute_import)
import vcr
import io
from munch import Munch

import logging
logging.basicConfig(level=logging.DEBUG)

from lleida_net.click_sign import CS_API

fixtures_path = 'specs/fixtures/click_sign/'

spec_VCR = vcr.VCR(
    record_mode='new',
    cassette_library_dir=fixtures_path
)

config = {
    'user': 'lumina',
    'password': 'password',
    'environment': 'prod'
}

scope = {
    "get_config": {
        "url": "/get_config"
    }
}

with description('A new CS API'):
    with before.each:
        with spec_VCR.use_cassette('init.yaml'):
            self.config = config
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


    with context('config fetch'):
        with it('must work as expected'):
            with spec_VCR.use_cassette('get_config_list.yaml'):
                request_result = self.api.post("get_config_list")
                assert request_result['code'] == 200

                assert "result" in request_result
                result = Munch(request_result['result'])
                assert "config" in result
                config = result.config
                assert type(config) == list, "Config must be a list of configurations"
